import os
import pickle
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Paths
test_data_path = os.path.join(
    BASE_DIR,
    "evaluation",
    "hard_test_data.csv"
)

model_path = os.path.join(
    BASE_DIR,
    "app",
    "models",
    "category_model.pkl"
)


# Load unseen test dataset
df = pd.read_csv(test_data_path)

# Combine description and merchant
df["text"] = (
    df["description"].astype(str) + " " +
    df["merchant"].astype(str)
)

X_text = df["text"]
y_true = df["category"]


# Load trained model and vectorizer
with open(model_path, "rb") as f:
    vectorizer, model = pickle.load(f)


# Transform unseen data
X_test = vectorizer.transform(X_text)


# Make predictions
y_pred = model.predict(X_test)


# Calculate metrics
accuracy = accuracy_score(y_true, y_pred)

precision = precision_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)


# Display results
print("\n========== UNSEEN DATASET EVALUATION ==========")

print(f"Test samples : {len(y_true)}")
print(f"Accuracy     : {accuracy:.2f}")
print(f"Precision    : {precision:.2f}")
print(f"Recall       : {recall:.2f}")
print(f"F1 Score     : {f1:.2f}")


print("\n========== CLASSIFICATION REPORT ==========")

print(
    classification_report(
        y_true,
        y_pred,
        zero_division=0
    )
)


print("\n========== CONFUSION MATRIX ==========")

print(confusion_matrix(y_true, y_pred))


# Show individual predictions
print("\n========== PREDICTIONS ==========")

for description, merchant, actual, predicted in zip(
    df["description"],
    df["merchant"],
    y_true,
    y_pred
):
    status = "✓" if actual == predicted else "✗"

    print(
        f"{status} "
        f"{description} | {merchant} "
        f"→ Actual: {actual}, Predicted: {predicted}"
    )


print("\n============================================")