import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    confusion_matrix, precision_recall_fscore_support, classification_report
)

# settings - for convenience
SOURCE_CSV       = "../data/reactor_features.csv" 
DEST_CSV         = "../data/reactor_predictions.csv"
CONTAMINATION    = 0.01 #look for a better threshold value after researching data
# or maybe conducting multiple model & tests based on it could be a better idea
RANDOM_STATE     = 42

# Data load
df = pd.read_csv(SOURCE_CSV, parse_dates=["Timestamp"])

# Select feature columns
reserved = {"Timestamp", "Failure", "DetectedFailure"}
feature_cols = [c for c in df.columns if c not in reserved]
X = df[feature_cols].values

# Fit Isolation Forest
iso = IsolationForest(
    n_estimators=200,
    contamination=CONTAMINATION,
    random_state=RANDOM_STATE,
)
iso.fit(X)

# Score & predict
df["IsoScore"] = iso.decision_function(X)            # higher = normal
df["IsoPred"]  = (iso.predict(X) == -1).astype(int)  # -1 → anomaly → 1

# 5. Evaluation
y_true = df["Failure"].astype(int).values
y_pred = df["IsoPred"].values

cm = confusion_matrix(y_true, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(
    y_true, y_pred, average="binary", zero_division=0
)

print("Confusion matrix [ [TN FP] [FN TP] ]:")
print(cm)
print(f"Precision: {precision:0.3f}  Recall: {recall:0.3f}  F1: {f1:0.3f}")

print("\nDetailed classification report:\n")
print(classification_report(y_true, y_pred, digits=3, zero_division=0))

# 6. print results
df.to_csv(DEST_CSV, index=False)
print(f"\nPredictions saved to {DEST_CSV}")