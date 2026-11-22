
import json
from pathlib import Path

import joblib
import pandas as pd
import math


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "trained_models" / "yield_model.pkl"
FEATURE_COLUMNS_PATH = BASE_DIR / "trained_models" / "yield_feature_columns.json"

# Original input fields used during model training
NUMERICAL_FEATURES = [
    "Year",
    "Temperature",
    "Rainfall",
    "Humidity",
    "pH",
    "Nitrogen",
    "Phosphorus",
    "Potassium",
    "Fertilizer",
    "Pesticide",
]

CATEGORICAL_FEATURES = [
    "Region",
    "Crop",
    "Season",
    "Soil Type",
]

# Load model and feature columns once
model = joblib.load(MODEL_PATH)

with open(FEATURE_COLUMNS_PATH, "r", encoding="utf-8") as file:
    FEATURE_COLUMNS = json.load(file)


def predict(features: dict) -> float:
    required_features = (
        CATEGORICAL_FEATURES + NUMERICAL_FEATURES
    )

    missing_features = [
        feature for feature in required_features
        if feature not in features
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )
    for feature in NUMERICAL_FEATURES:
        value = float(features[feature])
    if not math.isfinite(value):
        raise ValueError(f"{feature} must be a finite number")

    # Create input DataFrame
    input_df = pd.DataFrame([features])

    # Validate categorical values against training categories
    for feature in CATEGORICAL_FEATURES:
        encoded_prefix = f"{feature}_"

        supported_values = [
            column[len(encoded_prefix):]
            for column in FEATURE_COLUMNS
            if column.startswith(encoded_prefix)
        ]

        if features[feature] not in supported_values:
            raise ValueError(
                f"Unsupported {feature}: {features[feature]}"
            )

    # Apply the same one-hot encoding used during training
    input_df = pd.get_dummies(
        input_df,
        columns=CATEGORICAL_FEATURES,
        dtype=int,
    )

    # Align input with all 349 model features
    input_df = input_df.reindex(
        columns=FEATURE_COLUMNS,
        fill_value=0,
    )

    prediction = model.predict(input_df)

    return round(float(prediction[0]), 2)
