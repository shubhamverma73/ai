from mcp.server.fastmcp import FastMCP
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# ==================================================
# Local Tools
# ==================================================

from tools.calculator_tool import (
    calculator_tool
)

from tools.rag_tool import (
    rag_tool
)

from tools.web_search_tool import (
    web_search_tool
)

mcp = FastMCP(
    "RAG Agent MCP Server"
)


# ==================================================
# RAG Search Tool
# ==================================================
# Executes the existing RAG pipeline.
#
# Flow:
#
# MCP Client
#     ↓
# MCP Server
#     ↓
# rag_tool()
#
# Returns:
#
# {
#     "answer": "...",
#     "sources": [...]
# }
# ==================================================

@mcp.tool() # It turns the calculator function into an MCP tool. The calculator is no longer just a local Python function; it is now a remotely callable MCP tool.
def rag_search(question: str):

    print("\n[MCP SERVER] RAG Tool Executed")

    return rag_tool(question)

@mcp.tool()
def calculator(question: str):

    print("\n[MCP SERVER] Calculator Tool Executed")

    return calculator_tool(question)

@mcp.tool()
def web_search(question: str):

    print("\n[MCP SERVER] Web Search Tool Executed")

    return web_search_tool(question)


if __name__ == "__main__":

    #mcp.run()

    print("\nStarting MCP SSE Server...")

    mcp.run(transport="sse")