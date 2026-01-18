import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

CHUNKS_FILE = os.path.join(PROCESSED_DIR, "sample_chunks.json")
FAISS_INDEX_FILE = os.path.join(PROCESSED_DIR, "faiss.index")
METADATA_FILE = os.path.join(PROCESSED_DIR, "faiss_metadata.json")

# Load chunks
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# Create embeddings locally
embeddings = model.encode(
    chunks,
    show_progress_bar=True,
    convert_to_numpy=True
).astype("float32")

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index
faiss.write_index(index, FAISS_INDEX_FILE)

# Save metadata
metadata = [{"id": i, "text": chunk} for i, chunk in enumerate(chunks)]

with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("✅ Local embeddings created and stored in FAISS")
print(f"🔢 Total vectors: {index.ntotal}")
