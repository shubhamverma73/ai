## Current architecture

app.py
   ↓
rag.py
   ↓
Chroma

---

### 1. Future architecture

```text
app.py
   ↓
agent.py
   ↓
 ┌───────────────┐
 │ RAG Tool      │
 │ Web Tool      │
 │ Calculator    │
 └───────────────┘
   ↓
Answer

```

### 2. Based on Prompt and RAG response tool call approach
```
   Question
    ↓
   RAG Tool
    ↓
   Found?
 ┌───────────┐
 │ Yes       │
 └─────┬─────┘
       ↓
    Answer

 ┌───────────┐
 │ No        │
 └─────┬─────┘
       ↓
   Web Search
       ↓
   Answer

```

### 2. LLM Query Rewrite Scenario
```
Question
   ↓
Follow-Up Detection
   ↓
LLM Query Rewrite
   ↓
Distance Router
   ↓
RAG / Web

```

### 3. We have practically implemented all of this:
```
✅ PDF Ingestion
✅ Chunking Strategy
✅ Embeddings
✅ Vector DB (Chroma Cloud)
✅ Similarity Search
✅ Source Citation
✅ Multi-PDF Retrieval
✅ Chat History
✅ History-Aware Retrieval
✅ Streaming Responses
✅ Tool Calling
✅ Agent Routing
✅ Calculator Tool
✅ Web Search Tool
✅ Distance-Based Routing
✅ Query Rewriting for Follow-Ups
```