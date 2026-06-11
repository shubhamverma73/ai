'''
Proposed Final Structure

get_retrieval_query()
build_history_text()
retrieve_context()
build_prompt()
deduplicate_sources()
rag_tool()          # Future Agent Tool
stream_answer()     # Current Flask Streaming

Flow:
    User
        ↓
    stream_answer()
        ↓
    retrieve_context()
        ↓
    build_prompt()
        ↓
    LLM Stream

Aur future:
    Agent
        ↓
    rag_tool()
        ↓
    retrieve_context()
        ↓
    Answer
'''

# rag_tool.py

import os
import chromadb

from dotenv import load_dotenv

from langchain_ollama import (
    ChatOllama,
    OllamaEmbeddings
)

load_dotenv()

# ==================================================
# Chat Memory
# ==================================================

chat_history = []

MAX_HISTORY = 5

# ==================================================
# Follow-Up Detection
# ==================================================

FOLLOWUP_PHRASES = [
    "what about",
    "tell me more",
    "more details",
    "explain that",
    "explain this",
    "and then",
    "what next"
]


def is_followup_question(question):

    question_lower = (
        question.lower().strip()
    )

    # ------------------------------------------
    # Short Question Signal
    # ------------------------------------------

    #if len(question.split()) <= 3:
        #return True

    # ------------------------------------------
    # Follow-Up Phrases
    # ------------------------------------------

    for phrase in FOLLOWUP_PHRASES:

        if phrase in question_lower:
            return True

    return False

# ==================================================
# Query Rewriter
# ==================================================

def rewrite_query_with_llm(question):

    # No history available
    if len(chat_history) == 0:
        return question

    last_chat = chat_history[-1]

    rewrite_prompt = f"""
You are a query rewriting assistant.

Conversation:

User:
{last_chat['user']}

Assistant:
{last_chat['assistant']}

Current User Question:
{question}

Rewrite the current question so it
can be understood independently.

Return ONLY the rewritten question.

Do not explain.
"""

    try:

        response = llm.invoke(
            rewrite_prompt
        )

        rewritten = (
            response.content.strip()
        )

        print(
            "\nREWRITTEN QUERY:"
        )

        print(
            rewritten
        )

        return rewritten

    except Exception as e:

        print(
            f"\nRewrite Error: {e}"
        )

        return question
    

# ==================================================
# Effective Query
# ==================================================

def get_effective_query(question):

    if not chat_history:
        return question

    if not is_followup_question(
        question
    ):
        return question

    return rewrite_query_with_llm(
        question
    )


# ==================================================
# Chroma Connection
# ==================================================

client = chromadb.CloudClient(
    api_key=os.getenv("CHROMA_API_KEY"),
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE")
)

collection = client.get_collection(
    "rag_test_collection"
)

# ==================================================
# Models
# ==================================================

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)

llm = ChatOllama(
    base_url="http://localhost:11434",
    model="llama3:8b",
    temperature=0.3
)

# ==================================================
# Build Retrieval Query
# ==================================================

def get_retrieval_query(question):

    retrieval_query = question

    # ------------------------------------------
    # History-Aware Retrieval
    # ------------------------------------------

    if len(chat_history) > 0:

        last_chat = chat_history[-1]

        retrieval_query = f"""
        Previous Question:
        {last_chat['user']}

        Current Question:
        {question}
        """

    return retrieval_query


# ==================================================
# Build Conversation History
# ==================================================

def build_history_text():

    history_text = ""

    for chat in chat_history:

        history_text += (
            f"User: {chat['user']}\n"
            f"Assistant: {chat['assistant']}\n\n"
        )

    return history_text


# ==================================================
# Retrieve Context From Chroma
# ==================================================

def retrieve_context(question):

    effective_query = (
        get_effective_query(
            question
        )
    )

    #retrieval_query = get_retrieval_query(
        #question
    #)

    #print("\nRETRIEVAL QUERY:")
    print("\nEFFECTIVE QUERY:")

    print(effective_query)

    # ------------------------------------------
    # Create Query Embedding
    # ------------------------------------------

    #query_embedding = embedding_model.embed_query(
        #retrieval_query
        #question
    #)

    query_embedding = (
        embedding_model.embed_query(
            effective_query
        )
    )

    # ------------------------------------------
    # Retrieve Relevant Chunks
    # ------------------------------------------

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    docs = results["documents"][0]

    metadata = results["metadatas"][0]

    print("\nSOURCES RETRIEVED:")

    for m in metadata:

        print(
            m["source"],
            "Page",
            m["page"]
        )

    # ------------------------------------------
    # Debug Retrieved Documents
    # ------------------------------------------

    print("\nRETRIEVED DOCS:")

    for i, doc in enumerate(docs):

        print(f"\n--- DOC {i+1} ---")

        print(doc[:300])

    # ------------------------------------------
    # Limit Context Size
    # ------------------------------------------

    context = "\n\n".join(
        docs[:3]
    )

    return context, metadata


# ==================================================
# Build Prompt
# ==================================================

def build_prompt(
    question,
    context,
    history_text
):

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If answer is not present in context,
say:

"I could not find this information."

Use the conversation history
and provided context.

Conversation History:
{history_text}

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt


# ==================================================
# Remove Duplicate Sources
# ==================================================

def deduplicate_sources(metadata):

    seen = set()

    unique_sources = []

    for source in metadata:

        key = (
            source["source"],
            source["page"]
        )

        if key not in seen:

            seen.add(key)

            unique_sources.append(
                source
            )

    return unique_sources


# ==================================================
# Save Chat Memory
# ==================================================

def save_chat_history(
    question,
    answer
):

    chat_history.append(
        {
            "user": question,
            "assistant": answer
        }
    )

    if len(chat_history) > MAX_HISTORY:

        chat_history.pop(0)


# ==================================================
# RAG Tool
#
# Future LangChain Agent
# will call this function.
# ==================================================

def rag_tool(question):

    history_text = build_history_text()

    context, metadata = retrieve_context(
        question
    )

    prompt = build_prompt(
        question,
        context,
        history_text
    )

    print("=" * 50)

    print(
        "QUESTION:",
        question
    )

    print(
        "CONTEXT LENGTH:",
        len(context)
    )

    print("=" * 50)

    response = llm.invoke(
        prompt
    )

    save_chat_history(
        question,
        response.content
    )

    unique_sources = (
        deduplicate_sources(
            metadata
        )
    )

    return {
        "answer": response.content,
        "sources": unique_sources
    }


# ==================================================
# Streaming Version
#
# Flask currently uses this.
# ==================================================

def stream_answer(question):

    history_text = build_history_text()

    context, metadata = retrieve_context(
        question
    )

    prompt = build_prompt(
        question,
        context,
        history_text
    )

    full_response = ""

    for chunk in llm.stream(
        prompt
    ):

        if chunk.content:

            full_response += (
                chunk.content
            )

            yield chunk.content

    # ------------------------------------------
    # Save Conversation
    # ------------------------------------------

    save_chat_history(
        question,
        full_response
    )

    # ------------------------------------------
    # Save Sources
    # ------------------------------------------

    stream_answer.last_sources = (
        deduplicate_sources(
            metadata
        )
    )

    yield "__END_STREAM__"

# ==================================================
# Distance Router Helper
# ==================================================

def get_best_distance(question):

    query_embedding = embedding_model.embed_query(
        question
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    distances = results.get(
        "distances",
        [[]]
    )

    print("\nTOP DISTANCES:")

    for d in results["distances"][0]:
        print(d)

    if (
        not distances
        or not distances[0]
    ):
        return 999

    return distances[0][0]