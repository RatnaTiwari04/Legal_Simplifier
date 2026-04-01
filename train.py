import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from preprocess import load_and_merge_datasets

MODEL_FOLDER = "models"
MODEL_PATH = os.path.join(MODEL_FOLDER, "simplifier_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_FOLDER, "tfidf_vectorizer.pkl")
DATA_PATH = os.path.join(MODEL_FOLDER, "training_data.pkl")

def train_model():
    os.makedirs(MODEL_FOLDER, exist_ok=True)

    df = load_and_merge_datasets()

    X_text = df["input"].tolist()
    y_text = df["output"].tolist()

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000
    )

    X_vectors = vectorizer.fit_transform(X_text)

    model = NearestNeighbors(n_neighbors=1, metric="cosine")
    model.fit(X_vectors)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(df, DATA_PATH)

    print("Training completed successfully.")
    print(f"Dataset size: {df.shape}")
    print(f"Model saved at: {MODEL_PATH}")
    print(f"Vectorizer saved at: {VECTORIZER_PATH}")
    print(f"Training data saved at: {DATA_PATH}")

if __name__ == "__main__":
    train_model()