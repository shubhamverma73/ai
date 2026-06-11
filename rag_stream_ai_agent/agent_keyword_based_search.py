# agent.py
import re

from tools.rag_tool import (
    rag_tool,
    stream_answer
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
    
    words = set(
        re.findall(
            r"\b\w+\b",
            question_lower
        )
    )

    for keyword in math_keywords:

        if " " in keyword:

            if keyword in question_lower:
                return "calculator"

        else:

            if keyword in words:
                return "calculator"

    # ------------------------------------------
    # Web Search Detection
    # ------------------------------------------

    web_keywords = [

        "latest",
        "current",
        "today",
        "news",
        "recent",
        "update",
        "updates",

        "live",

        "weather",

        "gold price",
        "silver price",

        "stock",
        "stocks",
        "share price",

        "cricket",
        "football",
        "ipl",

        "search web",
        "web search",
        "internet",

        "who is currently",
        "what happened",
        "breaking"
    ]

    # ============== Just for debugging matching keywords ==============
    print("\nQUESTION:")
    print(question_lower)

    print("\nWEB KEYWORD CHECK:")

    for keyword in web_keywords:

        result = keyword in question_lower

        print(
            f"web keyword and question '{keyword}' -> {result}"
        )
    # =================================================

    words = set(
        re.findall(
            r"\b\w+\b",
            question_lower
        )
    )

    for keyword in web_keywords:

        if " " in keyword:

            if keyword in question_lower:
                return "web_search"

        else:

            if keyword in words:
                return "web_search"

    # ------------------------------------------
    # Default
    # ------------------------------------------

    return "rag_search"


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