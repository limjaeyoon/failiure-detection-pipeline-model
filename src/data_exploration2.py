import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

data_path = Path(__file__).resolve().parent.parent / "data" / "reactor_multisensor_1day.csv"
df = pd.read_csv(data_path, parse_dates=["Timestamp"])
outputs = Path(__file__).resolve().parent.parent / "outputs"
outputs.mkdir(exist_ok=True)

def plot_sensor(col):
    plt.figure(figsize=(10, 3))
    plt.plot(df["Timestamp"], df[col], lw=0.7)
    # mark injected failures
    fails = df[df["Failure"] == 1]
    plt.scatter(fails["Timestamp"], fails[col], color="red", zorder=5)
    plt.title(col)
    plt.tight_layout()
    out = outputs / f"{col.lower()}_trend.png"
    plt.savefig(out, dpi=150)
    plt.close()

plot_sensor("Temperature")
plot_sensor("Pressure")
plot_sensor("FlowRate")
