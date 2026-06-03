import sys
import yfinance as yf
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import mplcursors
import matplotlib.dates as mdates

from pandas.tseries.offsets import BDay
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.models import load_model

# -------------------------
# Settings
# -------------------------

FUTURE_DAYS = 5
SEQUENCE_LENGTH = 60

# -------------------------
# Ticker
# -------------------------

ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "AAPL"

print(f"\nEvaluating model for {ticker}")

# -------------------------
# Load model and scaler
# -------------------------

model = load_model(
    f"{ticker}_stock_model.keras"
)

feature_scaler = joblib.load(
    f"{ticker}_feature_scaler.pkl"
)

target_scaler = joblib.load(
    f"{ticker}_target_scaler.pkl"
)

# -------------------------
# Download data
# -------------------------

data = yf.download(
    ticker,
    start="2024-01-01",
    progress=False
)

features = data[
    ['Open', 'High', 'Low', 'Close', 'Volume']
]

target = data[['Close']]

# -------------------------
# Scale data
# -------------------------

scaled_features = feature_scaler.transform(
    features
)

scaled_target = target_scaler.transform(
    target
)

# -------------------------
# Create evaluation sequences
# -------------------------

X_test = []
y_actual = []

for i in range(SEQUENCE_LENGTH, len(scaled_features)):

    X_test.append(
        scaled_features[
            i-SEQUENCE_LENGTH:i
        ]
    )

    y_actual.append(
        scaled_target[i,0]
    )

X_test = np.array(X_test)

X_test.reshape(
    (
        X_test.shape[0],
        60,
        5
    )
)

# -------------------------
# Historical Predictions
# -------------------------

predictions = model.predict(
    X_test,
    verbose=0
)

# -------------------------
# Convert back to prices
# -------------------------

predictions = target_scaler.inverse_transform(
    predictions
)

y_actual = np.array(
    y_actual,
    dtype=np.float64
).reshape(-1, 1)

y_actual = target_scaler.inverse_transform(
    y_actual
)

# -------------------------
# Historical dates
# -------------------------

dates = data.index[
    SEQUENCE_LENGTH:
]

# -------------------------
# Last 60 days
# -------------------------

last_n = 60

dates_plot = dates[-last_n:]

actual_plot = y_actual[
    -last_n:
].flatten()

pred_plot = predictions[
    -last_n:
].flatten()

# -------------------------
# Metrics
# -------------------------

mae = mean_absolute_error(
    actual_plot,
    pred_plot
)

latest_difference = abs(
    actual_plot[-1]
    -
    pred_plot[-1]
)

# -------------------------
# Console output
# -------------------------

print("\nLatest Comparison")
print("-" * 50)

print(
    f"Actual Price    : {actual_plot[-1]:.2f}"
)

print(
    f"Predicted Price : {pred_plot[-1]:.2f}"
)

print(
    f"Difference      : {latest_difference:.2f}"
)

print(
    f"MAE Error       : {mae:.2f}"
)

# -------------------------
# Interactive Plotly Chart
# -------------------------

fig = go.Figure()

# Actual Price
fig.add_trace(
    go.Scatter(
        x=dates_plot,
        y=actual_plot,
        mode="lines",
        name="Actual Price",
        hovertemplate=
        "<b>Date</b>: %{x}<br>" +
        "<b>Actual</b>: %{y:.2f}<extra></extra>"
    )
)

# Historical Prediction
fig.add_trace(
    go.Scatter(
        x=dates_plot,
        y=pred_plot,
        mode="lines",
        name="Historical Prediction",
        hovertemplate=
        "<b>Date</b>: %{x}<br>" +
        "<b>Predicted</b>: %{y:.2f}<extra></extra>"
    )
)


fig.update_layout(
    title=(
        f"{ticker} Stock Analysis<br>"
        f"MAE = {mae:.2f} | "
        f"Latest Difference = {latest_difference:.2f}"
    ),
    xaxis_title="Date",
    yaxis_title="Stock Price",
    hovermode="x unified",
    template="plotly_white",
    height=800
)

fig.show()

# Actual

plt.plot(
    dates_plot,
    actual_plot,
    linewidth=2,
    label="Actual Price"
)

# Historical prediction

plt.plot(
    dates_plot,
    pred_plot,
    linewidth=2,
    label="Historical Prediction"
)

# Latest actual point

plt.scatter(
    dates_plot[-1],
    actual_plot[-1],
    s=120
)

# Latest predicted point

plt.scatter(
    dates_plot[-1],
    pred_plot[-1],
    s=120
)

# =========================
# ADD THIS HERE
# =========================

cursor = mplcursors.cursor(hover=True)

@cursor.connect("add")
def on_add(sel):
    x, y = sel.target

    date = mdates.num2date(x)

    sel.annotation.set_text(
        f"Price: {y:.2f}\n"
        f"Date: {date.strftime('%Y-%m-%d')}"
    )

# =========================
# END
# =========================

plt.title(
    f"{ticker} Stock Analysis\n"
    f"MAE = {mae:.2f} | "
    f"Latest Difference = {latest_difference:.2f}",
    fontsize=14
)

plt.xlabel("Date")
plt.ylabel("Stock Price")

plt.xticks(
    rotation=45
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()

# for predict
# python evaluate_model.py AAPL
# python evaluate_model.py GOOGL
# python evaluate_model.py MSFT
# python evaluate_model.py TSLA