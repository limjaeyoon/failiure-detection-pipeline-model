import pandas as pd
import matplotlib.pyplot as plt
import os

# Load dataset
df = pd.read_csv("../data/reactor_multisensor_1day.csv", parse_dates=["Timestamp"])

# Make sure output folder exists
os.makedirs("../outputs", exist_ok=True)

# Set plotting style
plt.style.use("seaborn-v0_8")

# Plot each sensor with failures highlighted
def plot_sensor(sensor: str):
    plt.figure(figsize=(12, 4))
    plt.plot(df["Timestamp"], df[sensor], label=sensor, color="blue")
    plt.scatter(df["Timestamp"][df["Failure"] == 1],
                df[sensor][df["Failure"] == 1],
                color="red", label="Failure", zorder=5)
    plt.title(f"{sensor} over Time with Failures")
    plt.xlabel("Timestamp")
    plt.ylabel(sensor)
    plt.legend()
    plt.tight_layout()
    
    # Save to outputs/
    plot_path = f"../outputs/{sensor.lower()}_trend.png"
    plt.savefig(plot_path)
    print(f"📊 Saved plot: {plot_path}")
    plt.close()

# Plot selected sensors
plot_sensor("Temperature")
plot_sensor("Pressure")
plot_sensor("FlowRate")
