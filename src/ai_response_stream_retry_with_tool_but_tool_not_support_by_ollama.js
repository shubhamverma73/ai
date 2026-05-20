// npm install express cors langchain @langchain/ollama zod

import express from "express";
import cors from "cors";
import { z } from "zod";
import { ChatOllama } from "@langchain/ollama";
import {
    createAgent,
    tool,
    HumanMessage,
} from "langchain";
import { modelRetryMiddleware } from "@langchain/langchain/agents/middleware";

const app = express();
app.use(cors());
app.use(express.json());

app.options("/{*any}", cors());

const llm = new ChatOllama({
    baseUrl: "http://localhost:11434",
    model: "llama3:8b",
    temperature: 0.7,
});

// Demo tool
const weatherTool = tool(
    async ({ city }) => {
        return `${city} ka weather garam ho sakta hai. Ye demo tool response hai.`;
    },
    {
        name: "weather_tool",
        description: "Kisi city ka demo weather batata hai",
        schema: z.object({
            city: z.string().describe("City name"),
        }),
    }
);

// Tool call limiter
const limiter = modelRetryMiddleware({
    maxRetries: 3,
    backoffFactor: 2.0,
    initialDelayMs: 1000,
});

// Agent
const agent = createAgent({
    model: llm,
    tools: [weatherTool],
    middleware: [limiter],
});

function getUserId(req) {
    return (
        req.headers["x-user-id"] ||
        req.body?.userId ||
        req.query?.userId ||
        "guest_user"
    );
}

// Plain text streaming endpoint
app.post("/chat-stream", async (req, res) => {
    try {
        const message = req.body?.message || "What about Bhadohi?";
        const userId = getUserId(req);

        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.setHeader("Transfer-Encoding", "chunked");

        const stream = await agent.stream(
            {
                messages: [new HumanMessage(message)],
            },
            {
                streamMode: "values",
                configurable: {
                    thread_id: userId,
                },
            }
        );

        let lastSentText = "";

        for await (const chunk of stream) {
            const lastMessage = chunk.messages?.[chunk.messages.length - 1];
            const text =
                typeof lastMessage?.content === "string"
                    ? lastMessage.content
                    : Array.isArray(lastMessage?.content)
                        ? lastMessage.content
                            .map((item) =>
                                typeof item === "string" ? item : item?.text || ""
                            )
                            .join("")
                        : "";

            if (text && text !== lastSentText) {
                const newText = text.slice(lastSentText.length);
                lastSentText = text;
                process.stdout.write(newText);
                res.write(newText);
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

// SSE endpoint
app.get("/chat-sse", async (req, res) => {
    try {
        const message = req.query.message || "What about Bhadohi?";
        const userId = getUserId(req);

        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");

        const stream = await agent.stream(
            {
                messages: [new HumanMessage(String(message))],
            },
            {
                streamMode: "values",
                configurable: {
                    thread_id: userId,
                },
            }
        );

        let lastSentText = "";

        for await (const chunk of stream) {
            const lastMessage = chunk.messages?.[chunk.messages.length - 1];
            const text =
                typeof lastMessage?.content === "string"
                    ? lastMessage.content
                    : Array.isArray(lastMessage?.content)
                        ? lastMessage.content
                            .map((item) =>
                                typeof item === "string" ? item : item?.text || ""
                            )
                            .join("")
                        : "";

            if (text && text !== lastSentText) {
                const newText = text.slice(lastSentText.length);
                lastSentText = text;
                process.stdout.write(newText);
                res.write(`data: ${JSON.stringify({ text: newText })}\n\n`);
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