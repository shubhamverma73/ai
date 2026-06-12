# 🚀 RAG Stream

A Retrieval-Augmented Generation (RAG) application built with Python, Flask, ChromaDB, Sentence Transformers, and Ollama.

This project demonstrates how to build a basic RAG pipeline that can ingest PDF documents, store embeddings in a vector database, retrieve relevant context, and generate answers using an LLM.

---

## 📌 Features

* PDF Ingestion
* Document Chunking
* Embedding Generation
* ChromaDB Vector Storage
* Semantic Search
* Context Retrieval
* Ollama Integration
* Streaming Responses
* Flask Web Interface

---

## 📂 Project Structure

```text
rag_stream/
│
├── app.py
├── ingest.py
├── rag.py
├── requirements.txt
├── .env
│
├── data/
│   └── pdf_files/
│
├── chroma/
│   └── vector_db/
│
├── templates/
│   └── index.html
│
└── static/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository_url>
cd rag_stream
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📄 Add Documents

Place your PDF files inside:

```text
data/
```

Run ingestion:

```bash
python ingest.py
```

---

## ▶️ Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🏗️ Architecture

```text
User
 │
 ▼
Flask App
 │
 ▼
Retriever
 │
 ▼
ChromaDB
 │
 ▼
Relevant Chunks
 │
 ▼
Ollama LLM
 │
 ▼
Final Answer
```

---

## 🎯 Learning Objectives

This project helps understand:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Embeddings
* Semantic Search
* Context Injection
* LLM Integration

---

## 📜 License

This project is intended for learning and experimentation purposes.
