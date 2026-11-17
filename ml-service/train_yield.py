import json
import os

import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor


DATA_PATH = "datasets/yield/source/crop_yield_dataset.csv"
MODEL_DIR = "trained_models"

os.makedirs(MODEL_DIR, exist_ok=True)

print("Loading yield dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")

target = "Yield"

categorical_features = [
    "Region",
    "Crop",
    "Season",
    "Soil Type",
]

numerical_features = [
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

features = categorical_features + numerical_features

print("Encoding categorical features...")

df = pd.get_dummies(
    df,
    columns=categorical_features,
    dtype=int
)

encoded_features = [column for column in df.columns if column != target]

X = df[encoded_features]
y = df[target]

print(f"Total input features after encoding: {X.shape[1]}")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

print("\nTraining XGBoost model...")

model = XGBRegressor(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training completed.")

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\nModel Evaluation")
print("----------------")
print(f"MAE:  {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R²:   {r2:.4f}")

model_path = os.path.join(
    MODEL_DIR,
    "yield_model.pkl"
)

joblib.dump(model, model_path)

print(f"\nModel saved to: {model_path}")

feature_columns_path = os.path.join(
    MODEL_DIR,
    "yield_feature_columns.json"
)

with open(feature_columns_path, "w") as file:
    json.dump(encoded_features, file, indent=4)

print(f"Feature columns saved to: {feature_columns_path}")

metadata = {
    "target": target,
    "original_features": features,
    "encoded_features": encoded_features,
    "metrics": {
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4)
    }
}

metadata_path = os.path.join(
    MODEL_DIR,
    "yield_model_metadata.json"
)

with open(metadata_path, "w") as file:
    json.dump(metadata, file, indent=4)

print(f"Metadata saved to: {metadata_path}")