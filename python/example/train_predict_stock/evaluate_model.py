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

scaler = joblib.load(
    f"{ticker}_scaler.pkl"
)

# -------------------------
# Download data
# -------------------------

data = yf.download(
    ticker,
    start="2024-01-01",
    progress=False
)

close_prices = data[['Close']]

# -------------------------
# Scale data
# -------------------------

scaled_data = scaler.transform(
    close_prices
)

# -------------------------
# Create evaluation sequences
# -------------------------

X_test = []
y_actual = []

for i in range(SEQUENCE_LENGTH, len(scaled_data)):

    X_test.append(
        scaled_data[
            i - SEQUENCE_LENGTH:i,
            0
        ]
    )

    y_actual.append(
        float(
            scaled_data[i, 0]
        )
    )

X_test = np.array(X_test)

X_test = X_test.reshape(
    (
        X_test.shape[0],
        X_test.shape[1],
        1
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

predictions = scaler.inverse_transform(
    predictions
)

y_actual = np.array(
    y_actual,
    dtype=np.float64
).reshape(-1, 1)

y_actual = scaler.inverse_transform(
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
# Future Forecast
# -------------------------

current_sequence = scaled_data[
    -SEQUENCE_LENGTH:
]

future_predictions = []

for _ in range(FUTURE_DAYS):

    X_future = np.array(
        [current_sequence]
    )

    X_future = X_future.reshape(
        (
            1,
            SEQUENCE_LENGTH,
            1
        )
    )

    pred = model.predict(
        X_future,
        verbose=0
    )

    future_predictions.append(
        pred[0][0]
    )

    current_sequence = np.vstack(
        [
            current_sequence[1:],
            pred
        ]
    )

future_predictions = np.array(
    future_predictions
).reshape(-1, 1)

future_prices = scaler.inverse_transform(
    future_predictions
)

print("\nFuture Forecast")
print("-" * 50)

for i, price in enumerate(
    future_prices,
    start=1
):
    print(
        f"Day {i}: {price[0]:.2f}"
    )

# -------------------------
# Future Dates
# -------------------------

last_date = dates_plot[-1]

future_dates = pd.date_range(
    start=last_date + BDay(1),
    periods=FUTURE_DAYS,
    freq="B"
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

# Future Forecast
fig.add_trace(
    go.Scatter(
        x=future_dates,
        y=future_prices.flatten(),
        mode="lines+markers",
        name="Future Forecast",
        line=dict(dash="dash"),
        hovertemplate=
        "<b>Future Date</b>: %{x}<br>" +
        "<b>Forecast</b>: %{y:.2f}<extra></extra>"
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

# Future forecast

plt.plot(
    future_dates,
    future_prices.flatten(),
    linestyle="--",
    marker="o",
    linewidth=3,
    label="Future Forecast"
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