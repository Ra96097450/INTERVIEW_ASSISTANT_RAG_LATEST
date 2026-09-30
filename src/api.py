from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .vector_store import ensure_vector_store
from .rag import generate_answer

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Checking vector store...")

    ensure_vector_store()

    print("Vector store ready.")

    yield


app = FastAPI(
    title="InterviewIQ API",
    lifespan=lifespan
)


class AskRequest(BaseModel):
    question: str
    history: list[dict] = Field(default_factory=list)

@app.get("/")
def root():
    return {
        "message": "InterviewIQ RAG API is running"
    }


@app.post("/ask")
def ask_question(request: AskRequest):

    answer, results = generate_answer(
        request.question, 
        request.history
    )

    sources = list(
        dict.fromkeys(
            metadata["source"]
            for metadata in results["metadatas"][0]
        )
    )

    retrieved_chunks = []

    for i, metadata in enumerate(results["metadatas"][0]):

        retrieved_chunks.append({
            "source": metadata["source"],
            "vector_distance": results["distances"][0][i],
            "reranker_score": results["reranker_scores"][0][i],
            "content": results["documents"][0][i]
        })

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks
    }