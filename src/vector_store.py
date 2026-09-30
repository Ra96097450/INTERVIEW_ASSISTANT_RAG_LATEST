import chromadb

from embeddings import create_embeddings


# Create persistent Chroma database
client = chromadb.PersistentClient(
    path="./chroma_db"
)


# Create or load our collection
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

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings.tolist()
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB")


if __name__ == "__main__":

    store_embeddings()

    print("Total records in ChromaDB:",
          collection.count())