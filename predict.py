import os
import joblib
import re

MODEL_FOLDER = "models"
MODEL_PATH = os.path.join(MODEL_FOLDER, "simplifier_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_FOLDER, "tfidf_vectorizer.pkl")
DATA_PATH = os.path.join(MODEL_FOLDER, "training_data.pkl")

THRESHOLD = 0.55


def load_artifacts():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    df = joblib.load(DATA_PATH)
    return model, vectorizer, df


LEGAL_DICTIONARY = {
    "indemnify": "compensate",
    "hold harmless": "protect from blame",
    "liable": "legally responsible",
    "liability": "legal responsibility",
    "liabilities": "legal responsibilities",
    "premises": "property",
    "hereunder": "under this agreement",
    "thereof": "of that",
    "whereas": "because",
    "hereto": "to this document",
    "notwithstanding": "despite",
    "covenant": "formal promise",
    "warranty": "guarantee",
    "breach": "breaking the agreement",
    "damages": "money for loss",
    "lessee": "tenant",
    "lessor": "landlord",
    "jurisdiction": "legal authority",
    "arbitration": "settling disputes outside court",
    "shall": "must"
}


def replace_legal_terms(text):
    simplified = text
    for term, meaning in sorted(LEGAL_DICTIONARY.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = r"\b" + re.escape(term) + r"\b"
        simplified = re.sub(pattern, meaning, simplified, flags=re.IGNORECASE)
    return simplified


def rule_based_simplify(text):
    simplified = replace_legal_terms(text)
    simplified = re.sub(r"\s+", " ", simplified).strip()
    return f"In simple words: {simplified}"


def simplify_text(user_input):
    model, vectorizer, df = load_artifacts()

    cleaned_input = user_input.lower().strip()
    user_vector = vectorizer.transform([cleaned_input])

    distances, indices = model.kneighbors(user_vector, n_neighbors=1)

    best_index = indices[0][0]
    similarity_score = 1 - distances[0][0]

    if similarity_score < THRESHOLD:
        return {
            "matched_input": None,
            "simplified_output": user_input,
            "similarity_score": similarity_score,
            "note": "Low similarity, so original sentence was returned."
        }

    return {
        "matched_input": df.iloc[best_index]["input"],
        "simplified_output": df.iloc[best_index]["output"],
        "similarity_score": similarity_score,
        "note": "Simplified using closest dataset match."
    }