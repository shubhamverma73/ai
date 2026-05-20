import express from "express";
import { ChatOllama } from "@langchain/ollama";

const app = express();

app.use(express.json());

const llm = new ChatOllama({
	baseUrl: "http://localhost:11434",
	model: "llama3:8b",
});

app.post("/chat", async (req, res) => {
	try {
		const { message } = req.body;

		const response = await llm.invoke(message);

		res.json({ success: true, response: response.content, });
	} catch (error) {
		res.status(500).json({ success: false, error: error.message, });
	}
});

app.listen(3000, () => {
	console.log("Server running on port 3000");
});