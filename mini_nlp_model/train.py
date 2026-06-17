import tensorflow as tf
import numpy as np

# Questions
questions = [
    "what is ai",
    "explain ai",
    "define ai",
    "tell me about ai",
    "what about ai",
    "ai meaning",
    "ai full form",

    "what is rag",
    "explain rag",
    "define rag",

    "what is mcp",
    "explain mcp",
    "define mcp",

    "what is langchain",
    "explain langchain",
    "tell me about langchain",
    "what about langchain",
    "langchain meaning",
    "langchain framework",

    "what is langgraph",
    "explain langgraph"
]

# Labels
labels = [
    0,0,0,0,0,0,0,
    1,1,1,
    2,2,2,
    3,3,3,3,3,3,
    4,4
]

# Convert text → numbers
vectorizer = tf.keras.layers.TextVectorization(
    max_tokens=1000,
    output_mode="int",
    output_sequence_length=10
)

vectorizer.adapt(questions)

# Model
model = tf.keras.Sequential([
    vectorizer,

    tf.keras.layers.Embedding(
        input_dim=1000,
        output_dim=16 # Each word will be represented by the model as a 16-number vector.
                        # "ai"
                        # ↓
                        # [0.23, -0.45, 0.12, ..., 0.88] means Total 16 values.
                        # that's why we call 16-dimensional embedding or 16-d embedding
    ),

    # 1000 × 16 = 16000
    # means:
    #     1000 possible tokens
    #     for every tokens 16 numbers
    #     so for embedding layer total 16000 parameterss

    # Now Dense layer: Dense(16) means Input: 16 neurons and Output: 16 neurons so total
    #                  16 × 16 = 256 weights, +16 bias = 272 parameters

    # Now Final layer: Dense(5) means Input: 16 neurons and Output: 5 classes so total
    #                  16 × 5 = 80, +5 bias = 85

    # Total:
    #         Embedding     16000
    #         Dense(16)       272
    #         Dense(5)         85
    #         -------------------
    #         Total         16357

    # So, Technically, model is approximately: 16.3k trainable parameters

    tf.keras.layers.GlobalAveragePooling1D(),

    tf.keras.layers.Dense(
        16,
        activation="relu"
    ),

    tf.keras.layers.Dense(
        5,
        activation="softmax"
    )
])

# Compile
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

questions = np.array(questions, dtype=object)
labels = np.array(labels)

# Train
model.fit(
    x=tf.constant(questions),
    y=tf.constant(labels),
    epochs=100,
    verbose=1
)

loss, acc = model.evaluate(
    tf.constant(questions),
    tf.constant(labels),
    verbose=0
)

# -----------------
# Question wise calculation
# ----------------
total = len(labels)
correct = round(acc * total)
incorrect = total - correct

# -----------------
# Accuracy and Loss
# ----------------
print("Accuracy:", acc)
print("Loss:", loss)
print(f"Accuracy in %: {acc * 100:.2f}%")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Out of your {total} examples, the model is correctly predicting approximately {correct} questions and {incorrect} incorrectly.")

# -----------------
# Vocabulary
# ----------------
print("Vocabulary", vectorizer.get_vocabulary())
vocab = vectorizer.get_vocabulary()
print(f"Index AI: {vocab.index('ai')}")
print(f"Index LangChain: {vocab.index('langchain')}")

# -----------------
# Embedding Weights
# ----------------
embedding_layer = model.layers[1]
weights = embedding_layer.get_weights()[0]
print(weights.shape)


# -----------------
# Vocabulary Weights
# ----------------
print("Embedding for AI:", weights[vocab.index('ai')])
print("Embedding for LangChain:", weights[vocab.index('langchain')])


# -----------------
# Model Summary
# ----------------
print("Model Summary", model.summary())

# Save model
model.save("mini_faq_model.keras")

print("Model saved!")