import pandas as pd

from pathlib import Path

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import joblib


# ============================================================
# Configuration
# ============================================================

DATASET = Path(
    "telemetry/processed/workload_dataset.csv"
)

MODEL_DIR = Path("ml/models")
RESULTS_DIR = Path("ml/results")

MODEL_FILE = MODEL_DIR / "workload_classifier.pkl"


# ============================================================
# Create directories
# ============================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Load dataset
# ============================================================

print("Loading dataset...")

df = pd.read_csv(DATASET)

print(f"Dataset shape: {df.shape}")


# ============================================================
# Features and target
# ============================================================

features = [
    "cpu_percent",
    "memory_percent",
    "rss_mb",
    "read_bytes_per_sec",
    "write_bytes_per_sec",
    "context_switches_per_sec",
    "minor_page_faults_per_sec",
    "major_page_faults_per_sec",
    "num_threads"
]

X = df[features]

y = df["workload_type"]


# ============================================================
# Train / Test split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.25,

    random_state=42,

    stratify=y
)


print()
print("Training samples:", len(X_train))
print("Testing samples :", len(X_test))


# ============================================================
# Random Forest
# ============================================================

model = RandomForestClassifier(

    n_estimators=100,

    random_state=42,

    class_weight="balanced",

    n_jobs=-1
)


print()
print("Training Random Forest...")

model.fit(
    X_train,
    y_train
)


# ============================================================
# Predictions
# ============================================================

y_pred = model.predict(X_test)


# ============================================================
# Accuracy
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print()
print("==========================================")
print("       DAIOS Workload Classifier")
print("==========================================")

print()

print(
    f"Accuracy: {accuracy:.4f}"
)


# ============================================================
# Classification report
# ============================================================

print()
print("Classification Report:")
print(
    classification_report(
        y_test,
        y_pred
    )
)


# ============================================================
# Confusion matrix
# ============================================================

print("Confusion Matrix:")

cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)


# ============================================================
# Feature importance
# ============================================================

importance = pd.DataFrame({

    "feature": features,

    "importance": model.feature_importances_

}).sort_values(
    "importance",
    ascending=False
)


print()
print("Feature Importance:")
print(importance)


# ============================================================
# Save model
# ============================================================

joblib.dump(
    model,
    MODEL_FILE
)


print()
print(f"Model saved to:")
print(MODEL_FILE)
