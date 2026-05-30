import numpy as np
import tensorflow as tf

np.random.seed(42)
tf.random.set_seed(42)

# ---------------------------------------------------
# 1) Training data
# Features:
# [price_score, camera_score, battery_score, performance_score, software_support_score]
#
# Score range: 0 to 10
# Output:
# 1 = mobile lene layak
# 0 = mobile lene layak nahi
# ---------------------------------------------------
X_train = np.array([
    [8, 8, 8, 8, 8],   # good overall -> buy
    [7, 9, 8, 7, 8],   # good camera + balanced -> buy
    [6, 8, 7, 7, 7],   # decent overall -> buy
    [9, 6, 8, 8, 7],   # value for money + strong battery/performance -> buy
    [5, 9, 6, 6, 6],   # camera good but overall average -> maybe buy
    [3, 4, 5, 4, 3],   # weak phone -> don't buy
    [2, 5, 4, 3, 2],   # poor value -> don't buy
    [4, 3, 4, 5, 3],   # weak camera/software -> don't buy
    [6, 4, 5, 4, 4],   # average but not strong enough -> don't buy
    [7, 7, 6, 8, 7],   # good enough -> buy
    [8, 5, 9, 8, 6],   # battery/performance strong -> buy
    [3, 8, 4, 4, 3],   # camera alone is not enough -> don't buy
], dtype=np.float32)

# labels: 0 = fail, 1 = pass
y_train = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0], dtype=np.float32) # here we are deciding that if everything is good enough then we will label it as 1 (buy), and if there are significant weaknesses in the phone's features, we will label it as 0 (don't buy). This is a simple binary classification problem where we are trying to predict whether a mobile phone is worth buying based on its price score, camera score, battery score, performance score, and software support score.

# ---------------------------------------------------
# 2) Model create and store into model variable
# ---------------------------------------------------
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(5,)),
    tf.keras.layers.Dense(10, activation='relu'), # First layer = 4 neurons
    tf.keras.layers.Dense(6, activation='relu'),  # Second layer = 3 neurons
    tf.keras.layers.Dense(1, activation='sigmoid') # binary output,  Output layer = 1 neuron
], name="MobileBuyerModel")


# ---------------------------------------------------
# 3) Compile
# ---------------------------------------------------
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# ---------------------------------------------------
# 4) Train
# ---------------------------------------------------
model.fit(X_train, y_train, epochs=150, verbose=0) # Now here we are traing the model using the fit method, where we pass the training data (X_train and y_train), specify the number of epochs (100 in this case), and set verbose to 0 to suppress the training output. The model will learn to find patterns in the training data to predict whether a student will pass or fail based on their study hours, attendance percentage, and assignment completion.

# ---------------------------------------------------
# 5) Model ko save karo
# ---------------------------------------------------
model.save("MobileBuyerModel.keras")

'''
D:\xampp\htdocs\node\open_ai\src\ai_model\train_model_and_predict_or_ask_question
└── MobileBuyerModel.keras  ← Ye file permanent save ho jati hai
'''
print("Model saved successfully!")