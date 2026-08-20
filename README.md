# Open AI Learning Repository

This repository is a hands-on collection of AI and LLM experiments built using Node.js, Python, LangChain, LangGraph, Ollama, and Retrieval-Augmented Generation (RAG) patterns. It includes practical examples for learning how modern AI applications are built and how local models are integrated into web and backend workflows.

---

## Overview

The project contains:

- Node.js examples for LangChain and Ollama
- Streaming AI response demos
- LangGraph workflow examples
- LangSmith tracing setup
- Python-based AI and NLP experiments
- RAG projects with ChromaDB and Flask
- Spam detection, language model training, and transformer experiments

---

## Technologies Used

- Node.js
- JavaScript / ES Modules
- LangChain
- LangGraph
- Ollama
- Express
- ChromaDB
- Python
- Flask
- TensorFlow / Keras
- LangSmith (for tracing and debugging)
- OpenAI-compatible AI workflows

---

## Repository Structure

```bash
open_ai/
├── README.md
├── package.json
├── package-lock.json
├── .gitignore
├── src/
│   ├── index.js
│   ├── ai_response_invoke.js
│   ├── ai_response_stream.js
│   ├── ai_response_stream_langsmith.js
│   ├── ai_response_invoke_langgraph.js
│   ├── ai_response_stream_memory_saver.js
│   ├── ai_response_stream_with_tool.js
│   ├── ai_response_stream_offline_tool.js
│   ├── html/
│   ├── css/
│   └── embadding/
├── rag/
│   ├── app.py
│   ├── rag.py
│   ├── ingest.py
│   ├── templates/
│   ├── static/
│   ├── data/
│   ├── venv/
│   └── README.md
├── rag_stream/
├── rag_stream_ai_agent/
├── rag_stream_ai_agent_mcp_alive_server/
├── rag_stream_ai_agent_with_mcp_server/
├── mini_nlp_model/
├── mini_nlp_model_lstm/
├── mini_nlp_model_updated/
├── mini_nlp_spam/
├── mini_transformer_model/
├── python/
└── node_modules/
```

---

## Main Areas of the Project

### 1. Node.js AI Examples
The `src/` folder contains examples for:

- basic LLM invocation
- streaming responses
- tool use and middleware
- memory handling
- LangGraph stateful flows
- LangSmith integration
- simple HTML/JS UI examples

### 2. RAG Projects
The `rag/` folder includes a document-based chatbot using:

- Flask
- LangChain
- ChromaDB
- PDF ingestion
- embeddings and retrieval
- LLM response generation

### 3. NLP and ML Experiments
The repo also includes Python projects such as:

- spam detection
- small language model training
- model prediction scripts
- transformer-based examples

---

## Prerequisites

Before running the project, make sure you have:

- Node.js 18+
- npm
- Python 3.10+
- Ollama installed and running locally

You may also need models such as:

```bash
ollama pull llama3:8b
ollama pull nomic-embed-text
```

---

## Setup

### Install Node dependencies

```bash
cd d:\xampp\htdocs\node\open_ai
npm install
```

### Install Python dependencies for RAG

```bash
cd d:\xampp\htdocs\node\open_ai\rag
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Run Examples

### Basic Node example

```bash
cd d:\xampp\htdocs\node\open_ai
node src/index.js
```

### Streaming response example

```bash
cd d:\xampp\htdocs\node\open_ai
node src/ai_response_stream.js
```

### LangGraph example

```bash
cd d:\xampp\htdocs\node\open_ai
node src/ai_response_invoke_langgraph.js
```

### RAG app

```bash
cd d:\xampp\htdocs\node\open_ai\rag
python app.py
```

Then open in browser:

```text
http://127.0.0.1:5000
```

---

## Environment Variables

Some examples use environment variables for tracing or API configuration. Check files such as `.ENV` and any local `.env` files before running them.

Example:

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_key_here
LANGSMITH_PROJECT=your_project_name
```

---

## Learning Goals

This repository is intended to help learn:

- LLM integration in JavaScript projects
- prompt engineering
- tool calling and agent workflows
- streaming responses
- retrieval-augmented generation
- graph-based orchestration with LangGraph
- debugging and monitoring with LangSmith
- NLP and model experimentation in Python

---

## Notes

This is a learning and experimentation repository, not a production-ready app. Many files are sample demos created to understand AI concepts in a practical way.

---

## Recommended Order to Explore

1. `src/index.js`
2. `src/ai_response_stream.js`
3. `src/ai_response_stream_with_tool.js`
4. `src/ai_response_invoke_langgraph.js`
5. `src/ai_response_stream_langsmith.js`
6. `rag/`
7. `mini_nlp_spam/`
8. Python model experiments in `mini_nlp_model*`

---

## License

This repository is used for learning and educational experimentation.
