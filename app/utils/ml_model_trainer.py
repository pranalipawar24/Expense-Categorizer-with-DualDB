import os
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def train_model():
    # Path to CSV file
    csv_path = "training_data.csv"

    # Check if file exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found at {csv_path}")

    # Load dataset
    df = pd.read_csv(csv_path)

    # Combine description and merchant columns
    df["text"] = (
        df["description"].astype(str) + " " +
        df["merchant"].astype(str)
    )

    # Features and labels
    X_text = df["text"]
    y = df["category"]

    # Convert text into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(X_text)

    # Train Naive Bayes model
    model = MultinomialNB()
    model.fit(X, y)

    # Create model save path
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )

    model_path = os.path.join(
        BASE_DIR,
        "app",
        "models",
        "category_model.pkl"
    )

    # Create models directory if it does not exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save model and vectorizer
    with open(model_path, "wb") as f:
        pickle.dump((vectorizer, model), f)

    print(f"✅ Model trained and saved at: {model_path}")


if __name__ == "__main__":
    train_model()