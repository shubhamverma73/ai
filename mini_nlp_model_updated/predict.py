import tensorflow as tf
import numpy as np
import json

model = tf.keras.models.load_model( "mini_faq_model.keras" )

with open( "label_mapping.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

while True:

    question = input("Ask: ")

    prediction = model.predict( np.array([question], dtype=object), verbose=0 ) # getting prediction

    print("Prediction", prediction)

    for i, prob in enumerate(prediction[0]):
        print(f"Label {i}: {prob * 100:.2f}%") # converting prediction scientific notation into percentage

    confidence = prediction.max()

    print("Confidence", confidence) # highest confidance that is mathing with my exact output

    # Ask: langgraph stands for
    # Prediction [[2.0956950e-05 2.7887532e-03 8.0048405e-03 4.7616576e-04 9.8870927e-01]]
    # Confidence 0.9887093
    # Here 0 => AI, 1 => RAG, 2 => MCP, 3 => LangChain, 4 => LangGraph so...
    # Above 9.8870927e-01 means it's at lastpace as per Inedex 4 so that's why at last position it's prediction is more heigher like:
    # AI => 0.0021%, RAG => 0.2789%, MCP => 0.8005%, LangChain => 0.0476%, LangGraph => 98.87%, Formula given above that is:
    # print(f"Label {i}: {prob * 100:.2f}%")

    if confidence < 0.70:
        print("I don't know.")
        continue

    class_id = np.argmax(prediction)

    print("Class:", class_id)
    print("Confidence:", prediction.max())

    print("\nAnswer:")
    print(answers[str(class_id)])
    print()