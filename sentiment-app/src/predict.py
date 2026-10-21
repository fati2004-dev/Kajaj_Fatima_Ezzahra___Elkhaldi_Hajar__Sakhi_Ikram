
#!/usr/bin/env python
"""Prédiction unitaire du sentiment."""

import sys
from functools import lru_cache
from pathlib import Path
from typing import Literal, TypedDict, cast

import joblib
from sklearn.pipeline import Pipeline

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
ModelSentiment = Literal["positive", "negative"]


class PredictionResult(TypedDict):
    label: ModelSentiment
    score: float


@lru_cache(maxsize=1)
def charger_modele() -> Pipeline:
    """Charge le modèle une seule fois par processus."""
    if not MODELE.exists():
        raise FileNotFoundError("models/sentiment.joblib absent : lancez python src/train.py")
    return cast(Pipeline, joblib.load(MODELE))


def predict(texte: str) -> PredictionResult:
    """Renvoie l'étiquette positive/négative et la confiance."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")

    pipeline = charger_modele()
    prediction = pipeline.predict([texte])[0]
    if prediction not in {"positive", "negative"}:
        raise RuntimeError(f"Classe de sentiment inattendue : {prediction!r}")
    etiquette = cast(ModelSentiment, prediction)
    score = float(pipeline.predict_proba([texte]).max())

    return {"label": etiquette, "score": round(score, 4)}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    resultat = predict(" ".join(sys.argv[1:]))
    print(f"{resultat['label']} (confiance {resultat['score']:.0%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
