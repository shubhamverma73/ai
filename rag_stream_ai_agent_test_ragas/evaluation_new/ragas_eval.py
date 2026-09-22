from datasets import Dataset
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from ragas import evaluate

from ragas.metrics import (Faithfulness, ResponseRelevancy,
                           LLMContextPrecisionWithReference, LLMContextRecall)


def evaluate_single(question, contexts, answer, ground_truth, evaluator_llm, evaluator_embeddings):
    dataset = Dataset.from_dict({
        "user_input": [question],
        "retrieved_contexts": [contexts],
        "response": [answer],
        "reference": [ground_truth],
    })

    ragas_llm = LangchainLLMWrapper(evaluator_llm)

    ragas_embeddings = LangchainEmbeddingsWrapper(evaluator_embeddings)

    result = evaluate(dataset=dataset,
                      metrics=[Faithfulness(), ResponseRelevancy(), LLMContextPrecisionWithReference(), LLMContextRecall()],
                      llm=ragas_llm,
                      embeddings=ragas_embeddings)

    return result
