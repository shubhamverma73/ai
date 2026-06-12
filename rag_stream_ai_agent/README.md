# 🤖 RAG Stream AI Agent

An Agentic RAG system built using Python, Flask, ChromaDB, Ollama, and custom tools.

This project extends a traditional RAG pipeline by introducing an AI Agent capable of selecting the most appropriate tool to answer a user's question.

Instead of always using document retrieval, the agent can dynamically choose between:

* RAG Search
* Calculator Tool
* Web Search Tool

---

# 🚀 Features

## RAG Features

* PDF Ingestion
* Document Chunking
* Embeddings
* ChromaDB Vector Database
* Semantic Search
* Source Citation
* Streaming Responses

## Agent Features

* Tool Calling
* Dynamic Tool Selection
* Query Rewriting
* Follow-Up Question Detection
* Distance-Based Routing
* Multi-Turn Conversations

## Tools

* RAG Tool
* Calculator Tool
* Web Search Tool

---

# 📂 Project Structure

```text
rag_stream_ai_agent/
│
├── app.py
├── agent.py
├── ingest.py
├── requirements.txt
│
├── chroma/
│
├── data/
│
├── tools/
│   ├── rag_tool.py
│   ├── calculator_tool.py
│   └── web_search_tool.py
│
├── templates/
│   └── index.html
│
└── static/
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone <repository_url>
cd rag_stream_ai_agent
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📄 Ingest Documents

Place PDF files inside:

```text
data/
```

Run:

```bash
python ingest.py
```

This generates embeddings and stores them inside ChromaDB.

---

# ▶️ Run Application

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

# 🏗️ System Architecture

```text
User
 │
 ▼
 AI Agent
 │
 ▼
 Tool Decision
 │
 ├──────────────► Calculator Tool
 │
 ├──────────────► RAG Tool
 │
 └──────────────► Web Search Tool
 │
 ▼
 Response
```

---

# 🔄 Agent Workflow

```text
Question
 │
 ▼
 Follow-Up Detection
 │
 ▼
 Query Rewriting
 │
 ▼
 Distance Router
 │
 ├──────────────► RAG Search
 │
 └──────────────► Web Search
 │
 ▼
 Final Answer
```

---

# 🎯 Distance-Based Routing

The system measures semantic distance between the user query and the retrieved document chunks.

### Low Distance

```text
Distance <= Threshold
```

Agent uses:

```text
RAG Tool
```

### High Distance

```text
Distance > Threshold
```

Agent uses:

```text
Web Search Tool
```

This helps prevent hallucinations and improves answer quality.

---

# 🧠 Agent Capabilities

### Mathematical Questions

Example:

```text
What is 250 * 43?
```

Selected Tool:

```text
Calculator Tool
```

---

### Document Questions

Example:

```text
What are MTAR Technologies revenue sources?
```

Selected Tool:

```text
RAG Tool
```

---

### General Knowledge Questions

Example:

```text
Who is the current Prime Minister of India?
```

Selected Tool:

```text
Web Search Tool
```

---

# 📚 Learning Outcomes

This project teaches:

* Agentic AI
* Tool Calling
* RAG Pipelines
* Query Routing
* Semantic Similarity
* Multi-Turn Conversations
* LLM Orchestration

---

# 🔮 Future Improvements

* MCP Integration
* Multi-Agent Systems
* Memory Layer
* Hybrid Search
* Advanced Tool Registry
* Production Deployment

---

# 📜 License

This project is intended for learning and educational purposes.
