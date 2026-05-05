import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


FEATURE_COLS = [
    'total_ingredients', 'irritants_count', 'comedogenic_count',
    'harmful_count', 'beneficial_count', 'irritants_ratio',
    'comedogenic_ratio', 'harmful_ratio', 'beneficial_ratio',
    'has_fragrance', 'has_alcohol', 'has_harmful', 'has_beneficial'
]

TARGET_COLS = [
    'is_for_dry_skin', 'is_for_oily_skin',
    'is_good_for_acne', 'is_fragrance_free'
]


def train_model(df, model_path="models/skincare_model.pkl"):
    """Train MultiOutput Random Forest and save to disk."""
    X = df[FEATURE_COLS]
    y = df[TARGET_COLS]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = MultiOutputClassifier(RandomForestClassifier(
        n_estimators=100, random_state=42))
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    for i, col in enumerate(TARGET_COLS):
        print(f"\n── {col} ──")
        print(classification_report(y_test.iloc[:, i], y_pred[:, i]))

    # Save
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"\n✅ Model saved to {model_path}")

    return model


def load_model(model_path="models/skincare_model.pkl"):
    """Load trained model from disk."""
    with open(model_path, "rb") as f:
        return pickle.load(f)


def predict(model, features_df):
    """Run prediction and return label array."""
    return model.predict(features_df)[0]
