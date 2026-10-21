#!/usr/bin/env python
"""Entraîne et sauvegarde le modèle de sentiment.

Usage :
  python src/train.py
  python src/train.py --allocine

Produit : models/sentiment.joblib et models/metrics.json
"""

import argparse
import json
from datetime import date
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

RACINE = Path(__file__).resolve().parents[1]
DEMO = RACINE / "data" / "demo_reviews.csv"
URL_ALLOCINE = (
    "https://huggingface.co/datasets/tblard/allocine/resolve/main/"
    "allocine/validation-00000-of-00001.parquet"
)
MODELE = RACINE / "models" / "sentiment.joblib"
METRIQUES = RACINE / "models" / "metrics.json"
SEUIL_F1 = 0.85
GRAINE = 42

def charger(allocine: bool) -> tuple[pd.DataFrame, str]:
    """Charge le jeu de démonstration ou le jeu public Allociné."""
    if allocine:
        df = pd.read_parquet(URL_ALLOCINE)
        df["label"] = df["label"].map({0: "negative", 1: "positive"})
        return df[["review", "label"]].dropna(), "allocine"

    if not DEMO.exists():
        raise SystemExit(
            "data/demo_reviews.csv absent : "
            "lancez d'abord python src/make_demo.py"
        )

    return pd.read_csv(DEMO), "demo"




    df_demo = pd.read_csv(DEMO)
    fichier_exemples = RACINE / "data" / "sample_reviews.csv"

    if fichier_exemples.exists():
        df_exemples = pd.read_csv(fichier_exemples)
        df = pd.concat([df_demo, df_exemples], ignore_index=True)
    else:
        df = df_demo

    df = df[["review", "label"]].dropna()
    df["review"] = df["review"].astype(str).str.strip()
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df = df[df["label"].isin(["positive", "negative"])]
    df = df.drop_duplicates(subset=["review", "label"])

    return df, "demo+sample"


def construire_pipeline() -> Pipeline:
    """Regroupe la vectorisation TF-IDF et la classification."""
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    min_df=2,
                    sublinear_tf=True,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=GRAINE,
                ),
            ),
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allocine",
        action="store_true",
        help="utiliser le jeu public Allociné",
    )
    args = parser.parse_args()

    df, source = charger(args.allocine)

    print(
        f"Source : {source}, {len(df)} avis "
        f"({(df['label'] == 'negative').sum()} négatifs)"
    )

    X_train, X_test, y_train, y_test = train_test_split(
        df["review"],
        df["label"],
        test_size=0.2,
        random_state=GRAINE,
        stratify=df["label"],
    )

    print(
        f"{len(X_train)} avis d'entraînement, "
        f"{len(X_test)} de test"
    )

    pipeline = construire_pipeline()
    pipeline.fit(X_train, y_train)

    vocabulaire = len(pipeline.named_steps["tfidf"].vocabulary_)
    print(f"Vocabulaire : {vocabulaire} termes")

    predictions = pipeline.predict(X_test)
    rapport = classification_report(
        y_test,
        predictions,
        output_dict=True,
        zero_division=0,
    )

    f1 = rapport["macro avg"]["f1-score"]
    print(f"F1 macro sur le jeu de test : {f1:.3f} (seuil {SEUIL_F1})")

    MODELE.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODELE)

    metriques = {
        "source": source,
        "date": date.today().isoformat(),
        "n_train": len(X_train),
        "n_test": len(X_test),
        "f1_macro": round(f1, 4),
        "accuracy": round(rapport["accuracy"], 4),
        "recall_negative": round(rapport["negative"]["recall"], 4),
        "seuil_f1": SEUIL_F1,
    }

    METRIQUES.write_text(
        json.dumps(metriques, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Modèle : {MODELE.relative_to(RACINE)}")
    print(
        f"Métriques : {METRIQUES.relative_to(RACINE)} "
        "(versionné dans Git, contrairement au modèle)"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
