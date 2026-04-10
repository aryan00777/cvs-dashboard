import pandas as pd
import numpy as np

np.random.seed(42)

n = 20000  # 👉 bigger dataset

countries = ["Denmark", "Sweden", "Norway"]
channels = ["Organic", "Paid", "Direct"]
plans = ["Basic", "Premium", "Pro"]
devices = ["Mobile", "Desktop", "Tablet"]

# Time range (creates trends + seasonality)
dates = pd.date_range(start="2023-01-01", periods=n, freq="H")

# Base dataframe
df = pd.DataFrame({
    "user_id": range(1, n + 1),
    "signup_date": dates,
    "country": np.random.choice(countries, n),
    "channel": np.random.choice(channels, n, p=[0.5, 0.3, 0.2]),
    "plan": np.random.choice(plans, n, p=[0.5, 0.3, 0.2]),
    "device": np.random.choice(devices, n, p=[0.6, 0.3, 0.1]),
})

# --- Create realistic trends ---
time_factor = np.linspace(0.5, 1.5, n)  # growth over time
noise = np.random.normal(0, 0.2, n)     # randomness

# Plan pricing
price_map = {"Basic": 100, "Premium": 300, "Pro": 500}
df["price"] = df["plan"].map(price_map)

# Conversion probability influenced by channel + noise + trend
base_conversion = 0.3

channel_effect = df["channel"].map({
    "Organic": 0.1,
    "Paid": 0.15,
    "Direct": 0.05
}).values

conversion_prob = base_conversion + channel_effect + noise * 0.1

# Apply clipping (valid probabilities)
conversion_prob = np.clip(conversion_prob, 0.05, 0.9)

df["converted"] = np.random.binomial(1, conversion_prob)

# Funnel step
df["step"] = df["converted"].apply(
    lambda x: "completed" if x == 1 else np.random.choice(["signup", "form_started"])
)

# Revenue
df["revenue"] = df["converted"] * df["price"]

# Add session behavior (more realistic variability)
df["session_time"] = np.random.gamma(shape=2, scale=3, size=n).astype(int)

# Add some spikes (simulate campaigns)
spike_indices = np.random.choice(df.index, size=500, replace=False)
df.loc[spike_indices, "revenue"] *= 2

# Save CSV
df.to_csv("data.csv", index=False)

print("✅ Large realistic dataset created with", n, "rows")