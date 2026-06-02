import numpy as np
import tensorflow as tf

# Seed fix karo - har baar same result aayega
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

y_train = np.array([
    1, 1, 1, 1, 1,
    0, 0, 0, 0, 1,
    1, 0
], dtype=np.float32)

# ---------------------------------------------------
# 2) Model create and store into model variable
# ---------------------------------------------------
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(5,)),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(6, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
], name="MobileBuyerModel")

# ---------------------------------------------------
# 3) Compile
# ---------------------------------------------------
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ---------------------------------------------------
# 4) Train
# ---------------------------------------------------
model.fit(X_train, y_train, epochs=150, verbose=0)

# ---------------------------------------------------
# 5) Test data
# ---------------------------------------------------
X_test = np.array([
    [8, 9, 8, 8, 8],   # expected buy
    [3, 4, 4, 3, 3],   # expected don't buy
    [6, 7, 6, 6, 6],   # borderline
    [9, 5, 9, 9, 7],   # expected buy
], dtype=np.float32)

y_test = np.array([1, 0, 1, 1], dtype=np.float32)

# ---------------------------------------------------
# 6) Evaluate
# ---------------------------------------------------
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print("Test Accuracy:", round(float(accuracy), 4))

# ---------------------------------------------------
# 7) Predict
# ---------------------------------------------------
pred_probs = model.predict(X_test, verbose=0)
pred_labels = (pred_probs >= 0.5).astype("int32")

print("\n--- Prediction Results ---")
for i in range(len(X_test)):
    print(f"\nMobile {i+1}")
    print("Features:", X_test[i].tolist())
    print("Predicted probability:", round(float(pred_probs[i][0]), 4))
    print("Predicted label:", int(pred_labels[i][0]))
    print("Actual label:", int(y_test[i]))
    print("Correct?:", int(pred_labels[i][0]) == int(y_test[i]))
    print("-" * 30)

# ---------------------------------------------------
# 8) New mobile check
# ---------------------------------------------------
# [price_score, camera_score, battery_score, performance_score, software_support_score]
#new_mobile = np.array([[7, 8, 7, 8, 7]], dtype=np.float32)
new_mobile = np.array([[0, 2, 7, 8, 1]], dtype=np.float32)

new_prob = model.predict(new_mobile, verbose=0)[0][0]
new_label = 1 if new_prob >= 0.5 else 0

print("\n--- New Mobile Decision ---")
print("Features:", new_mobile[0].tolist())
print("Buy probability:", round(float(new_prob), 4))

if new_label == 1:
    print("Result: Ye mobile lene layak hai.")
else:
    print("Result: Ye mobile lene layak nahi hai.")
		
# https://youtu.be/dl0p3XRBIuI?si=NDJZ9-ETolJbxfnw [Learn how create Model, complie, train, evaluate (Test) and predict (get data from model) ]
# with help of verbose = 1, we can track every steps of evaluate like number os steps one by one, loss and accuracy.
# in every steps, accuracy will increase and loss witll decrease
# we can use callback function if we want to stop epoch if accuracy is acchieved the target we decided. (https://github.com/shubhamverma73/ai/blob/main/python/tensorform/Stop%20epoch%20if%20accuracy%20target%20acchieved.ipynb)