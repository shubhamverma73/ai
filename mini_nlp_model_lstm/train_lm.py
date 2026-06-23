import tensorflow as tf
import numpy as np

tf.random.set_seed(42)
np.random.seed(42)

'''
Mini Language Model

Instead of:

Question
↓
Class

We train:

Words
↓
Next Word
'''

sentences = [
    # AI

    "what is ai <END>",
    "explain ai <END>",
    "define ai <END>",
    "ai stands for artificial intelligence <END>",
    "artificial intelligence is a branch of computer science <END>",
    "ai helps machines learn patterns <END>",
    "ai can automate tasks <END>",
    "ai is used in healthcare <END>",
    "ai is used in robotics <END>",
    "ai is used in chatbots <END>",
    "ai can analyze large amounts of data <END>",
    "artificial intelligence can solve complex problems <END>",
    "machine learning is a part of ai <END>",
    "deep learning is a type of ai <END>",
    "ai powers recommendation systems <END>",
    "ai can recognize images <END>",
    "ai can understand text <END>",
    "ai can generate content <END>",
    "ai is transforming industries <END>",
    "ai can improve productivity <END>",

    # RAG

    "what is rag <END>",
    "explain rag <END>",
    "define rag <END>",
    "rag means retrieval augmented generation <END>",
    "rag combines retrieval and generation <END>",
    "rag fetches information before answering <END>",
    "rag improves factual responses <END>",
    "rag helps reduce hallucinations <END>",
    "rag uses external knowledge sources <END>",
    "rag can search documents before generating answers <END>",
    "rag improves answer accuracy <END>",
    "rag is useful for enterprise chatbots <END>",
    "rag connects llms with databases <END>",
    "rag retrieves relevant information <END>",
    "rag works with vector databases <END>",
    "rag is commonly used in question answering systems <END>",
    "rag can access private knowledge bases <END>",
    "rag improves context awareness <END>",
    "retrieval augmented generation combines search and generation <END>",
    "rag allows models to use fresh information <END>",

    # MCP

    "what is mcp <END>",
    "explain mcp <END>",
    "define mcp <END>",
    "mcp stands for model context protocol <END>",
    "mcp helps tools communicate with ai systems <END>",
    "mcp standardizes tool integration <END>",
    "mcp enables secure communication between models and tools <END>",
    "mcp simplifies ai integrations <END>",
    "mcp allows models to access external resources <END>",
    "mcp can connect ai with databases <END>",
    "mcp supports tool calling <END>",
    "mcp improves interoperability <END>",
    "mcp provides a common protocol <END>",
    "mcp can expose APIs to ai systems <END>",
    "mcp makes integrations easier <END>",

    # LangChain

    "what is langchain <END>",
    "explain langchain <END>",
    "langchain is a framework for llm applications <END>",
    "langchain helps developers build ai applications <END>",
    "langchain supports chains and agents <END>",
    "langchain works with language models <END>",
    "langchain can integrate tools <END>",
    "langchain can connect vector databases <END>",
    "langchain simplifies llm workflows <END>",
    "langchain supports memory components <END>",
    "langchain enables prompt engineering workflows <END>",
    "langchain is widely used in ai projects <END>",
    "langchain supports retrieval augmented generation <END>",
    "langchain helps orchestrate ai pipelines <END>",
    "langchain provides reusable components <END>",

    # LangGraph

    "what is langgraph <END>",
    "explain langgraph <END>",
    "define langgraph <END>",
    "langgraph is used for agent workflows <END>",
    "langgraph helps build stateful agents <END>",
    "langgraph supports graph based workflows <END>",
    "langgraph is useful for multi step reasoning <END>",
    "langgraph manages agent state <END>",
    "langgraph enables complex workflows <END>",
    "langgraph works with langchain <END>",
    "langgraph supports multi agent systems <END>",
    "langgraph helps coordinate agents <END>",
    "langgraph can manage execution flow <END>",
    "langgraph provides graph orchestration <END>",
    "langgraph is designed for advanced agent systems <END>"

]

# -----------------
# Vocabulary
# -----------------

vectorizer = tf.keras.layers.TextVectorization(
    max_tokens=1000,
    output_mode="int"
)

vectorizer.adapt(sentences)

vocab = vectorizer.get_vocabulary()

print("Vocabulary:")
print(vocab)

vocab_size = len(vocab)

# -----------------
# Build Training Data
# -----------------

X = []
Y = []

for sentence in sentences:

    tokens = vectorizer(
        tf.constant([sentence])
    ).numpy()[0]

    tokens = [t for t in tokens if t != 0]

    for i in range(1, len(tokens)):

        input_sequence = tokens[:i]

        target_word = tokens[i]

        X.append(input_sequence)

        Y.append(target_word)

# -----------------
# Padding
# -----------------

max_len = max(len(seq) for seq in X)

X = tf.keras.preprocessing.sequence.pad_sequences(
    X,
    maxlen=max_len,
    padding="pre"
)

Y = np.array(Y)

print("Training Samples:", len(X))
print("Max Sequence Length:", max_len)

# -----------------
# Model
# -----------------

model = tf.keras.Sequential([

    tf.keras.layers.Embedding(
        input_dim=vocab_size,
        output_dim=32,
        input_length=max_len
    ),

    tf.keras.layers.LSTM(64),

    tf.keras.layers.Dense(
        vocab_size,
        activation="softmax"
    )
])

# -----------------
# Compile
# -----------------

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# -----------------
# Train
# -----------------

history = model.fit(
    X,
    Y,
    epochs=200,
    verbose=1
)

print(
    "Final Accuracy:",
    history.history["accuracy"][-1]
)

# -----------------
# Save Model
# -----------------

model.save(
    "mini_language_model.keras"
)

# -----------------
# Save Vocabulary
# -----------------

import json

with open(
    "vocab.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        vocab,
        f,
        ensure_ascii=False,
        indent=4
    )

print("Model Saved!")