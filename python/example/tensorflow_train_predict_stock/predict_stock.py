import sys
import yfinance as yf
import numpy as np
import joblib

from tensorflow.keras.models import load_model

# ==========================
# Settings
# ==========================
FUTURE_DAYS = 5

# ==========================
# Get Stock Symbol
# ==========================
ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "AAPL"

print(f"\nPredicting next {FUTURE_DAYS} trading days for {ticker}")

# ==========================
# Load Model & Scaler
# ==========================
model = load_model(
    f"{ticker}_stock_model.keras"
)

scaler = joblib.load(
    f"{ticker}_scaler.pkl"
)

# ==========================
# Download Latest Data
# ==========================
data = yf.download(
    ticker,
    period="6mo",
    progress=False
)

if len(data) < 60:
    raise Exception(
        "Not enough data available."
    )

close_prices = data[['Close']]

# ==========================
# Scale Data
# ==========================
scaled_data = scaler.transform(
    close_prices
)

# Last 60 days
current_sequence = scaled_data[-60:]

# ==========================
# Predict Next 5 Days
# ==========================
predictions = []

for day in range(FUTURE_DAYS):

    X_test = np.array([current_sequence])
    X_test = X_test.reshape((1, 60, 1))

    pred = model.predict(
        X_test,
        verbose=0
    )

    predictions.append(
        pred[0][0]
    )

    # Remove first value and append prediction
    current_sequence = np.vstack([
        current_sequence[1:],
        pred
    ])

# ==========================
# Convert Back To Real Price
# ==========================
predictions = np.array(
    predictions
).reshape(-1, 1)

predicted_prices = scaler.inverse_transform(
    predictions
)

# ==========================
# Output
# ==========================
print("\nForecast:")

for i, price in enumerate(
    predicted_prices,
    start=1
):
    print(
        f"Day {i}: ${price[0]:.2f}"
    )

# for predict
# python predict_stock.py AAPL
# python predict_stock.py GOOGL
# python predict_stock.py MSFT
# python predict_stock.py TSLA