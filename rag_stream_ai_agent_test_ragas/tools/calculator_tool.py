# calculator_tool.py

import math
import re


# ==================================================
# Extract Math Expression
# ==================================================

def extract_expression(text):

    text = text.lower().strip()

    # ------------------------------------------
    # Natural Language Replacements
    # ------------------------------------------

    replacements = {
        "plus": "+",
        "add": "+",

        "minus": "-",
        "subtract": "-",

        "multiplied by": "*",
        "multiply by": "*",
        "times": "*",

        "divided by": "/",
        "divide by": "/",

        "mod": "%",
        "modulus": "%",

        "power of": "**"
    }

    for key, value in replacements.items():
        text = text.replace(
            key,
            value
        )

    # ------------------------------------------
    # Square Root
    # ------------------------------------------

    sqrt_match = re.search(
        r"(sqrt|square root of)\s*(\d+)",
        text
    )

    if sqrt_match:

        number = sqrt_match.group(2)

        return f"sqrt({number})"

    # ------------------------------------------
    # Extract Math Expression
    # ------------------------------------------

    expression = re.findall(
        r"[0-9\.\+\-\*\/%\(\)]+" ,
        text
    )

    expression = "".join(
        expression
    )

    return expression.strip()


# ==================================================
# Calculator Tool
# ==================================================

def calculator_tool(question):

    """
    Examples:

    45+58
    45+58 kitna hai
    100 divided by 4
    what is 25 multiplied by 10
    sqrt 81
    square root of 81
    """

    try:

        expression = extract_expression(
            question
        )

        if not expression:

            raise ValueError(
                "No expression found."
            )

        print(
            f"CALCULATOR EXPRESSION: {expression}"
        )

        allowed_names = {

            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,

            "sqrt": math.sqrt
        }

        result = eval(
            expression,
            {"__builtins__": {}},
            allowed_names
        )

        return {
            "answer": str(result),
            "sources": []
        }

    except Exception as e:

        print(
            f"Calculator Error: {e}"
        )

        return {
            "answer": "Invalid calculation.",
            "sources": []
        }