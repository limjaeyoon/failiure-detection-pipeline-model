TITLE: READINESS PIPELINE FOR PI CONNECT

*PURPOSE*

    Build a generic, swappable time‑series pipeline that starts with
    synthetic reactor data and can be pointed at live OSIsoft PI tags
    the moment the PI AF SDK becomes available. 
    The current focus is failure detection in a petrochemical
    reactor using Z‑score rules and an Isolation‑Forest model.

*PROJECT FILE HIERARCHY*

    failiure-detection-pipeline-model/
    ├── data/                # CSV inputs & engineered datasets
    │   ├── reactor_multisensor_1day.csv        (raw synthetic)
    │   ├── reactor_features.csv                (with z‑scores)
    |   |__ reactor_with_predictions.csv        (raw synthetic + z score + moving average)
    │   └── reactor_predictions.csv             (model output)
    ├── outputs/             # figures, model artefacts, reports
    ├── src/                 # python source code
    │   ├── data_generation.py
    │   ├── data_exploration.py
    │   ├── data_exploration2.py
    │   ├── feature_engineering.py
    │   ├── detection.py
    │   |── model_training.py
    |   |__ model_prediction_visual.py
    └── README.txt

*.py DESCRIPTION*

    1. data_generation.py – Synthesises minute‑level reactor sensor data plus ground‑truth Failure labels.

    2. data_exploration.py – Quick EDA: summary stats & sanity‑check plots.

    3. data_exploration2.py – Deeper EDA: distributions, correlations, time‑series behaviour.

    4. feature_engineering.py – Derives Z_ columns & rolling features, writing reactor_features.csv.

    5. detection.py – Applies max‑|z| > 3 rule, outputs reactor_predictions.csv & confusion matrix.

    6. model_training.py – Fits IsolationForest on engineered features, prints precision/recall/F1.

    7. model_prediction_visual.py – Plots the confusion matrix and precision‑recall curve for any
                                    saved prediction set, exporting figures to outputs/.

*CURRENT STATUS*

    1. Synthetic dataset generated (24 h × 4 sensors, 1‑min resolution)
    2. Z‑scores & engineered features validated
    3. Rule‑based detection: Recall = 1.00, Precision ≈ 0.33
    4. Isolation‑Forest baseline trained and evaluated

*NEXT STEPS*

    1. main.py orchestration – single entry‑point chaining generation → exploration → features → detection/model
    2. all knobs (e.g. z‑score threshold, IsolationForest contamination) exposed in a global config file
    3. look for data applicable in the process / model here

LAST UPDATED: August 7th, 2025