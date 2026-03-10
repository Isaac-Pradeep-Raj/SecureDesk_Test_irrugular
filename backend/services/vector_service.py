import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Embedding dimension for MiniLM
dimension = 384

# FAISS index
index = faiss.IndexFlatL2(dimension)

# Store original chunks
chunk_store = []


def add_chunks_to_index(chunks):
    if not chunks:
        return

    embeddings = model.encode(chunks)

    vectors = np.array(embeddings).astype("float32")

    index.add(vectors)

    chunk_store.extend(chunks)

    print(f"[VectorService] Added {len(chunks)} chunks.")
    print(f"[VectorService] Index size: {index.ntotal}")
    print(f"[VectorService] Chunk store size: {len(chunk_store)}")


def search_chunks(query, top_k=5, threshold=1.5):

    # If index is empty, return no results
    if index.ntotal == 0:
        print("[VectorService] FAISS index is empty.")
        return []

    # Ensure top_k does not exceed index size
    top_k = min(top_k, index.ntotal)

    query_embedding = model.encode([query])

    query_vector = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []

    for dist, i in zip(distances[0], indices[0]):

        # Skip invalid indices or distance too high
        if i == -1 or dist > threshold:
            continue

        # Ensure index exists in chunk_store
        if 0 <= i < len(chunk_store):
            results.append(chunk_store[i])
        else:
            print(f"[VectorService] Warning: index {i} out of chunk_store range.")

    return results