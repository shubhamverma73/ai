import json
import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.rag_tool import (retrieve_context, build_prompt, llm, embedding_model)

from evaluation_new.ragas_eval import ( evaluate_single )


def generate_answer(question):

    context, metadata, docs = retrieve_context(question)

    prompt = build_prompt(question=question, context=context, history_text="")

    response = llm.invoke(prompt)

    return (response.content, docs)


def run_evaluation():

    all_scores = []

    with open("evaluation_new/test_dataset.json", "r", encoding="utf-8") as f:

        test_cases = json.load(f)

    print("\n")
    print("=" * 80)
    print("RAGAs Evaluation")
    print("=" * 80)

    for index, test_case in enumerate(test_cases, start=1):

        question = test_case["question"]

        ground_truth = test_case["ground_truth"]

        answer, contexts = (generate_answer(question))

        result = evaluate_single(question=question, contexts=contexts, answer=answer, ground_truth=ground_truth, evaluator_llm=llm, evaluator_embeddings=embedding_model)

        print("\n")
        print("=" * 80)

        print(f"Test Case : {index}")

        print(f"Question   : {question}")

        print(f"Answer     : {answer}")

        print("\nScores")

        print(type(result))
        print(result)

        df = result.to_pandas()

        print(df)

        # Question bhi save kar lenge
        df["question"] = question

        all_scores.append(df)

        row = df.iloc[0]

        # ==========================================
        # Print Evaluation Scores
        # ==========================================

        print("\nEvaluation Scores")
        print("-" * 40)

        metrics = [
            "faithfulness", "answer_relevancy",
            "llm_context_precision_with_reference", "context_recall"
        ]

        for metric in metrics:

            score = row[metric]

            if pd.isna(score):

                score = "N/A"

            else:

                score = round(score, 4)

            print(f"{metric:<40}: {score}")

        print("=" * 80)

    final_df = pd.concat(all_scores, ignore_index=True)

    print("\n")
    print("=" * 80)
    print("Average Scores")
    print("=" * 80)

    final_df.to_csv("evaluation_new/evaluation_report.csv", index=False)

    print(final_df.mean(numeric_only=True))


if __name__ == "__main__":

    run_evaluation()
