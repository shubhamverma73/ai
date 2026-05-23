// search.js

// npm install @langchain/ollama

import fs from "fs";
import { pathToFileURL } from "url";
import { OllamaEmbeddings } from "@langchain/ollama";

const embeddings = new OllamaEmbeddings({
	baseUrl: "http://localhost:11434",
	model: "nomic-embed-text",
});

// Cosine Similarity Function
export function cosineSimilarity(vecA, vecB) {
	let dotProduct = 0;
	let normA = 0;
	let normB = 0;

	for (let i = 0; i < vecA.length; i++) {
		dotProduct += vecA[i] * vecB[i];
		normA += vecA[i] * vecA[i];
		normB += vecB[i] * vecB[i];
	}

	return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

async function search(query) {
	// Load stored embeddings
	const storedData = JSON.parse(
		fs.readFileSync("embeddings.json", "utf-8")
	);

	// Generate query embedding
	const queryEmbedding = await embeddings.embedQuery(query);

	let bestMatch = null;
	let highestScore = -1;

	for (const item of storedData) {
		const score = cosineSimilarity(
			queryEmbedding,
			item.embedding
		);

		console.log(
			`Similarity with "${item.text}" => ${score}`
		);

		if (score > highestScore) {
			highestScore = score;
			bestMatch = item.text;
		}
	}

	console.log("\n=====================");
	console.log("User Query:", query);
	console.log("Best Match:", bestMatch);
	console.log("Score:", highestScore);
	console.log("=====================");
}

// Ask anything
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
	search("What i want to build?");
}

// node search.js