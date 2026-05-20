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

// NEW: system prompt added
const SYSTEM_PROMPT = `
You are a helpful AI assistant.
Rules:
1. Reply in simple Hindi.
2. Keep answers clear and practical.
3. If user asks for current weather, current date, or real-time info and you do not actually know it, do not guess.
4. If something is uncertain, say it clearly.
5. Use short examples when helpful.
`;

app.post("/chat-stream", async (req, res) => {
    try {
        const message = req.body?.message || "What about Bhadohi?";

        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.setHeader("Transfer-Encoding", "chunked");

        // CHANGED: direct string ki jagah system + human messages bheje gaye
        const stream = await llm.stream([
            ["system", SYSTEM_PROMPT],
            ["human", message],
        ]);

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

app.get("/chat-sse", async (req, res) => {
    try {
        const message = req.query.message || "What about Bhadohi?";

        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");

        // CHANGED: direct string ki jagah system + human messages bheje gaye
        const stream = await llm.stream([
            ["system", SYSTEM_PROMPT],
            ["human", message],
        ]);

        for await (const chunk of stream) {
            process.stdout.write(chunk.text);
            res.write(`data: ${JSON.stringify({ text: chunk.text })}\n\n`);
        }

        res.write(`data: ${JSON.stringify({ done: true })}\n\n`);
        res.end();
    } catch (error) {
        console.error(error);
        res.write(`data: ${JSON.stringify({ error: "Streaming failed" })}\n\n`);
        res.end();
    }
});

app.listen(5000, () => {
    console.log("Server running on http://localhost:5000");
});