# agent.py
import re

from tools.rag_tool import (
    rag_tool,
    stream_answer,
    get_best_distance,
    get_effective_query
)

from tools.calculator_tool import (
    calculator_tool
)

from tools.web_search_tool import (
    web_search_tool
)

# ==================================================
# Tool Registry
# ==================================================

TOOLS = {

    "rag_search": rag_tool,

    "calculator": calculator_tool,

    "web_search": web_search_tool
}

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

    THRESHOLD = 0.85

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

    tool = TOOLS[
        tool_name
    ]

    return tool(
        question
    )


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

    if tool_name == "calculator":

        stream_answer.last_sources = []

        result = calculator_tool(
            question
        )

        yield result["answer"]

        yield "\n__END_STREAM__"

        return

    # ------------------------------------------
    # Web Search
    # ------------------------------------------

    if tool_name == "web_search":

        result = web_search_tool(
            question
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