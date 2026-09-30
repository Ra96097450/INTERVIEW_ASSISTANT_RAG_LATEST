from sentence_transformers import SentenceTransformer
from .chunking import chunk_text
from .ingestion import load_documents


# Load embedding model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def create_embeddings():

    documents = load_documents()

    all_chunks = []

    for document in documents:

        chunks = chunk_text(document["text"])

        for chunk in chunks:

            all_chunks.append({
                "source": document["source"],
                "text": chunk
            })

    texts = [chunk["text"] for chunk in all_chunks]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return all_chunks, embeddings


if __name__ == "__main__":

    chunks, embeddings = create_embeddings()

    print("Total chunks:", len(chunks))
    print("Embedding shape:", embeddings.shape)

    print("\nFirst chunk:")
    print(chunks[0]["text"])

    print("\nFirst embedding:")
    print(embeddings[0])