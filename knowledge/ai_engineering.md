# AI Engineering

## AI Engineer Responsibilities
An AI engineer typically works across data processing, machine learning or LLM applications, APIs, deployment, evaluation, and monitoring.

## Production RAG
A production RAG system commonly contains document ingestion, preprocessing, chunking, embeddings, vector storage, retrieval, prompt construction, LLM generation, evaluation, observability, and security.

## FastAPI
FastAPI is a Python web framework commonly used to build APIs. It supports request validation using Python type hints and integrates well with Pydantic models.

A RAG backend can expose an endpoint such as POST /ask that accepts a user question and returns an answer together with retrieved sources.

## Evaluation
RAG systems should be evaluated separately for retrieval and generation.

Retrieval metrics can include Recall@K, Precision@K, and Mean Reciprocal Rank. Generation can be evaluated for answer relevance, faithfulness, and citation correctness.

## Observability
Useful production metrics include request latency, retrieval latency, LLM latency, token usage, error rates, retrieved document IDs, and user feedback.
