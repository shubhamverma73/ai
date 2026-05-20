// npm install express cors langchain @langchain/ollama

import express from "express";
import cors from "cors";
import { ChatOllama } from "@langchain/ollama";
import {
    createAgent,
    createMiddleware,
    HumanMessage,
    SystemMessage,
} from "langchain";

const app = express();
app.use(cors());
app.use(express.json());

app.options("/{*any}", cors());

const llm = new ChatOllama({
    baseUrl: "http://localhost:11434",
    model: "llama3:8b",
    temperature: 0.7,
});

// Middleware - only wrapModelCall, clean and correct
const customMiddleware = createMiddleware({
    name: "CustomPromptMiddleware",

    wrapModelCall: async (request, handler) => {
        const extraInstruction = new SystemMessage(`
You are a helpful AI assistant.
Rules:
1. Reply in simple Hindi.
2. Keep answers practical and clear.
3. If user asks about real-time info, do not guess.
4. Use short examples if needed.
5. Keep formatting neat.
`);

        return handler({
            ...request,
            systemMessage: request.systemMessage.concat(extraInstruction),
        });
    },
});

const agent = createAgent({
    model: llm,
    tools: [],
    systemPrompt: "You are a helpful assistant.",
    middleware: [customMiddleware],
});

// Plain text endpoint
app.post("/chat-stream", async (req, res) => {
    try {
        const message = req.body?.message || "What about Bhadohi?";

        res.setHeader("Content-Type", "text/plain; charset=utf-8");

        const result = await agent.invoke({
            messages: [new HumanMessage(message)],
        });

        const lastMessage = result.messages[result.messages.length - 1];
        const text =
            typeof lastMessage?.content === "string"
                ? lastMessage.content
                : Array.isArray(lastMessage?.content)
                ? lastMessage.content
                      .map((item) => (typeof item === "string" ? item : item?.text || ""))
                      .join("")
                : "";

        process.stdout.write(text);
        res.end(text);
    } catch (error) {
        console.error(error);
        if (!res.headersSent) {
            res.status(500).json({ error: "Something went wrong" });
        } else {
            res.end("\n[ERROR]");
        }
    }
});

// SSE endpoint
app.get("/chat-sse", async (req, res) => {
    try {
        const message = req.query.message || "What about Bhadohi?";

        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");

        const result = await agent.invoke({
            messages: [new HumanMessage(String(message))],
        });

        const lastMessage = result.messages[result.messages.length - 1];
        const text =
            typeof lastMessage?.content === "string"
                ? lastMessage.content
                : Array.isArray(lastMessage?.content)
                ? lastMessage.content
                      .map((item) => (typeof item === "string" ? item : item?.text || ""))
                      .join("")
                : "";

        process.stdout.write(text);
        res.write(`data: ${JSON.stringify({ text })}\n\n`);
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