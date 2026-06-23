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
# Generate Text
# -----------------

while True:

    text = input("\nInput: ").lower()

    generated_text = text

    # How many new words to generate
    max_new_words = 10

    for _ in range(max_new_words):

        words = generated_text.split()

        sequence = []

        for word in words:

            if word in word_to_id:
                sequence.append(
                    word_to_id[word]
                )

        if len(sequence) == 0:

            print("Unknown words")
            break

        sequence = tf.keras.preprocessing.sequence.pad_sequences(
            [sequence],
            maxlen=5,
            padding="pre"
        )

        prediction = model.predict(
            sequence,
            verbose=0
        )

        # Top prediction
        top5 = np.argsort(
            prediction[0]
        )[-5:]

        top5_probs = prediction[0][top5]

        top5_probs = top5_probs / np.sum(top5_probs)

        next_word_id = np.random.choice(
            top5,
            p=top5_probs
        )

        next_word_id = np.random.choice(top5)

        next_word = id_to_word.get(
            next_word_id,
            "[UNK]"
        )

        if next_word == "<END>":
            break

        generated_text += " " + next_word

    print("\nGenerated:")
    print(generated_text)