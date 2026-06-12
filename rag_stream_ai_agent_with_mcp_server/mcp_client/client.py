import asyncio
import json
import time

from mcp import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters
)

# ==================================================
# MCP Client Helper
# ==================================================
# This file provides a reusable helper function
# for calling tools exposed by the MCP server.
# This function can call any MCP tool.
#
# Example:
# await call_tool("calculator", {...})
# await call_tool("weather", {...})
# ==================================================
start = time.time() # calculate execution time

async def call_tool(
    tool_name,
    arguments
):

    total_start = time.perf_counter()

    # Path to the MCP server
    server_params = (
        StdioServerParameters(
            command="python",
            args=[
                "mcp_server/server.py" # This function listens on the MCP server and it means python mcp_server/server.py
            ]
        )
    )

    '''
    Diagram:
        +----------------+
        |   MCP Client   |
        +----------------+
                |
                | stdin/stdout
                |
        +----------------+
        |   MCP Server   |
        +----------------+
    '''

    '''
        If we call call_tool() multiple times like this:
            await call_tool("calculator", ...)
            await call_tool("weather", ...)
            await call_tool("web_search", ...)

        In Background:
            - Each call to call_tool() starts a new MCP server process, like this:
                python mcp_server/server.py # calculator
                python mcp_server/server.py # weather
                python mcp_server/server.py # web_search

            - This is inefficient because starting the MCP server process takes time.
        Optimization:
            - Start the MCP server process once and keep it running.
            - Reuse the same MCP server process for multiple tool calls.
            - This way, we only pay the startup cost once.

        Note:
            - In production, the MCP server would be a long-running service that is always on.
        
        So the process flow would look like this:
        ┌─────────────────┐
        │     Agent       │
        └────────┬────────┘
                │
                │
                ▼
        ┌─────────────────┐
        │   MCP Client    │
        └────────┬────────┘
                │
                │ persistent connection
                ▼
        ┌─────────────────┐
        │   MCP Server    │
        │   (Alive)       │
        └─────────────────┘

    So to make it alive always after start the server we will create some files like this:
        mcp_client/
            │
            ├── manager.py
            ├── client.py
            └── ...

    Currently only calculator tool taking near about:
        ≈ 5-10 sec

    So after impementing the optimization we can reduce the tool execution time to:
        First Call
            ≈ 3-5 sec

        Second Call
            ≈ 50-200 ms

        Third Call
            ≈ 50-200 ms

    Because:
        Server already alive
        Session already initialized
        Models already imported
        Chroma already connected

    Another Benefit:
        from tools.rag_tool import rag_tool
        are calling on every request, means on every request:
            CloudClient(...)
            ChatOllama(...)
            OllamaEmbeddings(...)
    After persistent connection:
    
        Application Start
            ↓
        Load Once
            ↓
        Reuse Forever
    '''

    # Start the MCP server process
    async with stdio_client( # stdio_client is a helper function that abstracts away the details of setting up the stdin/stdout communication with the MCP server process. It takes care of starting the server process and establishing the communication channels. and call this script: python mcp_server/server.py
        server_params
    ) as (
        read_stream,
        write_stream
    ):

        # Create MCP session
        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            # MCP handshake / initialization
            await session.initialize()

            # ----------------------------------
            # Execute Tool
            # ----------------------------------
            tool_start = time.perf_counter()
            result = (
                await session.call_tool(
                    tool_name,
                    arguments
                )
            )
            tool_end = time.perf_counter()
            print(f"[MCP CLIENT] Tool Execution Time: " f"{tool_end - tool_start:.2f} sec" )

            total_end = time.perf_counter()
            print(f"[TOTAL MCP TIME] " f"{total_end-total_start:.2f} sec" )

            # ----------------------------------
            # Safety Check
            # ----------------------------------
            # If the tool returns no content,
            # return None
            # ----------------------------------
            if not result.content:
                return None

            # ----------------------------------
            # Parse MCP Output
            # ----------------------------------
            # Tool output comes as a JSON string:
            #
            # '{"answer":"100","sources":[]}'
            #
            # json.loads() converts it into a
            # Python dictionary:
            #
            # {
            #   "answer": "100",
            #   "sources": []
            # }
            # ----------------------------------
            return json.loads(
                result.content[0].text
            )
        
        '''
        HTTP Transport →        Browser ↔ Website
        WebSocket Transport →   Real-time chat
        Stdio Transport →       Parent Process ↔ Child Process
        '''

# Currently, our MCP client and MCP server are on the same machine, so Studio is the best choice.

# ==================================================
# Entry Point
# ==================================================
if __name__ == "__main__":

    # Run the helper function
    result = asyncio.run(
        call_tool(
            "calculator",
            {
                "question":
                "What is 5 + 5?"
            }
        )
    )

    print(result)

print( "TIME: ", round(time.time() - start,2)," seconds") # calculate execution time