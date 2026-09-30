# Retrieval Augmented Generation

## What is RAG?
Retrieval Augmented Generation, or RAG, is a system design in which relevant external information is retrieved before an LLM generates an answer.

A basic RAG pipeline is:

User Query -> Embedding -> Retrieval -> Context -> LLM -> Answer

## Embeddings
An embedding is a numerical vector representation of text. Texts with similar semantic meaning tend to have vectors that are close to each other according to a similarity metric.

Embeddings allow a system to perform semantic search.

## Chunking
Chunking divides large documents into smaller pieces before embedding them. Good chunks should contain enough context to be meaningful while remaining focused.

Very large chunks can reduce retrieval precision, while extremely small chunks may lose context.

## Vector Database
A vector database stores embeddings and allows similarity searches.

Examples include Chroma, Qdrant, Pinecone, and Weaviate.

## Retrieval
Given a user query, the system creates an embedding for the query and retrieves the most similar document chunks.

The top-k retrieved chunks are commonly passed to the LLM as context.

## Hallucination Control
A RAG application can reduce hallucinations by instructing the model to answer using retrieved context and explicitly state when the available context does not contain enough information.

Source metadata can also be returned so users can inspect where an answer came from.
