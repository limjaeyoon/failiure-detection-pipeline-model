# main.py
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT.parent / "data"
OUT_DIR  = ROOT.parent / "outputs"

def run_script(script_name: str):
    script_path = ROOT / script_name
    if not script_path.exists():
        print(f"(skip) {script_name} not found.")
        return
    print(f"\n— Running {script_name} —")
    result = subprocess.run([sys.executable, str(script_path)], cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

def main():
    # Ensure folders exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Force mode: regenerating and OVERWRITING existing CSVs and plots.\n")

    # Always (re)generate data and overwrite files
    run_script("data_generation.py")

    # Always rerun detection, feature engineering, training, and visualization
    run_script("data_exploration.py")
    run_script("detection.py")
    run_script("feature_engineering.py")
    run_script("model_training.py")
    run_script("model_prediction_visual.py")

    print("\nDone. All artifacts were recomputed and saved over existing files.")

if __name__ == "__main__":
    main()
