import pandas as pd

# file dest and moving value time window configuration
SOURCE_CSV   = "../data/reactor_with_detection.csv"
DEST_CSV     = "../data/reactor_features.csv"
WINDOW_MIN   = 15

# read data
df = pd.read_csv(SOURCE_CSV, parse_dates=["Timestamp"]).set_index("Timestamp")

# decide which columns are 
reserved = {"Failure"} | {c for c in df.columns if c.startswith("Z_")}
sensor_cols = [c for c in df.columns if c not in reserved]

# build features
for col in sensor_cols:
    roll = df[col].rolling(f"{WINDOW_MIN}min", min_periods=1)
    df[f"{col}_mean"] = roll.mean()
    df[f"{col}_std"]  = roll.std()
    df[f"{col}_min"]  = roll.min()
    df[f"{col}_max"]  = roll.max()
    df[f"{col}_grad"] = df[col].diff()

# save
df.to_csv(DEST_CSV)
print(f"Features added.  Saved to {DEST_CSV}")
