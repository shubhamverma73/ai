// npm install express cors langchain @langchain/ollama

import express from "express";
import cors from "cors";
import { OllamaEmbeddings } from "@langchain/ollama";

const app = express();

app.use(cors());
app.use(express.json());

app.options("/{*any}", cors());

const embeddings = new OllamaEmbeddings({
  baseUrl: "http://localhost:11434",
  model: "nomic-embed-text", // embedding model
});

app.post("/embedding", async (req, res) => {
  try {
    const text = req.body?.text || "lion";

    // Generate embedding
    const vector = await embeddings.embedQuery(text);

    console.log("Total Dimensions:", vector.length);

    console.log("First 10 Values:");
    console.log(vector.slice(0, 10));

    res.json({
      text,
      totalDimensions: vector.length,
      first10Values: vector,
    });

  } catch (error) {
    console.error(error);

    res.status(500).json({
      error: "Something went wrong",
    });
  }
});

app.listen(5000, () => {
  console.log("Server running on http://localhost:5000");
});