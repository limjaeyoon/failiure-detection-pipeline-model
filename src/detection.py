import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import confusion_matrix, classification_report

data_path = Path(__file__).resolve().parent.parent / "data" / "reactor_multisensor_1day.csv"
df = pd.read_csv(data_path, parse_dates=["Timestamp"]).set_index("Timestamp")

# rolling Z-scores
window = 30          # 30-minute centred window
for col in ["Temperature", "Pressure", "FlowRate", "CatalystLevel"]:
    mean = df[col].rolling(window, center=True).mean()
    std  = df[col].rolling(window, center=True).std()
    df[f"Z_{col}"] = (df[col] - mean) / std

# rule-based flag: any |Z| > 3
df["DetectedFailure"] = (df[[c for c in df.columns if c.startswith("Z_")]]
                         .abs().gt(3).any(axis=1).astype(int))

# confusion matrix
y_true = df["Failure"]
y_pred = df["DetectedFailure"]
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
print(f"TP {tp} | FP {fp} | FN {fn} | TN {tn}")

out_csv = Path(__file__).resolve().parent.parent / "outputs" / "reactor_with_detection.csv"
out_csv.parent.mkdir(exist_ok=True)
df.to_csv(out_csv)
print("Saved results to outputs/reactor_with_detection.csv")

print(confusion_matrix(df["Failure"], df["DetectedFailure"]))
print(classification_report(df["Failure"], df["DetectedFailure"], digits=3))