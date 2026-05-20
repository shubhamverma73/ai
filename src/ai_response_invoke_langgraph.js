// npm install express cors langchain @langchain/ollama @langchain/langgraph

import express from "express";
import cors from "cors";
import { ChatOllama } from "@langchain/ollama";
import { StateGraph, START, END } from "@langchain/langgraph";

const app = express();
app.use(cors());
app.use(express.json());

const llm = new ChatOllama({
    baseUrl: "http://localhost:11434",
    model: "llama3:8b",
    temperature: 0.7,
});

// 1) Graph state - generic for any user query
const graph = new StateGraph({
    channels: {
        userMessage: {
            value: (_oldValue, newValue) => newValue,
            default: () => "",
        },
        draftAnswer: {
            value: (_oldValue, newValue) => newValue,
            default: () => "",
        },
        reviewFeedback: {
            value: (_oldValue, newValue) => newValue,
            default: () => "",
        },
        finalAnswer: {
            value: (_oldValue, newValue) => newValue,
            default: () => "",
        },
    },
});

// 2) Node 1: Initial answer generate karega - ANY user query ke liye
const draftNode = async (state) => {
    const prompt = `
User ne ye pucha: "${state.userMessage}"

Is question ka clear, practical, Hindi me answer do. 
- Short aur useful rakhna
- Examples use karo agar jarurat ho
- Step-by-step socho internally
`;

    const response = await llm.invoke(prompt);
    
    return {
        draftAnswer: response.content,
    };
};

// 3) Node 2: Draft ko self-review karega - ANY answer ke liye
const reviewNode = async (state) => {
    const prompt = `
Ye answer hai: "${state.draftAnswer}"

Is answer ko review karo:
1. Kya ye complete aur accurate hai?
2. Kya kuch missing hai?
3. Kya confusing ya unclear hai?
4. Improve karne ke specific suggestions do.

Sirf feedback aur improvement points do, koi naya answer mat banao.
`;

    const response = await llm.invoke(prompt);
    
    return {
        reviewFeedback: response.content,
    };
};

// 4) Node 3: Review feedback se final improved answer banayega - ANY query ke liye
const finalizeNode = async (state) => {
    const prompt = `
Original user question: "${state.userMessage}"
Initial answer: "${state.draftAnswer}"
Review feedback aur suggestions: "${state.reviewFeedback}"

Ab review suggestions ko incorporate karke final improved answer banao.
- Clear, concise, Hindi me
- Feedback ke points cover karo
- User ke original question ko perfectly address karo
`;

    const response = await llm.invoke(prompt);
    
    return {
        finalAnswer: response.content,
    };
};

// 5) Graph flow - universal workflow for ANY query
const chatGraph = graph
    .addNode("draftNode", draftNode)
    .addNode("reviewNode", reviewNode)
    .addNode("finalizeNode", finalizeNode)
    .addEdge(START, "draftNode")
    .addEdge("draftNode", "reviewNode")
    .addEdge("reviewNode", "finalizeNode")
    .addEdge("finalizeNode", END)
    .compile();

// LangGraph route - multi-step universal workflow
app.post("/chat-stream", async (req, res) => {
    try {
        const message = req.body?.message || "What about Bhadohi?";

        const result = await chatGraph.invoke({
            userMessage: message,
        });

        res.setHeader("Content-Type", "text/plain; charset=utf-8");
        res.end(result.finalAnswer);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Something went wrong" });
    }
});


// Without streaming and langgraph invoke example
app.get("/chat-sse", async (req, res) => {
	try {
		const message = req.query.message || "What about Bhadohi?";

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

app.listen(5000, () => {
	console.log("Server running on http://localhost:5000");
});