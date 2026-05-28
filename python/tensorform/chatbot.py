# pip install langchain langchain-ollama

from langchain_ollama import ChatOllama


# Load Model
llm = ChatOllama(
    model="llama3:8b",
    temperature=0.7
)


# Ask Question
response = llm.invoke(
    "What is callback hell in JavaScript?"
)


# Print Response
print(response.content)