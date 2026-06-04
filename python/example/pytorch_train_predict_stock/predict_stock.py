import sys
import yfinance as yf
import numpy as np
import joblib

import torch
import torch.nn as nn

FUTURE_DAYS = 5

ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "AAPL"

# --------------------
# Model Definition
# --------------------
class StockGRU(nn.Module):

    def __init__(self):

        super().__init__()

        self.gru = nn.GRU(
            input_size=1,
            hidden_size=50,
            batch_first=True
        )

        self.fc1 = nn.Linear(
            50,
            25
        )

        self.fc2 = nn.Linear(
            25,
            1
        )

    def forward(self, x):

        output, hidden = self.gru(x)

        x = hidden[-1]

        x = self.fc1(x)

        x = self.fc2(x)

        return x

# --------------------
# Load Model
# --------------------
model = StockGRU()

model.load_state_dict(
    torch.load(
        f"{ticker}_stock_model.pth"
    )
)

model.eval()

# --------------------
# Load Scaler
# --------------------
scaler = joblib.load(
    f"{ticker}_scaler.pkl"
)

# --------------------
# Latest Data
# --------------------
data = yf.download(
    ticker,
    period="6mo",
    progress=False
)

close_prices = data[['Close']]

scaled_data = scaler.transform(
    close_prices
)

current_sequence = scaled_data[-60:]

# --------------------
# Future Prediction
# --------------------
predictions = []

for _ in range(FUTURE_DAYS):

    X_test = torch.tensor(
        current_sequence,
        dtype=torch.float32
    )

    X_test = X_test.unsqueeze(0)

    with torch.no_grad():

        pred = model(X_test)

    pred_value = pred.item()

    predictions.append(
        pred_value
    )

    current_sequence = np.vstack([
        current_sequence[1:],
        [[pred_value]]
    ])

# --------------------
# Convert Back
# --------------------
predictions = np.array(
    predictions
).reshape(-1,1)

prices = scaler.inverse_transform(
    predictions
)

# --------------------
# Output
# --------------------
print("\nForecast:\n")

for i, price in enumerate(
    prices,
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