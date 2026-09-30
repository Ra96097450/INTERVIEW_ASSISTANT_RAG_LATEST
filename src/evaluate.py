import json
import time
from pathlib import Path

from rag import generate_answer


BASE_DIR = Path(__file__).resolve().parent.parent

EVAL_FILE = BASE_DIR / "data" / "evaluation.json"


with open(EVAL_FILE, "r", encoding="utf-8") as f:
    dataset = json.load(f)


total = len(dataset)

correct_retrieval = 0
total_latency = 0
total_precision = 0

for item in dataset:

    question = item["question"]
    expected_sources = set(item["expected_sources"])

    start = time.perf_counter()

    answer, results = generate_answer(
        question,
        history=[]
    )

    latency = time.perf_counter() - start

    total_latency += latency

    retrieved_sources = [
    metadata["source"]
    for metadata in results["metadatas"][0]
]

    expected_sources = set(item["expected_sources"])

    # Recall@3
    if expected_sources:
        recall_hit = bool(
            expected_sources.intersection(retrieved_sources)
        )
    else:
        recall_hit = len(retrieved_sources) == 0

    # Precision@3
    if expected_sources:
        relevant_retrieved = sum(
            1
            for source in retrieved_sources
            if source in expected_sources
        )

        precision = (
            relevant_retrieved / len(retrieved_sources)
            if retrieved_sources
            else 0
        )
    else:
        # For an unknown question, all retrieved chunks
        # should ideally be zero.
        precision = (
            1.0
            if len(retrieved_sources) == 0
            else 0.0
        )

    if recall_hit:
        correct_retrieval += 1

    total_precision += precision

    print("\n" + "=" * 60)

    print(f"Question: {question}")

    print(f"Expected: {expected_sources}")

    print(f"Retrieved: {retrieved_sources}")

    print(f"Latency: {latency:.2f}s")

    print(f"Retrieval hit: {recall_hit}")

    print(f"Answer: {answer}")


retrieval_recall = correct_retrieval / total

average_latency = total_latency / total


print("\n" + "=" * 60)

print("EVALUATION SUMMARY")

print("=" * 60)

print(f"Total questions: {total}")

print(
    f"Retrieval Recall: "
    f"{retrieval_recall:.2%}"
)

precision_at_3 = total_precision / total

print(
    f"Precision@3: "
    f"{precision_at_3:.2%}"
)

print(
    f"Average latency: "
    f"{average_latency:.2f}s"
)