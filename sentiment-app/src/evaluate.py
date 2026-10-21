"""Évaluation du modèle de sentiment entraîné au TP2."""

import json
from pathlib import Path

import joblib
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

RACINE = Path(__file__).resolve().parents[1]
DONNEES = RACINE / "data" / "demo_reviews.csv"
MODELE = RACINE / "models" / "sentiment.joblib"


def main() -> int:
    """Évalue le modèle et affiche ses principales métriques."""
    if not DONNEES.exists():
        print(f"Fichier de données introuvable : {DONNEES}")
        return 1

    if not MODELE.exists():
        print(f"Modèle introuvable : {MODELE}")
        return 1

    import pandas as pd

    donnees = pd.read_csv(DONNEES)
    X = donnees["text"].astype(str)
    y = donnees["label"].astype(str)

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    modele = joblib.load(MODELE)
    y_pred = modele.predict(X_test)

    print("Rapport de classification :")
    print(classification_report(y_test, y_pred, zero_division=0))

    mc = confusion_matrix(y_test, y_pred)
    etiquettes = sorted(y.unique())

    print("Matrice de confusion (lignes = vérité, colonnes = prédiction)")
    print(f"{'':>10}{etiquettes[0]:>10}{etiquettes[1]:>10}")
    for nom, ligne in zip(etiquettes, mc, strict=True):
        print(f"{nom:>10}{ligne[0]:>10}{ligne[1]:>10}")

    if len(etiquettes) == 2:
        faux_negatifs = mc[1][0]
        faux_positifs = mc[0][1]
        print(f"\n{faux_positifs} négatifs classés positifs, {faux_negatifs} positifs classés négatifs")

    erreurs = [
        (texte, vrai, predit)
        for texte, vrai, predit in zip(X_test, y_test, y_pred, strict=True)
        if vrai != predit
    ]
    print(f"\n{len(erreurs)} erreurs au total. Trois exemples :")
    for texte, vrai, predit in erreurs[:3]:
        print(f"  vérité={vrai:9s} prédit={predit:9s} | {texte[:90]}")

    fichier_metriques = RACINE / "models" / "metrics.json"
    if fichier_metriques.exists():
        with fichier_metriques.open(encoding="utf-8") as fichier:
            metriques = json.load(fichier)
        print("\nMétriques enregistrées :")
        print(json.dumps(metriques, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
