# agent.py
import re
import asyncio

from tools.rag_tool import (
    stream_answer,
    get_best_distance,
    get_effective_query
)

from mcp_client.client import (
    call_tool
)

# ==================================================
# Tool Decision Logic
# ==================================================

def decide_tool(question):

    question_lower = (
        question.lower().strip()
    )

    # ------------------------------------------
    # Calculator Detection
    # ------------------------------------------

    math_symbols = [

        "+",
        "-",
        "*",
        "/",
        "%",
        "**"
    ]

    if any(
        symbol in question
        for symbol in math_symbols
    ):
        return "calculator"

    math_keywords = [

        "plus",
        "add",

        "minus",
        "subtract",

        "multiply",
        "multiplied",
        "times",

        "divide",
        "divided",

        "sqrt",
        "square root",

        "power",

        "calculate"
    ]

    math_pattern = re.search(
        r"\d+\s*[\+\-\*\/%]\s*\d+",
        question
    )

    if math_pattern:
        return "calculator"

    # ------------------------------------------
    # Distance Routing
    # ------------------------------------------

    routing_query = (
        get_effective_query(
            question
        )
    )

    print(
        f"\nROUTING QUERY:\n{routing_query}"
    )

    best_distance = (
        get_best_distance(
            routing_query
        )
    )
    print(
        f"\nBEST DISTANCE: {best_distance}"
    )

    THRESHOLD = 0.80

    if best_distance <= THRESHOLD:

        print(
            "ROUTE => RAG"
        )

        return "rag_search"

    print(
        "ROUTE => WEB"
    )

    return "web_search"


# ==================================================
# Non Streaming Agent
# ==================================================

def agent_answer(question):

    tool_name = decide_tool(
        question
    )

    print("\nAGENT DECISION:")
    print(tool_name)

    # ------------------------------------------
    # Calculator via MCP
    # ------------------------------------------

    if tool_name == "calculator":

        return asyncio.run(
            call_tool(
                "calculator",
                {
                    "question": question
                }
            )
        )

    # ------------------------------------------
    # RAG via MCP
    # ------------------------------------------

    if tool_name == "rag_search":

        return asyncio.run(
            call_tool(
                "rag_search",
                {
                    "question": question
                }
            )
        )

    # ------------------------------------------
    # Web Search via MCP
    # ------------------------------------------

    if tool_name == "web_search":

        return asyncio.run(
            call_tool(
                "web_search",
                {
                    "question": question
                }
            )
        )

    # ------------------------------------------
    # Safety Fallback
    # ------------------------------------------

    return {
        "answer": "No suitable tool found.",
        "sources": []
    }


# ==================================================
# Streaming Agent
# ==================================================

def stream_agent_answer(question):

    tool_name = decide_tool(
        question
    )

    print("\nAGENT DECISION:")
    print(tool_name)

    # ------------------------------------------
    # Calculator
    # ------------------------------------------

    # ------------------------------------------
    # Calculator via MCP
    # ------------------------------------------
    #
    # Flow:
    #
    # Agent
    #   ↓
    # MCP Client
    #   ↓
    # MCP Server
    #   ↓
    # calculator_tool()
    #
    # The calculator is no longer executed
    # directly inside the agent.
    #
    # Instead, the agent calls the MCP server.
    # ------------------------------------------

    if tool_name == "calculator":

        stream_answer.last_sources = []

        result = asyncio.run(
            call_tool(
                "calculator",
                {
                    "question": question
                }
            )
        )

        yield result["answer"]

        yield "\n__END_STREAM__"

        return

    # ------------------------------------------
    # Web Search via MCP
    # ------------------------------------------
    #
    # Agent
    #   ↓
    # MCP Client
    #   ↓
    # MCP Server
    #   ↓
    # web_search_tool()
    #
    # Web Search now executes remotely
    # through the MCP server.
    # ------------------------------------------

    if tool_name == "web_search":

        result = asyncio.run(
            call_tool(
                "web_search",
                {
                    "question": question
                }
            )
        )

        stream_answer.last_sources = (
            result["sources"]
        )

        yield result["answer"]

        yield "\n__END_STREAM__"

        return

    # ------------------------------------------
    # RAG
    # ------------------------------------------

    if tool_name == "rag_search":

        yield from stream_answer(
            question
        )