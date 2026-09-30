import chromadb

from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder


# Load the same embedding model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

#Reranker 
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


# Connect to existing ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="interviewiq"
)


def search(query, top_k=3, max_distance=0.75):

    query_embedding = model.encode(query).tolist()

    # Retrieve more candidates first
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # First-stage relevance filtering
    candidates = []

    for i, distance in enumerate(distances):

        if distance <= max_distance:

            candidates.append({
                "document": documents[i],
                "metadata": metadatas[i],
                "distance": distance
            })

    if not candidates:

        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
            "reranker_scores": [[]]
            }

    # Reranking
    pairs = [
        [query, candidate["document"]]
        for candidate in candidates
    ]

    reranker_scores = reranker.predict(pairs)

    # Attach reranker score
    for candidate, score in zip(
        candidates,
        reranker_scores
    ):
        candidate["reranker_score"] = float(score)

    # Highest reranker score first
    candidates.sort(
        key=lambda x: x["reranker_score"],
        reverse=True
    )

    # Keep best 3
    candidates = candidates[:top_k]

    return {
    "documents": [[
        candidate["document"]
        for candidate in candidates
    ]],

    "metadatas": [[
        candidate["metadata"]
        for candidate in candidates
    ]],

    "distances": [[
        candidate["distance"]
        for candidate in candidates
    ]],

    "reranker_scores": [[
        candidate["reranker_score"]
        for candidate in candidates
    ]]
}



if __name__ == "__main__":

    query = "How does gradient descent update model weights?"

    results = search(query)

    print("\nUSER QUERY:")
    print(query)

    print("\nRETRIEVED CHUNKS:\n")

    for i, document in enumerate(results["documents"][0]):

        print(f"--- Result {i + 1} ---")
        print(document)

        print("\nSource:")
        print(results["metadatas"][0][i])

        print("\nDistance:")
        print(results["distances"][0][i])

        print()