import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import random

# scaffold a 1-minute index for one day 
start = datetime(2025, 8, 1, 0, 0)
timestamps = [start + timedelta(minutes=i) for i in range(24 * 60)]

# build four correlated sensor series 
rng = np.random.default_rng(seed=42)
temperature   = 100 + rng.normal(0, 0.8, 1440).cumsum() / 50
pressure      = 15  + rng.normal(0, 0.05, 1440).cumsum() / 50
flow_rate     = 50  + rng.normal(0, 0.6, 1440).cumsum() / 50
catalyst_lvl  = 100 + rng.normal(0, 1.0, 1440).cumsum() / 50

df = pd.DataFrame({
    "Timestamp"     : timestamps,
    "Temperature"   : temperature,
    "Pressure"      : pressure,
    "FlowRate"      : flow_rate,
    "CatalystLevel" : catalyst_lvl,
    "Failure"       : 0               # ground-truth label placeholder
})

# inject five failure spikes & label them
failure_rows = random.sample(range(240, 1200), 5)      # avoid first/last 4 h
df.loc[failure_rows, ["Temperature", "Pressure",
                      "FlowRate", "CatalystLevel"]] *= [0.95, 1.12, 1.15, 1.03]
df.loc[failure_rows, "Failure"] = 1

# save
data_dir = Path(__file__).resolve().parent.parent / "data"
data_dir.mkdir(exist_ok=True)
output_path = data_dir / "reactor_multisensor_1day.csv"
df.to_csv(output_path, index=False)

print(f"Data saved to {output_path}")
