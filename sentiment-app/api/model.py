"""Raccord entre l'API et le modèle entraîné au TP2."""

import sys
from pathlib import Path
from typing import Literal, TypedDict

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from predict import charger_modele  # noqa: E402
from predict import predict as _predict  # noqa: E402

SEUIL_ABSTENTION = 0.60

LabelSentiment = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]


class Prediction(TypedDict):
    """Résultat d'une prédiction."""

    label: LabelSentiment
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec seuil d'abstention."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        """Vérifie que le modèle est disponible."""
        charger_modele()

    def predict(self, text: str) -> Prediction:
        """Prédit le sentiment ou s'abstient si la confiance est trop faible."""
        resultat = _predict(text)
        score = resultat["score"]
        etiquette = resultat["label"].lower()

        if score < SEUIL_ABSTENTION:
            etiquette_finale: LabelSentiment = "INDETERMINE"
        elif etiquette == "positive":
            etiquette_finale = "POSITIVE"
        elif etiquette == "negative":
            etiquette_finale = "NEGATIVE"
        else:
            raise ValueError("Étiquette inconnue renvoyée par le modèle")

        return {
            "label": etiquette_finale,
            "score": score,
            "text": text[:100],
        }


def load_model() -> SentimentClassifier:
    """Construit le classifier utilisé par l'API."""
    return SentimentClassifier()
