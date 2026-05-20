// Install required packages first:
// npm install langchain @langchain/ollama

import { ChatOllama } from "@langchain/ollama";

// Ollama model configuration
const llm = new ChatOllama({
	baseUrl: "http://localhost:11434", // Ollama default URL
	model: "llama3:8b",
	temperature: 0.7,
});

// Simple function
async function runChat() {
	try {
		const response = await llm.invoke(
			"What about Bhadohi?"
		);

		console.log("AI Response:");
		console.log(response.content);
	} catch (error) {
		console.error("Error:", error);
	}
}

//runChat();

async function runStreamChat() {
  try {
    const stream = await llm.stream(
      "What about Bhadohi?"
    );

    console.log("AI Streaming Response:\n");

    for await (const chunk of stream) {
      process.stdout.write(chunk.text);
    }

    console.log("\n\nStream complete.");
  } catch (error) {
    console.error("Error:", error);
  }
}

runStreamChat();
