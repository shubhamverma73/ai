import tensorflow as tf
import numpy as np
import json

# -----------------
# Load Model
# -----------------

model = tf.keras.models.load_model(
    "mini_language_model.keras"
)

# -----------------
# Load Vocabulary
# -----------------

with open(
    "vocab.json",
    "r",
    encoding="utf-8"
) as f:

    vocab = json.load(f)

word_to_id = {
    word: idx
    for idx, word in enumerate(vocab)
}

id_to_word = {
    idx: word
    for idx, word in enumerate(vocab)
}

# -----------------
# Prediction Loop
# -----------------

while True:

    text = input("\nInput: ").lower()

    words = text.split()

    sequence = []

    for word in words:

        if word in word_to_id:
            sequence.append(
                word_to_id[word]
            )

    if len(sequence) == 0:

        print("Unknown words")
        continue

    sequence = tf.keras.preprocessing.sequence.pad_sequences(
        [sequence],
        maxlen=5,
        padding="pre"
    )

    prediction = model.predict(
        sequence,
        verbose=0
    )

    # ------------------
    # Top Predictions
    # ------------------
    top5 = np.argsort(prediction[0])[-5:][::-1]
    print("\nTop Predictions:")
    for idx in top5:
        print(f"{id_to_word[idx]} : {prediction[0][idx]*100:.2f}%")
    # ------------------

    next_word_id = np.argmax(
        prediction
    )

    print(
        "Next Word:",
        id_to_word.get(
            next_word_id,
            "[UNK]"
        )
    )