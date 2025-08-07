import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
from pathlib import Path          # NEW

# Paths
DATA_CSV   = "../data/reactor_predictions.csv"
OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Load predictions
df = pd.read_csv(DATA_CSV, parse_dates=["Timestamp"])

# Timeline plot of predictions vs. truth
fig1, ax = plt.subplots(figsize=(12, 3))
ax.plot(df["Timestamp"], df["IsoScore"], label="Isolation-Forest score")
ax.scatter(df.loc[df["IsoPred"] == 1, "Timestamp"],
           df.loc[df["IsoPred"] == 1, "IsoScore"],
           marker="x", s=40, label="Model flagged", zorder=3)
ax.scatter(df.loc[df["Failure"] == 1, "Timestamp"],
           df.loc[df["Failure"] == 1, "IsoScore"],
           marker="o", facecolors="none", edgecolors="r",
           label="Real failure", zorder=4)

ax.set_title("Model score timeline – circles = real failures, x = model flags")
ax.set_xlabel("Time")
ax.set_ylabel("Isolation-Forest decision_function")
ax.legend(loc="upper right")
fig1.tight_layout()

# Confusion-matrix heat-map
y_true = df["Failure"].astype(int).values
y_pred = df["IsoPred"].values
cm = confusion_matrix(y_true, y_pred)

fig2, ax2 = plt.subplots(figsize=(3, 3))
im = ax2.imshow(cm, cmap="Blues")
ax2.set_xticks([0, 1]); ax2.set_yticks([0, 1])
ax2.set_xticklabels(["Pred 0", "Pred 1"]); ax2.set_yticklabels(["True 0", "True 1"])
ax2.set_xlabel("Predicted"); ax2.set_ylabel("Actual")
ax2.set_title("Confusion Matrix")

for i in range(2):
    for j in range(2):
        ax2.text(j, i, cm[i, j], ha="center", va="center", fontsize=12)

fig2.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
fig2.tight_layout()

# Save files
fig1.savefig(OUTPUT_DIR / "timeline.png", dpi=150)
fig2.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=150)
print(f"Saved timeline.png and confusion_matrix.png to {OUTPUT_DIR}")

# plt.show()