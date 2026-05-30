import tensorflow as tf
import numpy as np

# ---------------------------------------------------
# 1) Model load karo (data se train nahi karna pade)
# ---------------------------------------------------
loaded_model = tf.keras.models.load_model("MobileBuyerModel.keras")

# ---------------------------------------------------
# 2) New mobile set karo jiska decision lena hai
# [price_score, camera_score, battery_score, performance_score, software_support_score]
# ---------------------------------------------------
#new_mobile = np.array([[0, 2, 7, 8, 1]], dtype=np.float32)
new_mobile = np.array([[8, 8, 7, 8, 8]], dtype=np.float32)

# ---------------------------------------------------
# 3) Sirf prediction karo
# ---------------------------------------------------
new_prob = loaded_model.predict(new_mobile, verbose=0)[0][0]
new_label = 1 if new_prob >= 0.5 else 0

# ---------------------------------------------------
# 4) Result show karo
# ---------------------------------------------------
print("--- New Mobile Decision ---")
print("Features:", new_mobile[0].tolist())
print("Buy probability:", round(float(new_prob), 4))

if new_label == 1:
    print("Result: Ye mobile lene layak hai.")
else:
    print("Result: Ye mobile lene layak nahi hai.")