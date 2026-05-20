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

// In-memory user usage store
const userMessageUsage = new Map();
const MAX_MESSAGES_PER_USER = 2; // Max messages per user in the time window

app.post("/chat-stream", async (req, res) => {
	try {
		const message = req.body?.message || "What about Bhadohi?";
		const userId = req.body?.userId || "user_101";
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


app.get("/chat-sse", async (req, res) => {
	try {
		console.log("SSE route hit");
		const message = req.query.message || "What about Bhadohi?";
		const userId = req.body?.userId || "user_101";

		res.setHeader("Content-Type", "text/event-stream"); // SSE content type
		res.setHeader("Cache-Control", "no-cache");
		res.setHeader("Connection", "keep-alive");

		const stream = await llm.stream(message);

		for await (const chunk of stream) {
			process.stdout.write(chunk.text);
			res.write(`data: ${JSON.stringify({ text: chunk.text })}\n\n`); // Send each chunk as an SSE message so here \n\n is important to denote end of message.
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