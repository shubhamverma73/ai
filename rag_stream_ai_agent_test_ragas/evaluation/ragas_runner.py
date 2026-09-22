import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.rag_tool import (
    build_history_text,
    build_prompt,
    llm,
    embedding_model,
    retrieve_context,
)
from evaluation.ragas_eval import evaluate_single

DATASET_PATH = PROJECT_ROOT / "evaluation" / "test_dataset.json"


def main():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    for sample in test_data:
        question = sample["question"]
        ground_truth = sample["ground_truth"]

        context, metadata, docs = retrieve_context(question)
        history_text = build_history_text()
        prompt = build_prompt(question, context, history_text)

        answer_obj = llm.invoke(prompt)
        answer = answer_obj.content if hasattr(answer_obj, "content") else str(answer_obj)

        result = evaluate_single(
            question=question,
            contexts=docs,
            answer=answer,
            ground_truth=ground_truth,
            llm_model=llm,
            embedding_model=embedding_model,
        )

        print(f"================> RAGAs Evaluation Testing Output: {result}")


if __name__ == "__main__":
    main()