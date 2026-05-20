// npm install express langchain @langchain/ollama

import express from "express";
import cors from "cors";
import { ChatOllama } from "@langchain/ollama";

const app = express();
app.use(cors());
app.use(express.json());

app.options("/{*any}", cors());

const llm = new ChatOllama({
    baseUrl: "http://localhost:11434",
    model: "llama3:8b",
    temperature: 0.7,
});

// NEW: system prompt
const SYSTEM_PROMPT = `
You are a helpful AI assistant.
Reply in simple Hindi.
Keep answers clear and practical.
`;

// NEW: in-memory chat history store
// Example structure:
// {
//   "user1": [
//     ["human", "mera naam Rahul hai"],
//     ["assistant", "Theek hai, main yaad rakhunga."]
//   ]
// }
const chatSessions = {};

// NEW: helper to get/create session history
function getSessionHistory(sessionId) {
    if (!chatSessions[sessionId]) {
        chatSessions[sessionId] = [];
    }
    return chatSessions[sessionId];
}

// NEW: optional history limit
function trimHistory(history, maxMessages = 10) {
    if (history.length > maxMessages) {
        return history.slice(-maxMessages);
    }
    return history;
}

app.post("/chat-stream", async (req, res) => {
    try {
        const message = req.body?.message || "What about Bhadohi?";
        const sessionId = req.body?.sessionId || "default";

        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.setHeader("Transfer-Encoding", "chunked");

        const history = getSessionHistory(sessionId);

        // NEW: build full message list with system + old history + current user message
        const messages = [
            ["system", SYSTEM_PROMPT],
            ...trimHistory(history),
            ["human", message],
        ];

        const stream = await llm.stream(messages);

        let fullResponse = "";

        for await (const chunk of stream) {
            process.stdout.write(chunk.text);
            res.write(chunk.text);
            fullResponse += chunk.text;
        }

        // NEW: save user + assistant messages in session history
        history.push(["human", message]);
        history.push(["assistant", fullResponse]);

        res.end();
    } catch (error) {
        console.error(error);
        if (!res.headersSent) {
            res.status(500).json({ error: "Something went wrong" });
        } else {
            res.end("\n[ERROR]");
        }
    }
});

app.get("/chat-sse", async (req, res) => {
    try {
        const message = req.query.message || "What about Bhadohi?";
        const sessionId = req.query.sessionId || "default";

        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");

        const history = getSessionHistory(sessionId);

        // NEW: build full message list with system + old history + current user message
        const messages = [
            ["system", SYSTEM_PROMPT],
            ...trimHistory(history),
            ["human", message],
        ];

        const stream = await llm.stream(messages);

        let fullResponse = "";

        for await (const chunk of stream) {
            process.stdout.write(chunk.text);
            res.write(`data: ${JSON.stringify({ text: chunk.text })}\n\n`);
            fullResponse += chunk.text;
        }

        // NEW: save user + assistant messages in session history
        history.push(["human", message]);
        history.push(["assistant", fullResponse]);

        res.write(`data: ${JSON.stringify({ done: true })}\n\n`);
        res.end();
    } catch (error) {
        console.error(error);
        res.write(`data: ${JSON.stringify({ error: "Streaming failed" })}\n\n`);
        res.end();
    }
});

// NEW: clear a session history manually
app.post("/clear-chat", (req, res) => {
    const sessionId = req.body?.sessionId || "default";
    chatSessions[sessionId] = [];
    res.json({ success: true, message: `Chat history cleared for session: ${sessionId}` });
});

app.listen(5000, () => {
    console.log("Server running on http://localhost:5000");
});