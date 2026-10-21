
"""Tests d'intégration de l'API (TP4, étape D)."""

from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
MODELE = RACINE / "models" / "sentiment.joblib"


@pytest.fixture
def client():
    """Démarre réellement l'application et exécute son lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as test_client:
        yield test_client


def test_demarrage_reel_charge_le_modele(client):
    """D.1 : le démarrage charge le modèle."""
    reponse = client.get("/health")

    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_empeche_le_demarrage(monkeypatch):
    """D.2 : le démarrage échoue si le fichier modèle manque."""
    from fastapi.testclient import TestClient

    from api.main import app
    from api.model import RACINE as RACINE_MODELE
    from api.model import charger_modele

    chemin_original = RACINE_MODELE / "models" / "sentiment.joblib"
    chemin_factice = chemin_original.with_name("modele_inexistant_tp4.joblib")

    import predict

    monkeypatch.setattr(predict, "MODELE", chemin_factice)
    charger_modele.cache_clear()

    try:
        with pytest.raises(FileNotFoundError):
            with TestClient(app):
                pass
    finally:
        charger_modele.cache_clear()


def test_modele_non_charge_retourne_503(client, monkeypatch):
    """D.3 : les routes protégées répondent 503 sans classifier."""
    from api.main import app

    monkeypatch.delattr(app.state, "classifier", raising=False)

    assert client.get("/health").status_code == 503

    reponse = client.post(
        "/predict",
        json={"text": "Produit excellent"},
    )
    assert reponse.status_code == 503
    assert reponse.json()["detail"] == "Modèle non chargé"


@pytest.mark.parametrize(
    "erreur",
    [
        RuntimeError("secret interne"),
        ValueError("bug interne"),
    ],
)
def test_erreur_modele_est_masquee(client, monkeypatch, erreur):
    """D.4 : une panne inattendue renvoie 500 sans exposer le détail."""
    from api.main import app

    class FauxClassifier:
        def predict(self, text):
            raise erreur

    monkeypatch.setattr(app.state, "classifier", FauxClassifier())

    reponse = client.post(
        "/predict",
        json={"text": "Produit excellent"},
    )

    assert reponse.status_code == 500
    assert reponse.json()["detail"] == "Erreur interne du serveur"
    assert "secret interne" not in reponse.text
    assert "bug interne" not in reponse.text

def test_label_inconnu_est_refuse(client, monkeypatch):
    """Une étiquette inattendue doit être rejetée avec une erreur 500."""
    from api.main import app

    class FauxClassifier:
        def predict(self, text):
            return {
                "label": "UNKNOWN",
                "score": 0.99,
                "text": text[:100],
            }

    monkeypatch.setattr(app.state, "classifier", FauxClassifier())

    reponse = client.post(
        "/predict",
        json={"text": "Produit excellent"},
    )

    assert reponse.status_code == 500
    assert reponse.json()["detail"] == "Réponse invalide du modèle"
    assert "UNKNOWN" not in reponse.text
