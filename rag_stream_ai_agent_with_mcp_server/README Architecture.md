## Current architecture:

User
 ↓
Agent
 ↓
Calculator Tool
Web Search Tool
RAG Tool
 ↓
Answer

### ---------- Using Script -------------
Agent
   ↓
decide_tool()
   ↓
calculator_tool()
rag_tool()
web_search_tool()

---

### 1. Future architecture:

```
User
 ↓
LLM
 ↓
MCP Client
 ↓
MCP Server
 ↓
Tools

```

### 2. Stage 1 — MCP Server:
```
rag_stream_ai_agent_with_mcp_server/
│
├── app.py
├── agent.py
├── ingest.py
│
├── tools/
│   ├── rag_tool.py
│   ├── calculator_tool.py
│   └── web_search_tool.py
│
├── mcp_server/
│   ├── server.py
│   └── requirements.txt

```

### 3. Stage 2 — MCP Client:
```
rag_stream_ai_agent_with_mcp_server/
│
├── mcp_server/
│   └── server.py
│
├── mcp_client/
│   └── client.py
```

### 4. Final Arcitecture:
```
User
  ↓
Agent
  ↓
MCP Client
  ↓
MCP Server
      ├── Calculator
      ├── Web Search
      └── RAG Search

```

### 5. MCP Journey:
```
Step 1:
Add MCP Server

Step 2:
Expose Calculator Tool

Step 3:
Expose RAG Tool

Step 4:
Expose Web Search Tool

Step 5:
Convert Agent → MCP Client
```

### Old Calculator Flow
```
Browser
  ↓
Agent
  ↓
calculator_tool()
```

### New Calculator Flow
```
Browser
  ↓
Agent
  ↓
asyncio.run()
  ↓
call_tool()
  ↓
stdio_client()
  ↓
Launch New Python Process
  ↓
python mcp_server/server.py
  ↓
Import all modules
  ↓
Create MCP Session
  ↓
Handshake
  ↓
Call Tool
  ↓
calculator_tool()
  ↓
Return Result
  ↓
Close Session
  ↓
Kill Process
```