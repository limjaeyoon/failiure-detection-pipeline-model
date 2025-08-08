# data_generation.py
from pathlib import Path
import numpy as np
import pandas as pd

# -----------------------------
# Simple configuration knobs
# -----------------------------
N_MINUTES = 24 * 60            # 1440 rows
NUM_FAILURES = 5               # total failure points to inject
START_TIME = "2025-08-01 00:00:00"  # fixed date for readability (can change)

# Output goes to project_root/data
DATA_DIR = (Path(__file__).resolve().parents[1] / "data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = DATA_DIR / "reactor_multisensor_1day.csv"

def generate_base_signals(n: int) -> pd.DataFrame:
    """Create baseline reactor signals with mild noise and drift."""
    # Time index (1-minute frequency)
    ts = pd.date_range(START_TIME, periods=n, freq="T")

    # Small random walks (drift) + white noise for realism
    rng = np.random.default_rng()  # no fixed seed => different each run

    temp = 100 + np.cumsum(rng.normal(0, 0.02, n)) + rng.normal(0, 0.8, n)
    press = 15 + np.cumsum(rng.normal(0, 0.002, n)) + rng.normal(0, 0.15, n)
    flow = 50 + np.cumsum(rng.normal(0, 0.01, n)) + rng.normal(0, 0.25, n)
    catalyst = 100 + np.cumsum(rng.normal(0, 0.01, n)) + rng.normal(0, 0.2, n)

    df = pd.DataFrame(
        {
            "Timestamp": ts,
            "Temperature": temp,
            "Pressure": press,
            "FlowRate": flow,
            "CatalystLevel": catalyst,
        }
    )
    df["Failure"] = 0  # binary ground truth
    return df

def inject_random_failures(df: pd.DataFrame, k: int) -> pd.DataFrame:
    """
    Flip 'Failure' to 1 at k random, unique indices and create clear sensor outliers
    at those exact rows. Minimal, surgical perturbations; single-point events.
    """
    n = len(df)
    rng = np.random.default_rng()  # independent generator (still no fixed seed)

    # Choose k unique indices anywhere in the range [0, n)
    failure_idxs = rng.choice(n, size=min(k, n), replace=False)

    # Apply outlier-like spikes/drops at each chosen row
    for idx in failure_idxs:
        # Randomly choose sign per signal to diversify patterns
        s_temp = rng.choice([-1, 1])
        s_press = rng.choice([-1, 1])
        s_flow = rng.choice([-1, 1])
        s_cat = rng.choice([-1, 1])

        # Push values far from their typical scale so z-score will pop
        df.at[idx, "Temperature"] += s_temp * rng.uniform(8.0, 15.0)   # big swing
        df.at[idx, "Pressure"]    += s_press * rng.uniform(1.5, 3.0)
        df.at[idx, "FlowRate"]    += s_flow * rng.uniform(1.0, 2.5)
        df.at[idx, "CatalystLevel"] += s_cat * rng.uniform(1.0, 2.5)

        df.at[idx, "Failure"] = 1

    return df

def main():
    df = generate_base_signals(N_MINUTES)
    df = inject_random_failures(df, NUM_FAILURES)

    # Save (overwrite) to ../data
    df.to_csv(OUT_CSV, index=False)
    print(f"Saved {len(df):,} rows to {OUT_CSV}")

    # Quick sanity check printout
    pos = int(df["Failure"].sum())
    print(f"Injected failures: {pos} (random indices each run)")

if __name__ == "__main__":
    main()
