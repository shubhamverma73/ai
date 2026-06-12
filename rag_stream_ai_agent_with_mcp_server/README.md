# 🔥 RAG Stream AI Agent with MCP Server

A production-style Agentic RAG system built using Python, Flask, ChromaDB, Ollama, and the Model Context Protocol (MCP).

This project demonstrates how modern AI Agents can communicate with tools through MCP instead of directly calling Python functions.

The agent interacts with tools through an MCP Client and MCP Server architecture.

---

# 🚀 Features

## RAG Features

* PDF Ingestion
* Semantic Search
* ChromaDB
* Source Citation
* Streaming Responses

## Agent Features

* Tool Selection
* Follow-Up Detection
* Query Rewriting
* Distance Routing

## MCP Features

* MCP Server
* MCP Client
* Tool Exposure
* Async Tool Execution
* Standardized Tool Interface
* Extensible Tool Architecture

---

# 📂 Project Structure

```text
rag_stream_ai_agent_with_mcp_server/
│
├── app.py
├── agent.py
├── ingest.py
├── requirements.txt
│
├── mcp_client/
│   └── client.py
│
├── mcp_server/
│   └── server.py
│
├── tools/
│   ├── rag_tool.py
│   ├── calculator_tool.py
│   └── web_search_tool.py
│
├── chroma/
│
├── data/
│
├── templates/
│
└── static/
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone <repository_url>
cd rag_stream_ai_agent_with_mcp_server
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

# 📄 Load Documents

Place PDF files inside:

```text
data/
```

Run:

```bash
python ingest.py
```

---

# ▶️ Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 🏗️ MCP Architecture

```text
User
 │
 ▼
 Agent
 │
 ▼
 MCP Client
 │
 ▼
 MCP Server
 │
 ├──────────────► Calculator Tool
 │
 ├──────────────► RAG Tool
 │
 └──────────────► Web Search Tool
 │
 ▼
 Result
 │
 ▼
 Agent
 │
 ▼
 User
```

---

# 🔄 Request Lifecycle

```text
Browser Request
       │
       ▼
Flask Application
       │
       ▼
AI Agent
       │
       ▼
call_tool()
       │
       ▼
MCP Client
       │
       ▼
MCP Server
       │
       ▼
Tool Execution
       │
       ▼
Result Returned
       │
       ▼
Agent Response
       │
       ▼
Browser
```

---

# 🧩 MCP Components

## MCP Server

Responsibilities:

* Register Tools
* Expose Tools
* Execute Tool Calls
* Return Structured Results

---

## MCP Client

Responsibilities:

* Connect to MCP Server
* Send Requests
* Receive Results
* Provide Tool Interface to Agent

---

## AI Agent

Responsibilities:

* Understand User Intent
* Select Tool
* Process Results
* Generate Final Response

---

# 🎯 Why MCP?

Traditional Approach:

```text
Agent
  ↓
Direct Function Call
```

MCP Approach:

```text
Agent
  ↓
MCP Client
  ↓
MCP Server
  ↓
Tool
```

Benefits:

* Standardization
* Scalability
* Tool Reusability
* Cleaner Architecture
* Easier Integration

---

# 📚 Learning Outcomes

This project helps understand:

* Model Context Protocol (MCP)
* Client-Server Communication
* Tool Exposure
* Agent Architectures
* Async Python
* Production AI Design Patterns

---

# 🛣️ Roadmap

* Persistent MCP Connection Manager
* Tool Registry System
* Multiple MCP Servers
* Memory Layer
* Multi-Agent Architecture
* Production Deployment
* Observability & Logging

---

# 📈 Evolution Journey

```text
Project 1
Basic RAG
      │
      ▼
Project 2
Agentic RAG
      │
      ▼
Project 3
MCP-Based Agentic RAG
```

---

# 📜 License

This project is intended for learning, experimentation, and understanding modern AI application architecture.
