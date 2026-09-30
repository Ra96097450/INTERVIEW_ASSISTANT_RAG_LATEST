import os

from dotenv import load_dotenv
from groq import Groq

from .retriever import search

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(query, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an AI Engineer interview assistant.

Answer the user's question using ONLY the context provided below.

If the answer cannot be found in the context, say:
"I don't have enough information in the knowledge base."

Formatting rules:
- Use Markdown for headings, bullet points, and emphasis.
- When writing mathematical equations, use LaTeX display math with $$ ... $$.
- Do not use [ ... ] for mathematical equations.
- Keep equations on separate lines.
- Use inline LaTeX with $ ... $ when an equation appears within a sentence.
- Use fenced code blocks for programming code.


Context:
----------------
{context}
----------------

Question:
{query}

Answer:
"""

    return prompt

def rewrite_query(query, history):

    if not history:
        return query

    conversation = ""

    for message in history[-6:]:
        conversation += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
You are a query rewriting system for a RAG application.

Rewrite the user's latest question into a standalone question
that can be understood without the conversation history.

Do not answer the question.
Do not add information that is not present.
Return ONLY the rewritten question.

Conversation:
{conversation}

Latest question:
{query}

Standalone question:
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def generate_answer(query, history=None):

    if history is None:
        history = []

    rewritten_query = rewrite_query(
        query,
        history
    )

    results = search(
    rewritten_query,
    top_k=3
    )
    
    if not results["documents"][0]:

        return (
            "I don't have enough information in the knowledge base.",
            results
        )


    retrieved_chunks = results["documents"][0]

    prompt = build_prompt(
        query,
        retrieved_chunks
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return answer, results


if __name__ == "__main__":

    history = [
        {
            "role": "user",
            "content": "What is gradient descent?"
        },
        {
            "role": "assistant",
            "content": "Gradient descent is an optimization algorithm used to minimize a loss function."
        }
    ]

    query = "Why does it reduce the loss?"

    rewritten = rewrite_query(
        query,
        history
    )

    print("\nOriginal query:")
    print(query)

    print("\nRewritten query:")
    print(rewritten)