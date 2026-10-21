"""Tests aux limites du contrat d'entrée (TP4, étape B)."""

import json
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")
ETIQUETTES = {"POSITIVE", "NEGATIVE", "INDETERMINE"}


@pytest.fixture(scope="module")
def client():
    """Portée « module » : l'API démarre une fois pour tout le fichier (hypothesis l'exige)."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as test_client:
        yield test_client


def en_json(valeur: object) -> bytes:
    """Corps de requête JSON, sous forme d'octets : permet aussi d'envoyer un corps invalide."""
    return json.dumps(valeur).encode("utf-8")


CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "   "}), 422, id="texte-espaces"),
    pytest.param(en_json({"text": "   \t\n"}), 422, id="texte-blanc"),
    pytest.param(en_json({"text": "a"}), 200, id="un-caractere"),
    pytest.param(en_json({"text": "a" * 2000}), 200, id="2000-caracteres"),
    pytest.param(en_json({"text": "a" * 2001}), 422, id="2001-caracteres"),
    pytest.param(en_json({}), 422, id="champ-absent"),
    pytest.param(en_json({"text": 42}), 422, id="type-invalide"),
    pytest.param(b"pas du json", 422, id="json-invalide"),
]


@pytest.mark.parametrize("corps, code_attendu", CAS)
def test_frontieres_du_contrat(client, corps, code_attendu):
    reponse = client.post(
        "/predict",
        content=corps,
        headers={"Content-Type": "application/json"},
    )
    assert reponse.status_code == code_attendu
    if code_attendu == 422:
        erreurs = reponse.json()["detail"]
        assert isinstance(erreurs, list)
        assert all({"loc", "msg", "type"} <= set(erreur) for erreur in erreurs)
    else:
        resultat = reponse.json()
        assert resultat["label"] in ETIQUETTES
        assert 0.0 <= resultat["score"] <= 1.0


NON_BLANC = st.characters(blacklist_categories=("Cs",)).filter(lambda c: not c.isspace())
TEXTES_VALIDES = st.text(alphabet=NON_BLANC, min_size=1, max_size=2000)
CARACTERE_BLANC = st.characters(
    whitelist_categories=("Zs",),
    whitelist_characters="\t\n\r\f\v",
)
TEXTES_BLANCS = st.text(alphabet=CARACTERE_BLANC, min_size=1, max_size=2000)


@settings(max_examples=25, deadline=None)
@given(texte=TEXTES_VALIDES)
def test_propriete_texte_non_blanc(client, texte):
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 200
    resultat = reponse.json()
    assert resultat["label"] in ETIQUETTES
    assert 0.0 <= resultat["score"] <= 1.0


@settings(max_examples=25, deadline=None)
@given(texte=TEXTES_BLANCS)
def test_propriete_texte_blanc(client, texte):
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 422
    erreurs = reponse.json()["detail"]
    assert isinstance(erreurs, list)
    assert all({"loc", "msg", "type"} <= set(erreur) for erreur in erreurs)
