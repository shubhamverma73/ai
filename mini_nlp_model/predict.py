import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model(
    "mini_faq_model.keras"
)

answers = {
    0: "AI stands for Artificial Intelligence.",

    1: "RAG means Retrieval-Augmented Generation.",

    2: "MCP stands for Model Context Protocol.",

    3: "LangChain is a framework for building LLM applications.",

    4: "LangGraph is used for agent workflows."
}

while True:

    question = input("Ask: ")

    prediction = model.predict(
        np.array([question], dtype=object),
        verbose=0
    )

    print("Prediction", prediction)

    confidence = prediction.max()

    print("Confidence", confidence)

    if confidence < 0.70:
        print("I don't know.")
        continue

    class_id = np.argmax(prediction)

    print("Class:", class_id)
    print("Confidence:", prediction.max())

    print("\nAnswer:")
    print(answers[class_id])
    print()