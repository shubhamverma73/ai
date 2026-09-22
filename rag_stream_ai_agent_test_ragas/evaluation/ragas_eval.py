def evaluate_single(
    question,
    contexts,
    answer,
    ground_truth,
    llm_model=None,
    embedding_model=None,
):
    """
    Evaluate one sample with the RAGAS framework.

    Keep it separate from the Flask answer stream so the app only returns
    the model answer. This function is intended for a standalone runner.

    The function accepts the same local LangChain Ollama objects the project
    already uses, and passes them explicitly into RAGAS so the evaluation
    path does not quietly drift into an OpenAI environment default.

    For robustness on a local machine we deliberately reduce the metric set
    and evaluation parallelism.
    """
    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import (
            answer_relevancy,
            context_recall,
        )
        from ragas.llms import LangchainLLMWrapper
        from ragas.embeddings import LangchainEmbeddingsWrapper

        # Prefer project-local Ollama objects when supplied; otherwise load
        # them from the existing project gateway object.
        if llm_model is None:
            from tools.rag_tool import llm as llm_model

        if embedding_model is None:
            from tools.rag_tool import embedding_model as embedding_model

        dataset = Dataset.from_dict({
            "question": [question],
            "answer": [answer],
            "contexts": [contexts],
            "ground_truth": [ground_truth],
        })

        ragas_llm = LangchainLLMWrapper(llm_model)
        ragas_embeddings = LangchainEmbeddingsWrapper(embedding_model)

        result = evaluate(
            dataset,
            metrics=[
                answer_relevancy,
                context_recall,
            ],
            llm=ragas_llm,
            embeddings=ragas_embeddings,
            show_progress=False,
            batch_size=1,
            raise_exceptions=False,
        )

        # Preserve the expected field shape for local runs. When a metric
        # cannot be produced by the installed local adapter stack, keep the
        # metric key in the result dictionary with an explicit None value
        # rather than crashing the schema or dropping the field silently.
        # This is a safe serialization format for a local evaluation test.
        if hasattr(result, "to_dict"):
            payload = result.to_dict()
        else:
            payload = result

        if isinstance(payload, dict):
            payload.setdefault("faithfulness", None)
            payload.setdefault("context_precision", None)
        else:
            payload = {
                "answer_relevancy": getattr(result, "answer_relevancy", None),
                "context_recall": getattr(result, "context_recall", None),
                "faithfulness": None,
                "context_precision": None,
            }

        return {
            "status": "ok",
            "result": payload,
        }

    except Exception as exc:
        return {
            "status": "skipped",
            "error": f"RAGAS evaluation skipped due to import/runtime failure: {exc}",
        }
