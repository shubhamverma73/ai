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

close_prices = data[['Close']]

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(close_prices)

# Save scaler
joblib.dump(
    scaler,
    f"{ticker}_scaler.pkl"
)

X = []
y = []

sequence_length = 60

for i in range(sequence_length, len(scaled_data)):
    X.append(scaled_data[i-sequence_length:i, 0])
    y.append(scaled_data[i, 0])

X = np.array(X)
y = np.array(y)

X = X.reshape((X.shape[0], X.shape[1], 1))

'''
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(60, 1)),
    LSTM(50),
    Dense(25),
    Dense(1)
])
'''

model = Sequential([
    GRU(50, return_sequences=True, input_shape=(60, 1)),
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
print(f"Scaler saved: {ticker}_scaler.pkl")

# for train
# python train_stock.py AAPL
# python train_stock.py GOOGL
# python train_stock.py MSFT
# python train_stock.py TSLA