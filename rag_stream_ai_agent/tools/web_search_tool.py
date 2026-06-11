# web_search_tool.py

from ddgs import DDGS

import requests

from bs4 import BeautifulSoup

from langchain_ollama import ChatOllama


# ==================================================
# LLM
# ==================================================

llm = ChatOllama(
    base_url="http://localhost:11434",
    model="llama3:8b",
    temperature=0.3
)

# ==================================================
# Download Page Content
# ==================================================

def fetch_page_content(url):

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # ------------------------------------------
        # Remove junk tags
        # ------------------------------------------

        for tag in soup([
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "nav"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # ------------------------------------------
        # Limit size
        # ------------------------------------------

        text = " ".join(
            text.split()
        )

        return text[:5000]

    except Exception as e:

        print(
            f"FETCH ERROR: {url}"
        )

        print(e)

        return ""


# ==================================================
# Web Search Tool V2
# ==================================================

def web_search_tool(question):

    try:

        print("\nWEB SEARCH:")
        print(question)

        # ------------------------------------------
        # Search
        # ------------------------------------------

        with DDGS() as ddgs:

            search_results = ddgs.text(
                question,
                max_results=5
            )

            results = list(
                search_results
            )

        if not results:

            return {
                "answer": "No web results found.",
                "sources": []
            }

        # ------------------------------------------
        # Build Context
        # ------------------------------------------

        context = ""

        sources = []

        for index, result in enumerate(
            results,
            start=1
        ):

            title = result.get(
                "title",
                ""
            )

            snippet = result.get(
                "body",
                ""
            )

            url = result.get(
                "href",
                ""
            )

            print(
                f"\nFetching: {title}"
            )

            page_content = fetch_page_content(
                url
            )

            if not page_content:

                page_content = snippet

            context += f"""

SOURCE {index}

TITLE:
{title}

URL:
{url}

CONTENT:
{page_content}

--------------------------------------------------

"""

            sources.append(
                {
                    "source": title,
                    "url": url,
                    "page": "-"
                }
            )

        # ------------------------------------------
        # Prompt
        # ------------------------------------------

        prompt = f"""
You are a helpful AI assistant.

Use ONLY the web information below.

If multiple sources agree,
combine them.

If information is missing,
say so.

Web Content:

{context}

Question:
{question}

Instructions:

1. Answer the question directly in the first 1-2 sentences.
2. Use Markdown formatting.
3. Use headings (##) when appropriate.
4. Use bullet points for lists.
5. Keep paragraphs short (2-4 lines maximum).
6. Do not repeat the question.
7. Do not say phrases like:

   * "According to the provided context"
   * "Based on the context"
   * "The context states"
8. If information is unavailable, clearly say:
   "I could not find this information."
9. Do not invent facts or make assumptions.
10. When multiple points exist, summarize first and then provide details.
11. Make the response easy to scan and read.

Answer:
"""

        response = llm.invoke(
            prompt
        )

        return {
            "answer": response.content,
            "sources": sources
        }

    except Exception as e:

        print(
            f"WEB SEARCH ERROR: {e}"
        )

        return {
            "answer": "Web search failed.",
            "sources": []
        }