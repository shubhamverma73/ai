import sys
import yfinance as yf
import numpy as np
import joblib

import torch
import torch.nn as nn

from sklearn.preprocessing import MinMaxScaler

# --------------------
# Settings
# --------------------
ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "AAPL"

SEQUENCE_LENGTH = 60

# --------------------
# Download Data
# --------------------
data = yf.download(
    ticker,
    start="2020-01-01",
    end="2026-06-01"
)

close_prices = data[['Close']]

# --------------------
# Scale Data
# --------------------
scaler = MinMaxScaler()

scaled_data = scaler.fit_transform(
    close_prices
)

joblib.dump(
    scaler,
    f"{ticker}_scaler.pkl"
)

# --------------------
# Create Sequences
# --------------------
X = []
y = []

for i in range(
    SEQUENCE_LENGTH,
    len(scaled_data)
):

    X.append(
        scaled_data[
            i-SEQUENCE_LENGTH:i
        ]
    )

    y.append(
        scaled_data[i]
    )

X = np.array(X)
y = np.array(y)

# --------------------
# Convert To Tensor
# --------------------
X = torch.tensor(
    X,
    dtype=torch.float32
)

y = torch.tensor(
    y,
    dtype=torch.float32
)

# --------------------
# GRU Model
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
# Create Model
# --------------------
model = StockGRU()

loss_fn = nn.MSELoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

# --------------------
# Training
# --------------------
epochs = 150

for epoch in range(epochs):

    prediction = model(X)

    loss = loss_fn(
        prediction,
        y
    )

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    print(
        f"Epoch {epoch+1}/{epochs} "
        f"Loss={loss.item():.6f}"
    )

# --------------------
# Save Model
# --------------------
torch.save(
    model.state_dict(),
    f"{ticker}_stock_model.pth"
)

print("\nModel Saved")

# for train
# python train_stock.py AAPL
# python train_stock.py GOOGL
# python train_stock.py MSFT
# python train_stock.py TSLA