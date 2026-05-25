import { CloudClient } from 'chromadb';
import { DefaultEmbeddingFunction } from '@chroma-core/default-embed';
import dotenv from 'dotenv';
import path from 'path';
import { generateEmbeddings } from './save-embeddings.js';
import { fileURLToPath, pathToFileURL } from 'url';
import fs from 'fs';
import crypto from 'crypto';

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
        name: 'my_details',
    });
}

async function addDocument(text, id = crypto.randomUUID(), metadata = { source: 'my_data' }) {
    const embeddingText = text.trim().toLowerCase();
    const embedding = await generateEmbeddings(embeddingText);
    const collection = await getCollection();

    await collection.add({
        ids: [id],
        metadatas: [metadata],
        documents: [text],
        embeddings: [embedding],
    });

    console.log('Added document to Chroma DB:', text);
}

//async function searchCollection(query, nResults = 5) {
async function searchCollection(query, nResults = 3) { // nResults set to 1 to get only the best match or n number of matches
    const collection = await getCollection();
    const queryEmbedding = await generateEmbeddings(query.trim().toLowerCase());

    const result = await collection.query({
        queryEmbeddings: [queryEmbedding],
        nResults,
        include: ['documents', 'metadatas', 'distances'],
    });

    console.log('\nSearch query:', query);

    const documents = result.documents?.[0] ?? [];
    const metadatas = result.metadatas?.[0] ?? [];
    const distances = result.distances?.[0] ?? [];

    documents.forEach((doc, index) => {
        console.log(`\nResult ${index + 1}:`, doc);
        console.log('Metadata:', metadatas[index]);
        console.log('Distance:', distances[index]);
    });

    return { documents, metadatas, distances, raw: result };
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
    //await addDocument('I am passionate about coding');
    await searchCollection('What i like?');
}

export { getCollection, addDocument, searchCollection };