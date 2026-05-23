// save-embeddings.js

// npm install @langchain/ollama

import fs from "fs";
import { pathToFileURL } from "url";
import { OllamaEmbeddings } from "@langchain/ollama";

const embeddings = new OllamaEmbeddings({
	baseUrl: "http://localhost:11434",
	model: "nomic-embed-text",
});

// Your training data
const data = [
	"My name is Shubham",
	"I am a software developer",
	"I live in Bhadohi",
	"I love Node.js",
	"I work with AI",
	"I use LangChain",
	"I like JavaScript",
	"I enjoy learning new technologies",
	"I am passionate about coding",
	"I want to build amazing applications",
];

export async function generateEmbeddings(text) {
	return await embeddings.embedQuery(text);
}

async function createEmbeddings() {
	const finalData = [];

	for (const text of data) {
		console.log(`Generating embedding for: ${text}`);

		const embedding = await generateEmbeddings(text);

		finalData.push({
			text,
			embedding,
		});
	}

	fs.writeFileSync(
		"embeddings.json",
		JSON.stringify(finalData, null, 2)
	);

	console.log("\nEmbeddings saved in embeddings.json");
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
	createEmbeddings();
}

// node save-embeddings.js