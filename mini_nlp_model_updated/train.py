import tensorflow as tf
import numpy as np
from feedAI import qa_data
import json

tf.random.set_seed(42) # Random numbers are made repeatable.
np.random.seed(42)

'''
Why is it used in AI/ML?

Suppose you are training a model.
    Today, accuracy = 66%.
    Tomorrow, you run the same code, and accuracy = 62%.

This can happen due to random initialization.

By setting a seed:
    tf.random.set_seed(42)
    np.random.seed(42)

The results remain more consistent, making debugging and learning easier.
'''

# Questions
questions = [
    "what is ai",
    "explain ai",
    "define ai",
    "tell me about ai",
    "what about ai",
    "ai meaning",
    "ai full form",
    "what is artificial intelligence",
    "define artificial intelligence",
    "explain artificial intelligence",
    "artificial intelligence meaning",

    "what is rag",
    "explain rag",
    "define rag",
    "tell me about rag",
    "what about rag",
    "rag meaning",
    "retrieval augmented generation",
    "what is retrieval augmented generation",
    "define retrieval augmented generation",

    "what is mcp",
    "explain mcp",
    "define mcp",
    "tell me about mcp",
    "what about mcp",
    "mcp meaning",
    "model context protocol",
    "what is model context protocol",
    "define model context protocol",


    "what is langchain",
    "explain langchain",
    "tell me about langchain",
    "what about langchain",
    "langchain meaning",
    "langchain framework",

    "what is langgraph",
    "explain langgraph",
    "define langgraph",
    "tell me about langgraph",
    "what about langgraph",
    "langgraph meaning",
]

# Labels
labels = [
    0,0,0,0,0,0,0,0,0,0,0,
    1,1,1,1,1,1,1,1,1,
    2,2,2,2,2,2,2,2,2,
    3,3,3,3,3,3,
    4,4,4,4,4,4
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

    #tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(64, activation="relu"),

    tf.keras.layers.Dense(32, activation="relu"), # Newly added

    tf.keras.layers.Dense(5, activation="softmax")
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
history = model.fit( x=tf.constant(questions), y=tf.constant(labels), epochs=100, verbose=1 )

# -----------------
# Check training history
# ----------------
print("Training history accuracy", history.history["accuracy"][-1])
print("Training history loss", history.history["loss"][-1])

loss, acc = model.evaluate( tf.constant(questions), tf.constant(labels), verbose=0 )

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
print("Vocabulary", vectorizer.get_vocabulary()) # Vocabulary ['', '[UNK]', 'what', 'about', 'is', 'define', 'ai', 'rag', 'meaning', 'mcp', 'langgraph', 'langchain', 'explain', 'tell', 'me', 'intelligence', 'artificial', 'retrieval', 'protocol', 'model', 'generation', 'context', 'augmented', 'full', 'framework', 'form']
vocab = vectorizer.get_vocabulary()
print(f"Index AI: {vocab.index('ai')}")
print(f"Index LangChain: {vocab.index('langchain')}")

# -----------------
# Embedding Weights
# ----------------
embedding_layer = model.layers[1]
weights = embedding_layer.get_weights()[0]
print(weights.shape)

# --------------------
# Just for Testing How Tocknization work
# --------------------
print("Tocknization for 'what is ai': ", vectorizer(tf.constant(["what is ai"])).numpy()) # it should be like this [[2 4 6 0 0 0 0 0 0 0]] based on Vocabulary position

print("Tocknization for 'AI': ", vectorizer(tf.constant(["AI"])).numpy()) # it should be like this [[6 0 0 0 0 0 0 0 0 0]] because at Vocabulary its position is at 6
print("Tocknization for 'LangChain': ", vectorizer(tf.constant(["LangChain"])).numpy())


# -----------------
# Vocabulary Weights
# ----------------
print("Embedding for AI:", weights[vocab.index('ai')])
print("Embedding for LangChain:", weights[vocab.index('langchain')])


# -----------------
# Model Summary
# ----------------
print("Model Summary", model.summary())


# -----------------
# Which questions is the model misclassifying?
# ----------------
preds = model.predict( tf.constant(questions), verbose=0 )

for q, actual, pred in zip( questions, labels, np.argmax(preds, axis=1) ):
    print( f"{q:25} actual={actual} pred={pred}" )


# -----------------
# Predict Question
# ----------------
print(np.argmax(model.predict(tf.constant(["what is ai"]), verbose=0)))
print(np.argmax(model.predict(tf.constant(["what is langchain"]), verbose=0)))

# -----------------
# Save Label Mapping
# -----------------
label_mapping = {}

for item in qa_data:
    label_mapping[item["label"]] = item["answer"]

with open("label_mapping.json", "w", encoding="utf-8") as f:
    json.dump(
        label_mapping,
        f,
        ensure_ascii=False,
        indent=4
    )

print("Label mapping saved!")

# Save model
model.save("mini_faq_model.keras")
print("Model saved!")


'''
Aapke code me ye layer:

    vectorizer = tf.keras.layers.TextVectorization(
        max_tokens=1000,
        output_mode="int",
        output_sequence_length=10
    )

aur:

    vectorizer.adapt(questions)

text ko tokens/integers me convert karti hai.

Example

Input:

    what is ai

Vocabulary banne ke baad kuch aisa ho sakta hai:

    what  -> 2
    is    -> 3
    ai    -> 4

To:

    "what is ai"
            ↓
    [2, 3, 4, 0, 0, 0, 0, 0, 0, 0]

Ye tokenization + numerical encoding hai.

Phir next layer:

    tf.keras.layers.Embedding(
        input_dim=1000,
        output_dim=16
    )

ye token IDs ko embeddings me convert karti hai.

Example:

    Token ID 4 ("ai")
            ↓
    [0.23, -0.45, 0.12, ..., 0.88]

16 numbers ka vector ban gaya.

Aapke model ka actual flow

    "what is ai"
        ↓
    TextVectorization
        ↓
    [2, 3, 4, 0, 0, 0, 0, 0, 0, 0]
        ↓
    Embedding Layer
        ↓
    [
    [0.12, ...],   ← what
    [0.55, ...],   ← is
    [0.23, ...],   ← ai
    ...
    ]
        ↓
    GlobalAveragePooling1D
        ↓
    Dense Layers
        ↓
    Softmax
        ↓
    Class Prediction

-------------------------------------------------------
Actual Tokenization

Agar input hai:

    what is ai

to tokenization ke baad:

    ["what", "is", "ai"]

milta hai.

Phir vocabulary use karke ye token IDs me convert hota hai:

    ["what", "is", "ai"]
        ↓
        [2, 4, 6]

Aur kyunki aapne:

    output_sequence_length=10

rakha hai, to padding bhi lagegi:

    [2, 4, 6, 0, 0, 0, 0, 0, 0, 0]

Yahi actual output hai jo Embedding layer me jata hai.

Aap khud verify kar sakte hain:

    print(vectorizer(tf.constant(["what is ai"])).numpy())

Output kuch aisa aayega:

    [[2 4 6 0 0 0 0 0 0 0]]

Ye tokenization + integer encoding ka final result hai.
'''