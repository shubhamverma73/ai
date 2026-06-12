'''
ingest.py

Ye sirf ek baar chalegi.

    PDF
    ↓
    Chunk
    ↓
    Embedding
    ↓
    Store in Chroma
'''

# ingest.py

import os
import uuid
import chromadb
import re

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings

load_dotenv()

# -------------------------
# Chroma Cloud Connection
# -------------------------

client = chromadb.CloudClient(
    api_key=os.getenv("CHROMA_API_KEY"),
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE")
)

collection = client.get_or_create_collection(
    name="rag_test_collection"
)

# -------------------------
# Load Single PDF
# -------------------------

#PDF_PATH = "data/pdfs/company_policy.pdf"

#loader = PyPDFLoader(PDF_PATH)
#docs = loader.load()

# -------------------------
# Load Single PDF
# -------------------------

# -------------------------
# Load Multiple PDFs
# -------------------------

PDF_FOLDER = "data/pdfs"

all_docs = []

pdf_files = [
    file
    for file in os.listdir(PDF_FOLDER)
    if file.endswith(".pdf")
]

for pdf_file in pdf_files:

    pdf_path = os.path.join(
        PDF_FOLDER,
        pdf_file
    )

    print(f"Loading: {pdf_file}")

    loader = PyPDFLoader(pdf_path)

    docs = loader.load()

    for doc in docs:

        doc.metadata["source"] = pdf_file

    all_docs.extend(docs)

# -------------------------
# Load Multiple PDFs
# -------------------------

print(f"Pages Loaded: {len(all_docs)}")

# -------------------------
# Chunking
# -------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(all_docs)

print(f"Chunks Created: {len(chunks)}")

# -------------------------
# Embedding Model
# -------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# -------------------------
# Prepare Data
# -------------------------

# pdf_name = os.path.basename(PDF_PATH)

ids = []
documents = []
metadatas = []
vectors = []

for chunk in chunks:

    cleaned_text = re.sub(
        r"\[cite:\d+\]",
        "",
        chunk.page_content
    )

    ids.append(str(uuid.uuid4()))

    documents.append(cleaned_text)

    #metadata = {
        #"source": pdf_name,
        #"page": chunk.metadata.get("page", 0) + 1 # Pages are 0-indexed internally, so we add 1 for human-friendly numbering
    #}
    metadata = {
        "source": chunk.metadata.get(
            "source",
            "Unknown"
        ),

        "page": chunk.metadata.get(
            "page",
            0
        ) + 1
    }

    metadatas.append(metadata)

    vectors.append(
        embeddings.embed_query(
            cleaned_text
        )
    )

# -------------------------
# Save into Chroma
# -------------------------

collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=vectors
)

print("PDF stored successfully!")

# Only one time run karna hai. Baad mein app.py se directly access karenge Chroma ko for retrieval.
# python ingest.py