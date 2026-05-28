import express from "express";
import { ChatOllama } from "@langchain/ollama";
import { ChatPromptTemplate } from "@langchain/core/prompts";

const app = express();

app.use(express.json());

const llm = new ChatOllama({
    baseUrl: "http://localhost:11434",
    model: "llama3:8b",
});

const prompt = ChatPromptTemplate.fromMessages([
    [
        "system", "Reply in {language}."
    ],
    ["human", "{message}"]
]);

const chain = prompt.pipe(llm);

app.post("/chat", async (req, res) => {
    try {
        const { message } = req.body;

        const response = await chain.invoke({
            message,
            language: "simple Hindi"
        });

        res.json({
            success: true,
            response: response.content,
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
        });
    }
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});