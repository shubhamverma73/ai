// npm install express langchain @langchain/ollama zod

import express from "express";
import cors from "cors";
import { ChatOllama } from "@langchain/ollama";

// ========================= NEWLY ADDED =========================
import { createAgent, tool } from "langchain";
import { z } from "zod";

const app = express();
app.use(cors());
app.use(express.json());

app.options("/{*any}", cors());

const llm = new ChatOllama({
    baseUrl: "http://localhost:11434",
    model: "llama3:8b",
    temperature: 0.7,
});


// ========================= NEWLY ADDED: real tool =========================
// Ye local system date/time tool hai. Koi online API use nahi ho rahi.
const dateTool = tool(
    async ({ query }) => {
        const now = new Date();

        const today = new Date(now);
        const yesterday = new Date(now);
        yesterday.setDate(now.getDate() - 1);

        const tomorrow = new Date(now);
        tomorrow.setDate(now.getDate() + 1);

        return JSON.stringify({
            query,
            now: now.toLocaleString("en-IN", { timeZone: "Asia/Kolkata" }),
            today: today.toLocaleDateString("en-IN", { timeZone: "Asia/Kolkata" }),
            yesterday: yesterday.toLocaleDateString("en-IN", { timeZone: "Asia/Kolkata" }),
            tomorrow: tomorrow.toLocaleDateString("en-IN", { timeZone: "Asia/Kolkata" }),
        });
    },
    {
        name: "date_tool",
        description: "Current date, time, today, yesterday aur tomorrow batane ke liye use karo.",
        schema: z.object({
            query: z.string().describe("User ka date/time related question"),
        }),
    }
);


// ========================= NEWLY ADDED: agent with tool =========================
const agent = createAgent({
    model: llm,
    tools: [dateTool],
});


app.post("/chat-stream", async (req, res) => {
    try {
        const message = req.body?.message || "What about Bhadohi?";

        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.setHeader("Transfer-Encoding", "chunked");

        // ========================= CHANGED =========================
        // llm.stream(message) ki jagah agent.stream(...) use ho raha hai
        const stream = await agent.stream({
            messages: [{ role: "user", content: message }],
        });

        // ========================= NEWLY ADDED =========================
        // agent.stream alag-alag event objects de sakta hai, isliye assistant text ko pick kar rahe hain
        for await (const chunk of stream) {
            const messages = chunk.messages || [];

            for (const msg of messages) {
                if (msg.role === "assistant" && typeof msg.content === "string") {
                    process.stdout.write(msg.content);
                    res.write(msg.content);
                }
            }
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

        res.setHeader("Content-Type", "text/event-stream"); // SSE content type
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");

        // ========================= CHANGED =========================
        const stream = await agent.stream({
            messages: [{ role: "user", content: message }],
        });

        // ========================= NEWLY ADDED =========================
        for await (const chunk of stream) {
            const messages = chunk.messages || [];

            for (const msg of messages) {
                if (msg.role === "assistant" && typeof msg.content === "string") {
                    process.stdout.write(msg.content);
                    res.write(`data: ${JSON.stringify({ text: msg.content })}\n\n`);
                }
            }
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