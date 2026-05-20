// npm install express cors langchain @langchain/ollama

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

// Config
const MAX_MESSAGES_PER_USER = 2; // Max messages per user in the time window
const WINDOW_MS = 60 * 60 * 1000; // 1 hour

function getUserId(req) {
    return (
        req.headers["x-user-id"] ||
        req.body?.userId ||
        req.query?.userId ||
        req.ip
    );
}

function chatLimitMiddleware(req, res, next) {
    const userId = getUserId(req);
    const now = Date.now();

    if (!userId) {
        return res.status(400).json({ error: "User ID is required" });
    }

    const existing = userMessageUsage.get(userId);

    if (!existing) {
        userMessageUsage.set(userId, {
            count: 1,
            windowStart: now,
        });
        req.userId = userId;
        return next();
    }

    const isWindowExpired = now - existing.windowStart > WINDOW_MS;

    if (isWindowExpired) {
        userMessageUsage.set(userId, {
            count: 1,
            windowStart: now,
        });
        req.userId = userId;
        return next();
    }

    if (existing.count >= MAX_MESSAGES_PER_USER) {
        return res.status(429).json({
            error: "Chat limit exceeded for this user",
            userId,
            limit: MAX_MESSAGES_PER_USER,
            windowMs: WINDOW_MS,
        });
    }

    existing.count += 1;
    userMessageUsage.set(userId, existing);

    req.userId = userId;
    next();
}

// Apply chat limit on both endpoints
app.post("/chat-stream", chatLimitMiddleware, async (req, res) => {
    try {
        const message = req.body?.message || "What about Bhadohi?";

        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.setHeader("Transfer-Encoding", "chunked");

        const stream = await llm.stream(message);

        for await (const chunk of stream) {
            process.stdout.write(chunk.text);
            res.write(chunk.text);
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

app.get("/chat-sse", chatLimitMiddleware, async (req, res) => {
    try {
        const message = req.query.message || "What about Bhadohi?";

        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");

        const stream = await llm.stream(message);

        for await (const chunk of stream) {
            process.stdout.write(chunk.text);
            res.write(`data: ${JSON.stringify({ text: chunk.text })}\n\n`);
        }

        res.write(`data: ${JSON.stringify({ done: true })}\n\n`);
        res.end();
    } catch (error) {
        console.error(error);

        if (!res.headersSent) {
            res.write(`data: ${JSON.stringify({ error: "Streaming failed" })}\n\n`);
        }

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