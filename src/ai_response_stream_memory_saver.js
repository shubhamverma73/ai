// npm install express cors @langchain/ollama @langchain/langgraph @langchain/core

import express from "express";
import cors from "cors";
import { ChatOllama } from "@langchain/ollama";
import { HumanMessage } from "@langchain/core/messages";
import {
    StateGraph,
    MessagesAnnotation,
    MemorySaver,
    START,
    END,
} from "@langchain/langgraph";

const app = express();
app.use(cors());
app.use(express.json());

const llm = new ChatOllama({
    baseUrl: "http://localhost:11434",
    model: "llama3:8b",
    temperature: 0.7,
});

function getUserId(req) {
    return (
        req.headers["x-user-id"] ||
        req.body?.userId ||
        req.query?.userId ||
        req.ip ||
        "guest_user"
    );
}

// Node: call model
async function callModel(state) {
    const response = await llm.invoke(state.messages);
    return { messages: [response] };
}

// Build graph
const workflow = new StateGraph(MessagesAnnotation)
    .addNode("agent", callModel)
    .addEdge(START, "agent")
    .addEdge("agent", END);

// MemorySaver: in-memory checkpoint store
const memory = new MemorySaver();

// Compile graph with memory
const graph = workflow.compile({
    checkpointer: memory,
});

// STREAM endpoint
app.post("/chat-stream", async (req, res) => {
    try {
        console.log("STREAM route hit");

        const message = req.body?.message || "Explain LangGraph simply";
        const userId = getUserId(req);

        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.setHeader("Transfer-Encoding", "chunked");

        const stream = await graph.stream(
            {
                messages: [new HumanMessage(message)],
            },
            {
                configurable: {
                    thread_id: String(userId),
                },
                streamMode: "values",
            }
        );

        let lastText = "";

        for await (const chunk of stream) {
            const lastMessage = chunk.messages?.[chunk.messages.length - 1];

            let text = "";
            if (typeof lastMessage?.content === "string") {
                text = lastMessage.content;
            } else if (Array.isArray(lastMessage?.content)) {
                text = lastMessage.content
                    .map((item) =>
                        typeof item === "string" ? item : item?.text || ""
                    )
                    .join("");
            }

            if (text && text !== lastText) {
                const delta = text.slice(lastText.length);
                lastText = text;
                res.write(delta);
            }
        }

        res.end();
    } catch (error) {
        console.error(error);
        if (!res.headersSent) {
            res.status(500).json({ error: "Streaming failed" });
        } else {
            res.end("\n[ERROR]");
        }
    }
});

// SSE endpoint
app.get("/chat-sse", async (req, res) => {
    try {
        console.log("SSE route hit");

        const message = req.query.message || "Explain LangGraph simply";
        const userId = getUserId(req);

        res.setHeader("Content-Type", "text/event-stream");
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");

        res.write(`data: ${JSON.stringify({ text: "SSE started" })}\n\n`);

        const stream = await graph.stream(
            {
                messages: [new HumanMessage(String(message))],
            },
            {
                configurable: {
                    thread_id: String(userId),
                },
                streamMode: "values",
            }
        );

        let lastText = "";

        for await (const chunk of stream) {
            const lastMessage = chunk.messages?.[chunk.messages.length - 1];

            let text = "";
            if (typeof lastMessage?.content === "string") {
                text = lastMessage.content;
            } else if (Array.isArray(lastMessage?.content)) {
                text = lastMessage.content
                    .map((item) =>
                        typeof item === "string" ? item : item?.text || ""
                    )
                    .join("");
            }

            if (text && text !== lastText) {
                const delta = text.slice(lastText.length);
                lastText = text;
                res.write(`data: ${JSON.stringify({ text: delta })}\n\n`);
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

// Optional: check memory/thread state
app.get("/memory/:userId", async (req, res) => {
    try {
        const userId = req.params.userId;

        const state = await graph.getState({
            configurable: {
                thread_id: userId,
            },
        });

        res.json({
            userId,
            values: state?.values || null,
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Could not fetch memory state" });
    }
});

app.listen(5000, () => {
    console.log("Server running on http://localhost:5000");
});