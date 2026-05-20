// npm install express cors langchain @langchain/ollama dotenv
// url for access langsmith: https://smith.langchain.com/o/bd23228e-ae1a-4528-aa87-14ef24b805f7

import "dotenv/config";
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

// In-memory user usage store
const userMessageUsage = new Map();
const MAX_MESSAGES_PER_USER = 2;

function getUserId(req) {
    return (
        req.headers["x-user-id"] ||
        req.body?.userId ||
        req.query?.userId ||
        "user_101"
    );
}

app.post("/chat-stream", async (req, res) => {
    try {
        const message = req.body?.message || "What about Bhadohi?";
        const userId = getUserId(req);

        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.setHeader("Transfer-Encoding", "chunked");

        const stream = await llm.stream(message, {
            runName: "chat-stream",
            tags: ["chat", "stream", "ollama"],
            metadata: {
                endpoint: "/chat-stream",
                userId,
                transport: "fetch-stream",
            },
        });

        for await (const chunk of stream) {
            const text = chunk.text || "";
            process.stdout.write(text);
            res.write(text);
        }

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
        console.log("SSE route hit");

        const message = req.query.message || "What about Bhadohi?";
        const userId = getUserId(req);

        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");
        res.setHeader("Access-Control-Allow-Origin", "*");

        if (res.flushHeaders) {
            res.flushHeaders();
        }

        const stream = await llm.stream(message, {
            runName: "chat-sse",
            tags: ["chat", "sse", "ollama"],
            metadata: {
                endpoint: "/chat-sse",
                userId,
                transport: "eventsource",
            },
        });

        for await (const chunk of stream) {
            const text = chunk.text || "";
            process.stdout.write(text);
            res.write(`data: ${JSON.stringify({ text })}\n\n`);
        }

        res.write(`data: ${JSON.stringify({ done: true })}\n\n`);
        res.end();
    } catch (error) {
        console.error(error);
        res.write(`data: ${JSON.stringify({ error: "Streaming failed" })}\n\n`);
        res.end();
    }
});

app.get("/usage/:userId", (req, res) => {
    const userId = req.params.userId;
    const data = userMessageUsage.get(userId);

    if (!data) {
        return res.json({
            userId,
            count: 0,
            limit: MAX_MESSAGES_PER_USER,
            remaining: MAX_MESSAGES_PER_USER,
        });
    }

    return res.json({
        userId,
        count: data.count,
        limit: MAX_MESSAGES_PER_USER,
        remaining: Math.max(0, MAX_MESSAGES_PER_USER - data.count),
        windowStart: data.windowStart,
    });
});

app.listen(5000, () => {
    console.log("Server running on http://localhost:5000");
});