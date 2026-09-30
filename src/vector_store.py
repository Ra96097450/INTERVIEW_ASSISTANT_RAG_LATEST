from pathlib import Path

import chromadb

from .embeddings import create_embeddings


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"


client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="interviewiq"
)


def store_embeddings():
    chunks, embeddings = create_embeddings()

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"chunk_{i}")
        documents.append(chunk["text"])
        metadatas.append({
            "source": chunk["source"]
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings.tolist()
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB")


def ensure_vector_store():
    count = collection.count()

    if count == 0:
        print("ChromaDB is empty. Building vector store...")
        store_embeddings()
    else:
        print(f"ChromaDB already contains {count} chunks.")


if __name__ == "__main__":
    ensure_vector_store()