import numpy as np
import tensorflow as tf

# 1) Sample training data
# features: [hours_studied, attendance_percent, assignments_done]
# Machine learning me input columns ko features bolte hain, aur jo output predict karna hai usko target/label bolte hain
'''
1 = hours studied
40 = attendance percent
0 = assignments done
Matlab first row ka meaning hua:
1 hour padha, 40% attendance thi, aur assignments 0 the.
'''

X_train = np.array([
    [1, 40, 0],
    [2, 45, 1],
    [2, 50, 0],
    [3, 60, 1],
    [4, 65, 1],
    [5, 70, 1],
    [6, 75, 1],
    [7, 80, 1],
    [8, 85, 1],
    [9, 90, 1]
], dtype=np.float32)

# labels: 0 = fail, 1 = pass
y_train = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1], dtype=np.float32) # here we are deciding that 4 hours of study and 65% attendance is the threshold for passing, so first 4 rows are labeled as 0 (fail) and the rest are labeled as 1 (pass) for training the model for X_train variable. This is a simple binary classification problem where we are trying to predict whether a student will pass or fail based on their study hours, attendance percentage, and assignment completion.

# 2) Model create and store into model variable
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(3,)),
    tf.keras.layers.Dense(8, activation='relu'), # First layer = 4 neurons
    tf.keras.layers.Dense(4, activation='relu'), # Second layer = 3 neurons
    tf.keras.layers.Dense(1, activation='sigmoid')  # binary output,  Output layer = 1 neuron
])

# 3) Compile
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# 4) Train
model.fit(X_train, y_train, epochs=100, verbose=0) # Now here we are traing the model using the fit method, where we pass the training data (X_train and y_train), specify the number of epochs (100 in this case), and set verbose to 0 to suppress the training output. The model will learn to find patterns in the training data to predict whether a student will pass or fail based on their study hours, attendance percentage, and assignment completion.

# 5) Test data
X_test = np.array([
    [2, 48, 0],   # expected fail
    [6, 78, 1],   # expected pass
    [3, 62, 1],   # maybe borderline
    [8, 88, 1]    # expected pass
], dtype=np.float32)

y_test = np.array([0, 1, 0, 1], dtype=np.float32)

# 6) Evaluate overall model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print("Test Accuracy:", accuracy)

# ----------------------------------------------------------
# Point 5 and 6 me humne test data create kiya aur model ko evaluate kiya, jisme humne dekha ki model ne test data par kitna achha perform kiya. Ab hum individual predictions ko validate karenge. Ye kewal Testing ke liye hai na ki training ke liye, kyunki humne model ko train karne ke liye alag data use kiya hai. Testing data se hum model ke generalization ability ko check karte hain, aur individual predictions se hum dekh sakte hain ki model ne har test sample par kya prediction kiya aur wo prediction sahi hai ya nahi. Niche hum individual predictions ko validate kar rahe hain, jisme hum har test sample ke input features, predicted probability, predicted label, actual label, aur prediction ki correctness ko print kar rahe hain. Isse hume pata chalega ki model ne har test sample par kya prediction kiya aur wo prediction sahi hai ya nahi.
# ----------------------------------------------------------

# 7) Predict
pred_probs = model.predict(X_test) # here we are using the predict method to get the predicted probabilities for each test sample. The output will be a value between 0 and 1, where values closer to 1 indicate a higher probability of passing and values closer to 0 indicate a higher probability of failing.
pred_labels = (pred_probs > 0.5).astype("int32")

# 8) Validate one by one
for i in range(len(X_test)):
    print("Input:", X_test[i])
    print("Predicted Probability:", float(pred_probs[i]))
    print("Predicted Label:", int(pred_labels[i]))
    print("Actual Label:", int(y_test[i]))
    print("Correct?" , int(pred_labels[i]) == int(y_test[i]))
    print("-" * 30)

'''
Is example me:
    X = input/features
    y = output/label
'''
		
# https://youtu.be/dl0p3XRBIuI?si=NDJZ9-ETolJbxfnw [Learn how create Model, complie, train, evaluate (Test) and predict (get data from model) ]
# with help of verbose = 1, we can track every steps of evaluate like number os steps one by one, loss and accuracy.
# in every steps, accuracy will increase and loss witll decrease
# we can use callback function if we want to stop epoch if accuracy is acchieved the target we decided.