
import { CloudClient } from 'chromadb';
import { DefaultEmbeddingFunction } from '@chroma-core/default-embed';
import dotenv from 'dotenv';
import path from 'path';
import { generateEmbeddings } from './save-embeddings.js';
import { fileURLToPath, pathToFileURL } from 'url';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.join(__dirname, '../.ENV') });

const client = new CloudClient({
    apiKey: process.env.CHROMA_API_KEY,
    tenant: process.env.CHROMA_TENANT,
    database: process.env.CHROMA_DATABASE,
});

async function getCollection() {
    return await client.getOrCreateCollection({
        name: 'my_details_384',
    });
}

// Cosine similarity helper (used to find the nearest item from local embeddings.json)
export function cosineSimilarity(vecA, vecB) {
    let dot = 0;
    let normA = 0;
    let normB = 0;
    for (let i = 0; i < vecA.length; i++) {
        dot += vecA[i] * vecB[i];
        normA += vecA[i] * vecA[i];
        normB += vecB[i] * vecB[i];
    }
    return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

async function addDocument(text, id = '1', metadata = { source: 'my_data' }) {
    const embedding = await generateEmbeddings(text);
    const collection = await getCollection();

    await collection.add({
        ids: [id],
        metadatas: [metadata],
        documents: [text],
        embeddings: [embedding],
    });

    console.log('Added document to Chroma DB:', text);
}

async function searchCollection(query, nResults = 5) {
    const collection = await getCollection();
    const queryEmbedding = await generateEmbeddings(query);

    const result = await collection.query({
        queryEmbeddings: [queryEmbedding],
        nResults,
        include: ['documents', 'metadatas', 'distances', 'embeddings'],
    });

    console.log('\nSearch query:', query);

    const documents = result.documents?.[0] ?? [];
    const metadatas = result.metadatas?.[0] ?? [];
    const distances = result.distances?.[0] ?? [];
    const returnedEmbeddings = result.embeddings?.[0] ?? [];

    // Compute cosine similarity between queryEmbedding and embeddings returned by Chroma
    try {
        if (returnedEmbeddings.length > 0) {
            let bestSim = -Infinity;
            let bestIndex = -1;
            for (let i = 0; i < returnedEmbeddings.length; i++) {
                const emb = returnedEmbeddings[i];
                if (!emb) continue;
                const sim = cosineSimilarity(queryEmbedding, emb);
                if (sim > bestSim) {
                    bestSim = sim;
                    bestIndex = i;
                }
            }
            if (bestIndex >= 0) {
                console.log('\nBest match (from Chroma embeddings):', documents[bestIndex]);
                console.log('Metadata:', metadatas[bestIndex]);
                console.log('Distance:', distances[bestIndex]);
                console.log('Similarity:', bestSim);
            }
        } else {
            console.log('No embeddings returned by Chroma to compute local similarity.');
        }
    } catch (err) {
        console.warn('Error computing similarity from Chroma embeddings:', err && err.message ? err.message : err);
    }

    return result;
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
    //await addDocument('I love Node.js', '4', { source: 'my_data' });
    await searchCollection('What I love?');
}

export { getCollection, addDocument, searchCollection };