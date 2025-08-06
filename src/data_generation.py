import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Create timestamp range (1-minute intervals for 24 hours)
start_time = datetime(2025, 8, 1)
timestamps = [start_time + timedelta(minutes=i) for i in range(24 * 60)]

# Simulate signals
n = len(timestamps)
np.random.seed(42)

# Temperature: base + sine + noise
temperature = 100 + np.sin(np.linspace(0, 3 * np.pi, n)) * 5 + np.random.normal(0, 0.5, n)

# Pressure: positively correlated with temp, plus noise
pressure = temperature * 0.15 + np.random.normal(0, 0.2, n)

# FlowRate: mostly flat, occasional small dips
flowrate = 50 + np.random.normal(0, 0.2, n)
flowrate[np.random.choice(n, 10, replace=False)] -= 3

# CatalystLevel: slowly declining over time
catalyst = 100 - np.linspace(0, 5, n) + np.random.normal(0, 0.1, n)

# Inject 5 failure spikes
failures = np.zeros(n)
failure_indices = np.random.choice(range(300, n - 300), size=5, replace=False)
temperature[failure_indices] += np.random.choice([10, -15, 20], size=5)
pressure[failure_indices] += np.random.choice([5, -4], size=5)
failures[failure_indices] = 1

# Create DataFrame
df = pd.DataFrame({
    "Timestamp": timestamps,
    "Temperature": temperature,
    "Pressure": pressure,
    "FlowRate": flowrate,
    "CatalystLevel": catalyst,
    "Failure": failures.astype(int)
})

# ✅ Save to root-level /data folder
output_path = os.path.join(os.path.dirname(__file__), "..", "data", "reactor_multisensor_1day.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)

print(f"Data saved to {output_path}")
