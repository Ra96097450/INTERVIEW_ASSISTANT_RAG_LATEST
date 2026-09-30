import json
from pathlib import Path

from groq import Groq

from rag import generate_answer


BASE_DIR = Path(__file__).resolve().parent.parent
EVAL_FILE = BASE_DIR / "data" / "evaluation.json"

client = Groq()


with open(EVAL_FILE, "r", encoding="utf-8") as f:
    dataset = json.load(f)


JUDGE_PROMPT = """
You are evaluating a RAG system.

Evaluate the generated answer using ONLY the retrieved context.

Question:
{question}

Retrieved Context:
{context}

Generated Answer:
{answer}

Return ONLY valid JSON in this exact format:

{{
  "faithfulness": 0 or 1,
  "relevance": 0 or 1,
  "explanation": "short explanation"
}}

Rules:

faithfulness = 1 if the answer is supported by the retrieved context.
faithfulness = 0 if the answer contains unsupported claims.

relevance = 1 if the answer directly answers the question.
relevance = 0 if it does not answer the question.

If the context does not contain enough information and the answer correctly says
"I don't have enough information in the knowledge base.",
then faithfulness and relevance should both be 1.
"""


faithfulness_scores = []
relevance_scores = []


for item in dataset:

    question = item["question"]

    answer, results = generate_answer(
        question,
        history=[]
    )

    contexts = results["documents"][0]

    context = "\n\n---\n\n".join(contexts)

    prompt = JUDGE_PROMPT.format(
        question=question,
        context=context,
        answer=answer
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    raw_result = response.choices[0].message.content

    try:
        evaluation = json.loads(raw_result)

    except json.JSONDecodeError:

        print("\nCould not parse judge response:")
        print(raw_result)

        continue

    faithfulness = evaluation["faithfulness"]
    relevance = evaluation["relevance"]

    faithfulness_scores.append(faithfulness)
    relevance_scores.append(relevance)

    print("\n" + "=" * 60)

    print(f"Question: {question}")

    print(f"Answer: {answer}")

    print(f"Faithfulness: {faithfulness}")

    print(f"Relevance: {relevance}")

    print(f"Explanation: {evaluation['explanation']}")


print("\n" + "=" * 60)
print("GENERATION EVALUATION")
print("=" * 60)

if faithfulness_scores:

    print(
        f"Faithfulness: "
        f"{sum(faithfulness_scores) / len(faithfulness_scores):.2%}"
    )

    print(
        f"Answer Relevance: "
        f"{sum(relevance_scores) / len(relevance_scores):.2%}"
    )