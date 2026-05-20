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


// ========================= NEWLY ADDED: local offline date helper =========================
// Ye helper local system time se aaj, kal, yesterday, etc. ka context banata hai.
// Isme koi online API use nahi ho rahi.
function getLocalDateContext() {
    const now = new Date();

    const today = new Date(now);
    const yesterday = new Date(now);
    yesterday.setDate(now.getDate() - 1);

    const tomorrow = new Date(now);
    tomorrow.setDate(now.getDate() + 1);

    const formatDate = (date) =>
        date.toLocaleDateString("en-IN", {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric",
            timeZone: "Asia/Kolkata",
        });

    const formatDateTime = (date) =>
        date.toLocaleString("en-IN", {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric",
            hour: "numeric",
            minute: "2-digit",
            second: "2-digit",
            hour12: true,
            timeZone: "Asia/Kolkata",
        });

    return {
        nowText: formatDateTime(today),
        todayText: formatDate(today),
        yesterdayText: formatDate(yesterday),
        tomorrowText: formatDate(tomorrow),
    };
}


// ========================= NEWLY ADDED: detect date-related query =========================
// Agar user date / today / yesterday / tomorrow type question puche,
// to hum local date context prompt me inject kar denge.
function buildPromptWithOfflineDateTool(message) {
    const text = String(message || "");
    const lowerText = text.toLowerCase();

    const needsDateContext =
        lowerText.includes("date") ||
        lowerText.includes("today") ||
        lowerText.includes("yesterday") ||
        lowerText.includes("tomorrow") ||
        lowerText.includes("aaj") ||
        lowerText.includes("kal") ||
        lowerText.includes("parso") ||
        lowerText.includes("abhi") ||
        lowerText.includes("time");

    if (!needsDateContext) {
        return text;
    }

    const dateContext = getLocalDateContext();

    return `
You are an offline assistant. Use the following LOCAL SYSTEM DATE/TIME information whenever the user asks about date, today, yesterday, tomorrow, or current time.

Current local date and time: ${dateContext.nowText}
Today: ${dateContext.todayText}
Yesterday: ${dateContext.yesterdayText}
Tomorrow: ${dateContext.tomorrowText}

Important:
- For date/time questions, answer using the above local system values.
- Do not say that you do not know the current date/time.
- If the user asks about weather or temperature, clearly say that live weather needs an external API/tool.

User question: ${text}
`.trim();
}


app.post("/chat-stream", async (req, res) => {
    try {
        const message = req.body?.message || "What about Bhadohi?";

        // ========================= NEWLY ADDED =========================
        // Date-related queries ke liye local offline date context inject kiya ja raha hai.
        const finalMessage = buildPromptWithOfflineDateTool(message);

        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.setHeader("Transfer-Encoding", "chunked");

        // ========================= CHANGED ONLY THIS VARIABLE =========================
        const stream = await llm.stream(finalMessage);

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

        // ========================= NEWLY ADDED =========================
        // SSE route me bhi same offline date context inject kiya ja raha hai.
        const finalMessage = buildPromptWithOfflineDateTool(message);

        res.setHeader("Content-Type", "text/event-stream"); // SSE content type
        res.setHeader("Cache-Control", "no-cache");
        res.setHeader("Connection", "keep-alive");

        // ========================= CHANGED ONLY THIS VARIABLE =========================
        const stream = await llm.stream(finalMessage);

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

app.listen(5000, () => {
    console.log("Server running on http://localhost:5000");
});