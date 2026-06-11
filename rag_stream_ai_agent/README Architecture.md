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


### 4. Phase wise:
Phase 1
   ✅ Basic RAG:
         PDF Upload
         Chunking
         Embeddings
         ChromaDB
         Retrieval
         LLM Answer

Phase 2
   ✅ Better RAG:
         Multi-PDF
         Streaming Response
         Source Citation
         Chat History

Phase 3

   ✅ Agentic AI:
         Calculator Tool
         Web Search Tool
         RAG Tool
         Tool Selection
         Follow-up Query Handling

### 4.1 Pending:

Phase 4

   ✅ MCP (Model Context Protocol)