# pip install fastapi uvicorn langserve sse-starlette langchain langchain-ollama

from fastapi import FastAPI

from langserve import add_routes

from langchain_ollama import ChatOllama


# Create Model
llm = ChatOllama(
    model="llama3:8b",
    temperature=0.7
)


# Create FastAPI App
app = FastAPI(
    title="AI Chatbot API",
    version="1.0",
    description="LangServe + Ollama API"
)


# Convert LLM into API
add_routes(
    app,
    llm,
    path="/chat"
)

# Run with: uvicorn chatbot:app --reload

# Server Start
#   INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

# Automatically Generated APIs
'''LangServe automatically ये endpoints बना देगा:
    /chat/invoke
    /chat/stream
    /chat/batch
    /chat/playground
    /chat/input_schema
    /chat/output_schema'''

'''Chat Playground UI
    Browser में open करें:
    http://127.0.0.1:8000/chat/playground'''


'''API Example
    POST Request
    POST http://127.0.0.1:8000/chat/invoke'''

'''Response
    {
    "output": {
        "content": "A closure in JavaScript is..."
    }
    }'''


'''Main Benefit of LangServe:
    Without LangServe:
        @app.post("/chat")
        सब manually बनाना पड़ता।

    लेकिन LangServe में:
        add_routes(app, llm, path="/chat")
        और automatically:
            APIs
            Validation
            Streaming
            Playground
            Schemas
        सब मिल जाता है।'''