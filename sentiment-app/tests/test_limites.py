
"""Tests aux limites du contrat d'entrée (TP4)."""

import json
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(
    not MODELE.exists(),
    reason="Modèle absent : lancez python src/train.py",
)


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as test_client:
        yield test_client


def en_json(valeur: object) -> bytes:
    return json.dumps(valeur).encode("utf-8")


CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "   "}), 422, id="texte-espaces"),
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
        detail = reponse.json()["detail"]
        assert isinstance(detail, list)
        assert all(
            isinstance(erreur, dict)
            and {"loc", "msg", "type"}.issubset(erreur)
            for erreur in detail
        )


@settings(deadline=None, max_examples=30)
@given(
    texte=st.text(
        min_size=1,
        max_size=2000,
        alphabet=st.characters(blacklist_categories=("Cs",)),
    ).filter(lambda valeur: bool(valeur.strip()))
)
def test_tout_texte_non_blanc_est_accepte(client, texte):
    reponse = client.post("/predict", json={"text": texte})

    assert reponse.status_code == 200
    resultat = reponse.json()
    assert resultat["label"] in {"POSITIVE", "NEGATIVE", "INDETERMINE"}
    assert 0 <= resultat["score"] <= 1


@settings(deadline=None, max_examples=20)
@given(
    texte=st.text(
        alphabet=" \t\n\r",
        min_size=1,
        max_size=20,
    )
)
def test_tout_texte_blanc_est_refuse(client, texte):
    reponse = client.post("/predict", json={"text": texte})

    assert reponse.status_code == 422
    detail = reponse.json()["detail"]
    assert isinstance(detail, list)
    assert all(
        isinstance(erreur, dict)
        and {"loc", "msg", "type"}.issubset(erreur)
        for erreur in detail
    )
