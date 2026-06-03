import sys
import yfinance as yf
import numpy as np
import joblib

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense

# Stock symbol
ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "AAPL"

print(f"Training model for {ticker}")

data = yf.download(
    ticker,
    start="2020-01-01",
    end="2026-06-01"
)

features = data[
    ['Open', 'High', 'Low', 'Close', 'Volume']
]

target = data[['Close']]

feature_scaler = MinMaxScaler()
target_scaler = MinMaxScaler()

scaled_features = feature_scaler.fit_transform(features)
scaled_target = target_scaler.fit_transform(target)

# Save scalers
joblib.dump(
    feature_scaler,
    f"{ticker}_feature_scaler.pkl"
)

joblib.dump(
    target_scaler,
    f"{ticker}_target_scaler.pkl"
)

X = []
y = []

sequence_length = 60

for i in range(sequence_length, len(scaled_features)):
    X.append(
        scaled_features[i-sequence_length:i]
    )

    # Close column = index 3

    y.append(
        scaled_target[i, 0]
    )

X = np.array(X)
y = np.array(y)

'''
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(60, 5)),
    LSTM(50),
    Dense(25),
    Dense(1)
])
'''

model = Sequential([
    GRU(50, return_sequences=True, input_shape=(60, 5)),
    GRU(50),
    Dense(25),
    Dense(1)
])

model.compile(
    optimizer="adam",
    loss="mean_squared_error"
)

model.fit(
    X,
    y,
    epochs=10,
    batch_size=32,
    verbose=1
)

model.save(
    f"{ticker}_stock_model.keras"
)

print(f"\nModel saved: {ticker}_stock_model.keras")
print(f"Scaler saved: {ticker}_feature_scaler.pkl")

# for train
# python train_stock.py AAPL
# python train_stock.py GOOGL
# python train_stock.py MSFT
# python train_stock.py TSLA