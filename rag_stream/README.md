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