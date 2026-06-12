## Current architecture:

Calculator
  ↓
Start Server
  ↓
Handshake
  ↓
Call Tool
  ↓
Shutdown

### 1. Future architecture:

```
Windows Start
    ↓
python app.py
    ↓
MCP Server Start (Once)
    ↓
MCP Session Initialize (Once)
    ↓
Alive
    ↓
Alive
    ↓
Alive

User Query 1
    ↓
Tool Call

User Query 2
    ↓
Tool Call

User Query 3
    ↓
Tool Call

Application Close
    ↓
MCP Shutdown

```

### 2. Stage 1 — MCP Manager:
```
mcp_client/
│
├── manager.py
├── client.py

```

### 3. Stage 2 — Manager will handle:
```
start()
call_tool()
stop()

```

### 4. Auto Reconnect:
```
Connection Lost
    ↓
Reconnect
    ↓
Continue

```

### 5. Startup Diagnostics:
```
[MCP] Starting...
[MCP] Connected
[MCP] Tools Loaded:
      calculator
      rag_search
      web_search
```

### manager.py file role:
```
1. Start MCP Server
2. Create Session
3. Reuse Session
4. Call Tools
5. Stop Session
```

### Final folder structure:
```
rag_stream_ai_agent_with_mcp_server/

│
├── app.py

│
├── agent.py

│
├── tools/
│   ├── calculator_tool.py
│   ├── rag_tool.py
│   └── web_search_tool.py

│
├── mcp_server/
│   └── server.py

│
└── mcp_client/
    ├── manager.py      <-- NEW
    └── client.py
```