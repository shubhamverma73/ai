import asyncio
import json
import time

from mcp import ClientSession

from mcp.client.sse import (
    sse_client
)

# ==================================================
# MCP Server URL
# ==================================================

MCP_SERVER_URL = (
    "http://127.0.0.1:8000/sse"
)

# ==================================================
# Reusable MCP Tool Caller
# ==================================================
#
# Connects to an already running
# MCP SSE server.
#
# Server must be started separately:
#
# python mcp_server/server.py
#
# ==================================================

async def call_tool(
    tool_name,
    arguments
):

    total_start = time.perf_counter()

    # ----------------------------------
    # Connect To SSE Server
    # ----------------------------------

    async with sse_client(
        MCP_SERVER_URL
    ) as (
        read_stream,
        write_stream
    ):

        # ----------------------------------
        # Create Session
        # ----------------------------------

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            # ----------------------------------
            # MCP Handshake
            # ----------------------------------

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

            print(f"\nCALLING MCP TOOL: {tool_name}")
            print(f"[MCP TOOL TIME] " f"{tool_end-tool_start:.2f} sec")

            total_end = time.perf_counter()

            print(f"[TOTAL MCP TIME] " f"{total_end-total_start:.2f} sec")
            print(f"\nMCP TOOL FINISHED: {tool_name}")

            # ----------------------------------
            # Empty Result Safety
            # ----------------------------------

            if not result.content:
                return None

            print(
                f"Tool Result: "
                f"{result.content[0].text}"
            )

            return json.loads(
                result.content[0].text
            )


# ==================================================
# Local Test
# ==================================================

if __name__ == "__main__":

    result = asyncio.run(
        call_tool(
            "calculator",
            {
                "question":
                "What is 100 + 50 ?"
            }
        )
    )

    print(result)