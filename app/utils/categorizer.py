import pickle

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
model_path = os.path.join(BASE_DIR, "app", "models", "category_model.pkl")

with open(model_path, "rb") as f:
    vectorizer, model = pickle.load(f)

def predict_category(description, merchant):
    text = description + " " + merchant
    X = vectorizer.transform([text])
    return model.predict(X)[0]
