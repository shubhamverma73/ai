# Execution Order

## Step 1: Store PDF in Chroma Database

Run the following command:

```bash
python ingest.py
```

**Expected Output:**

```text
PDF stored successfully!
```

---

## Step 2: Start the Flask Server

Run:

```bash
python app.py
```

**Expected Output:**

```text
Running on:
http://127.0.0.1:5000
```

---

## Step 3: Open the Application

Open the following URL in your browser:

```text
http://127.0.0.1:5000
```

---

## Step 4: Ask a Question

Example:

```text
What is leave policy?
```

---

## How It Works

```text
User (Browser)
      │
      ▼
    Flask
      │
      ▼
    rag.py
      │
      ▼
 Chroma DB
      │
      ▼
   Ollama
      │
      ▼
   Answer
      │
      ▼
 User (Browser)
```

---

## Workflow Summary

1. Store PDF documents in Chroma using `ingest.py`
2. Start the Flask application using `app.py`
3. Open the web interface in your browser
4. Ask questions about the uploaded PDF
5. The system retrieves relevant content from Chroma and generates answers using Ollama

---
##  FULL DETAILS
---
# PDF RAG Chatbot with Streaming

A Retrieval-Augmented Generation (RAG) chatbot built using Flask, LangChain, ChromaDB Cloud, and Ollama.

The chatbot can:

* Chat with one or multiple PDF documents
* Retrieve relevant information from PDFs
* Show source citations
* Maintain chat memory
* Support history-aware retrieval
* Stream responses token-by-token
* Use ChromaDB Cloud for vector storage

---

# Features

✅ PDF Loading

✅ Multi-PDF Support

✅ Text Chunking

✅ Embeddings using Ollama

✅ ChromaDB Cloud Storage

✅ Retrieval-Augmented Generation (RAG)

✅ Source Citations

✅ Chat Memory (Last 5 Conversations)

✅ History-Aware Retrieval

✅ Streaming Responses

---

# Tech Stack

* Flask
* LangChain
* ChromaDB Cloud
* Ollama
* llama3:8b
* nomic-embed-text
* HTML
* CSS
* JavaScript

---

# Project Structure

```text
rag/
│
├── data/
│   └── pdfs/
│       ├── file1.pdf
│       └── file2.pdf
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── app.js
│
├── templates/
│   └── index.html
│
├── app.py
├── rag.py
├── ingest.py
├── requirements.txt
├── .env
└── README.md
```

---

# Clone Repository

```bash
git clone <YOUR_REPOSITORY_URL>

cd rag
```

---

# Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

CMD:

```bash
venv\Scripts\activate
```

Git Bash:

```bash
source venv/Scripts/activate
```

PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Install Ollama

Download:

https://ollama.com

Verify:

```bash
ollama --version
```

---

# Download Models

LLM:

```bash
ollama pull llama3:8b
```

Embedding Model:

```bash
ollama pull nomic-embed-text
```

Verify:

```bash
ollama list
```

Expected:

```text
llama3:8b
nomic-embed-text
```

---

# ChromaDB Cloud Setup

Create account:

https://www.trychroma.com

Create:

* Tenant
* Database

Copy:

* API Key
* Tenant ID
* Database Name

---

# Environment Variables

Create `.env`

```env
CHROMA_API_KEY=YOUR_API_KEY
CHROMA_TENANT=YOUR_TENANT
CHROMA_DATABASE=YOUR_DATABASE
```

---

# Add PDFs

Place PDFs inside:

```text
data/pdfs/
```

Example:

```text
data/pdfs/company_policy.pdf
data/pdfs/environment_policy.pdf
```

---

# Ingest PDFs

Run once after adding PDFs.

```bash
python ingest.py
```

This will:

* Load PDFs
* Chunk Documents
* Generate Embeddings
* Store Embeddings in ChromaDB

Expected:

```text
Loading: company_policy.pdf
Loading: environment_policy.pdf

Pages Loaded: XX
Chunks Created: XX

PDF stored successfully!
```

---

# Run Application

Start Flask server:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# Example Questions

```text
What is the company's top priority?

Explain the STOP principle.

How does the company contribute to environmental protection?

What are the employee safety guidelines?
```

---

# Current Capabilities

* Multi-PDF Retrieval
* Source Citations
* Streaming Responses
* Chat Memory
* History-Aware Retrieval

---

# Future Improvements

* Agentic RAG
* Hybrid Search
* Re-ranking
* User Authentication
* Conversation Persistence
* Citation Highlighting
* PDF Upload from UI

---

# Author

Shubham Verma
AI / Machine Learning Enthusiast
GitHub: https://github.com/<your-github-username>

```
```
