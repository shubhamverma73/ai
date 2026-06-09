'''
Ye realtime chalegi.

    Question
    ↓
    Retriever
    ↓
    Relevant Chunks
    ↓
    Prompt
    ↓
    Ollama
    ↓
    Answer
'''

# rag.py

import json
import os
import chromadb

from dotenv import load_dotenv

from langchain_ollama import (
    ChatOllama,
    OllamaEmbeddings
)

load_dotenv()

# -------------------------
# Chat Memory
# -------------------------

chat_history = []

MAX_HISTORY = 5

# -------------------------
# Chroma Connection
# -------------------------

client = chromadb.CloudClient(
    api_key=os.getenv("CHROMA_API_KEY"),
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE")
)

collection = client.get_collection(
    "rag_test_collection"
)

# -------------------------
# Models
# -------------------------

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)

llm = ChatOllama(
    base_url="http://localhost:11434",
    model="llama3:8b",
    temperature=0.3
)

# -------------------------
# Main Function
# -------------------------

def ask_question(question):

    retrieval_query = question

    if len(chat_history) > 0:

        last_chat = chat_history[-1]

        retrieval_query = f"""
    Previous Question:
    {last_chat['user']}

    Current Question:
    {question}
    """
        
    # ========================= Temp: Retrieve Relevant Chunks =========================
    print("\nRETRIEVAL QUERY:")
    print(retrieval_query)

    '''
        We are passing retrieval_query to embedding model [Here ChromaDB] to get the embedding of the question along with the previous question (if exists).
        User:
            What is the STOP principle?
                History save ho gayi.

            Ab user:
                Tell me about point number S

            Retriever ko actually ye milega:

                Previous Question:
                What is the STOP principle?

                Current Question:
                Tell me about point number S
        
    This technique is called "History-Aware Retrieval". Isse kya hota hai ki retriever ko current question ke sath sath previous question ka context bhi mil jata hai, jisse wo zyada relevant chunks retrieve kar pata hai.
    '''
    # ========================= Temp: Retrieve Relevant Chunks =========================

    query_embedding = embedding_model.embed_query(
        retrieval_query
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

    docs = results["documents"][0]
    metadata = results["metadatas"][0]

    print("\nSOURCES RETRIEVED:")

    for m in metadata:
        print( m["source"], "Page", m["page"])

    print("\nSOURCES EXTRACTED:")

    history_text = "" # This chat history will be sent to the model [Here Ollama] as part of the prompt so that it can generate answer based on that history as well. This is useful in case of follow-up questions.

    for chat in chat_history:
        history_text += (
            f"User: {chat['user']}\n"
            f"Assistant: {chat['assistant']}\n\n"
        )

    #context = "\n\n".join(docs[:2])
    #  ================= Temp: just to check how much context we are sending to the model =================
    print("\nRETRIEVED DOCS:")
    for i, doc in enumerate(docs):
        print(f"\n--- DOC {i+1} ---")
        print(doc[:300])
    #  ================= Temp: just to check how much context we are sending to the model =================
    #context = "\n\n".join(docs)    
    context = "\n\n".join(docs[:3]) # just to limit the context size for now. Baad mein dynamic karenge based on token limit of the model.
    
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

    print("=" * 50)
    print("QUESTION:", question)
    print("DOCS FOUND:", len(docs)) # i have define n_results=2 that's why it will return max 2 docs
    print("CONTEXT LENGTH:", len(context)) # just to check how much context we are sending to the model
    print("=" * 50)

    response = llm.invoke(prompt)

    chat_history.append(
        {
            "user": question,
            "assistant": response.content
        }
    )

    if len(chat_history) > MAX_HISTORY:
        chat_history.pop(0)

    # ======== Make sources unique ========
    seen = set()
    unique_sources = []

    for source in metadata:

        key = (
            source["source"],
            source["page"]
        )

        if key not in seen:
            seen.add(key)
            unique_sources.append(source)
    # =====================================

    return {
        "answer": response.content,
        "sources": unique_sources
    }


def stream_answer(question):

    retrieval_query = question

    if len(chat_history) > 0:

        last_chat = chat_history[-1]

        retrieval_query = f"""
Previous Question:
{last_chat['user']}

Current Question:
{question}
"""

    query_embedding = embedding_model.embed_query(
        retrieval_query
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

    docs = results["documents"][0]
    metadata = results["metadatas"][0]

    history_text = ""

    for chat in chat_history:

        history_text += (
            f"User: {chat['user']}\n"
            f"Assistant: {chat['assistant']}\n\n"
        )

    context = "\n\n".join(docs[:3])

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

    full_response = ""

    for chunk in llm.stream(prompt):

        if chunk.content:

            full_response += chunk.content

            yield chunk.content

    chat_history.append(
        {
            "user": question,
            "assistant": full_response
        }
    )

    if len(chat_history) > MAX_HISTORY:
        chat_history.pop(0)

    seen = set()
    unique_sources = []

    for source in metadata:

        key = (
            source["source"],
            source["page"]
        )

        if key not in seen:
            seen.add(key)
            unique_sources.append(source)

    stream_answer.last_sources = unique_sources

    yield "__END_STREAM__"