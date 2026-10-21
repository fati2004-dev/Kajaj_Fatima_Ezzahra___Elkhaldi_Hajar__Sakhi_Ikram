"""Raccord entre l'API et le modèle entraîné au TP2."""

import sys
from pathlib import Path
from typing import TypedDict

from api.schemas import SentimentLabel

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from predict import ModelSentiment, PredictionResult, charger_modele  # noqa: E402
from predict import predict as _predict  # noqa: E402

SEUIL_ABSTENTION = 0.60
ETIQUETTES: dict[ModelSentiment, SentimentLabel] = {
    "positive": "POSITIVE",
    "negative": "NEGATIVE",
}


class ApiPrediction(TypedDict):
    label: SentimentLabel
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec seuil d'abstention."""

    model_name: str = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        model = charger_modele()
        classes = set(model.classes_)
        if classes != set(ETIQUETTES):
            raise RuntimeError(f"Classes de sentiment inattendues : {sorted(classes)!r}")

    def predict(self, text: str) -> ApiPrediction:
        """Renvoie le sentiment, ou INDETERMINE si le score est sous le seuil."""
        resultat: PredictionResult = _predict(text)
        label = ETIQUETTES.get(resultat["label"])
        if label is None:
            raise ValueError("Étiquette inconnue renvoyée par le modèle")
        if resultat["score"] < SEUIL_ABSTENTION:
            label = "INDETERMINE"
        return {"label": label, "score": resultat["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier utilisé par l'API."""
    return SentimentClassifier()
