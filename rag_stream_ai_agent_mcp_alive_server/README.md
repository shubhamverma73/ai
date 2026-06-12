# Agentic RAG + MCP + SSE Transport

A production-style Agentic RAG application built using:

* Flask
* ChromaDB Cloud
* Ollama
* MCP (Model Context Protocol)
* SSE Transport
* Multi-source Retrieval (RAG + Web Search)
* Tool Routing Agent

---

# Features

## Calculator Tool

Supports:

* Addition
* Subtraction
* Multiplication
* Division
* Modulus
* Power
* Square Root

Examples:

```text
45 + 58
100 divided by 4
sqrt 81
square root of 81
```

---

## RAG Tool

Retrieves information from PDFs stored inside ChromaDB Cloud.

Features:

* Semantic Search
* Query Rewriting
* Follow-Up Question Handling
* Conversation Memory
* Source Tracking

---

## Web Search Tool

Searches the internet when information is not found in the vector database.

Features:

* DuckDuckGo Search
* Page Scraping
* Context Building
* LLM Summarization
* Source Collection

---

## Agent Router

Automatically decides which tool should be used.

Routing Flow:

```text
User Question
        ↓
   Agent Router
        ↓
 ┌──────────────┐
 │ Calculator   │
 │ RAG Search   │
 │ Web Search   │
 └──────────────┘
        ↓
     Response
```

---

# Architecture

```text
Browser
   ↓
Flask App
   ↓
Agent Router
   ↓
MCP Client
   ↓
MCP SSE Server
   ↓
Tools

Calculator Tool
RAG Tool
Web Search Tool
```

---

# Project Structure

```text
project/

│
├── app.py
├── agent.py
├── ingest.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── app.js
│
├── tools/
│   ├── calculator_tool.py
│   ├── rag_tool.py
│   └── web_search_tool.py
│
├── mcp_client/
│   └── client.py
│
├── mcp_server/
│   └── server.py
│
├── data/
│   └── pdfs/
│       ├── file1.pdf
│       ├── file2.pdf
│       └── ...
│
├── .env
├── requirements.txt
│
└── README.md
```

---

# MCP Architecture

Current implementation uses:

```text
SSE Transport
```

Flow:

```text
Flask
   ↓
Agent
   ↓
MCP Client
   ↓
SSE Connection
   ↓
MCP Server
   ↓
Tool Execution
```

---

# Implemented Stages

```text
✓ Stage 1
MCP Installation

✓ Stage 2
Calculator MCP Tool

✓ Stage 3
RAG MCP Tool

✓ Stage 4
Web Search MCP Tool

✓ Stage 5
SSE Transport

✗ Stage 6
Persistent Session Manager
(Deferred)

✗ Stage 7
Multi Tool Agent
(Future Enhancement)
```

---

# Environment Variables

Create:

```text
.env
```

Example:

```env
CHROMA_API_KEY=YOUR_KEY
CHROMA_TENANT=YOUR_TENANT
CHROMA_DATABASE=YOUR_DATABASE
```

---

# Install Dependencies

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Start Ollama

Pull model:

```bash
ollama pull llama3:8b
```

Pull embedding model:

```bash
ollama pull nomic-embed-text
```

Start Ollama:

```bash
ollama serve
```

Verify:

```bash
http://localhost:11434
```

---

# Load PDFs into Chroma

Place PDFs inside:

```text
data/pdfs/
```

Run:

```bash
python ingest.py
```

Flow:

```text
PDF
 ↓
Chunk
 ↓
Embedding
 ↓
ChromaDB Cloud
```

Run only when adding new PDFs.

---

# Start MCP Server

Open Terminal 1:

```bash
python mcp_server/server.py
```

Expected Output:

```text
Starting MCP SSE Server...
```

Server URL:

```text
http://127.0.0.1:8000/sse
```

---

# Start Flask Application

Open Terminal 2:

```bash
python app.py
```

Expected Output:

```text
Running on:

http://127.0.0.1:5000
```

Open browser:

```text
http://127.0.0.1:5000
```

---

# Runtime Flow

```text
Terminal 1

python mcp_server/server.py

       ↓

MCP SSE Server Running


--------------------------------


Terminal 2

python app.py

       ↓

Flask Running


--------------------------------


Browser

http://127.0.0.1:5000

       ↓

Ask Questions

       ↓

Agent Selects Tool

       ↓

MCP Executes Tool

       ↓

Answer Returned
```

---

# Example Questions

## Calculator

```text
45 + 79

sqrt 144

100 divided by 5
```

---

## RAG

```text
What is the company leave policy?

Explain the employee benefits.

What does the policy say about travel reimbursement?
```

---

## Follow-Up Questions

```text
What is the leave policy?

How many casual leaves?

What about sick leaves?
```

Agent automatically rewrites follow-up queries.

---

## Web Search

```text
Latest Nvidia stock news

Who won the IPL?

What is the latest version of Python?
```

If vector search confidence is low:

```text
Agent
 ↓
Web Search
```

---

# Future Improvements

## Stage 6

Persistent MCP Session

Status:

```text
Deferred
```

Reason:

```text
Flask + asyncio.run() architecture
is not compatible with long-lived
MCP SSE sessions without additional
event-loop management.
```

---

## Stage 7

Multi Tool Agent

Example:

```text
User Question
        ↓
RAG Search
        ↓
Need Latest Data?
        ↓
Web Search
        ↓
Combine Results
        ↓
Final Answer
```

---

# Tech Stack

* Python
* Flask
* ChromaDB Cloud
* Ollama
* LangChain
* MCP
* SSE
* DuckDuckGo Search
* BeautifulSoup
* HTML
* CSS
* JavaScript

---

# Author

Agentic RAG + MCP + SSE Learning Project

Built for understanding:

* RAG Systems
* MCP Architecture
* Tool Calling
* Agent Routing
* Vector Search
* Web Search Integration
* SSE Communication
