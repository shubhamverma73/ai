# pip install fastapi uvicorn langserve langchain langchain-ollama

from fastapi import FastAPI
from langserve import add_routes
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

app = FastAPI(
    title="Simple Chatbot Chain",
    version="1.0",
    description="LangServe demo with a simple chatbot chain"
)

llm = ChatOllama(
    base_url="http://localhost:11434",
    model="llama3:8b",
    temperature=0.7,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Reply in simple Hindi."),
    ("human", "{message}")
])

chain = prompt | llm

add_routes(
    app,
    chain,
    path="/chatbot"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)