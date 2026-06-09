from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3:8b"
)

response = llm.invoke(
    "Hello"
)

print(response.content)