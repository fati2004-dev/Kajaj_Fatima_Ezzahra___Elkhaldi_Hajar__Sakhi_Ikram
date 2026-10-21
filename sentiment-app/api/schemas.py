
"""Contrats d'entrée et de sortie de l'API (Pydantic v2)."""

from pydantic import BaseModel, Field, field_validator


class PredictRequest(BaseModel):
    """Requête de prédiction."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Texte à classifier",
        examples=["Livraison rapide, produit conforme, très satisfait"],
    )

    @field_validator("text")
    @classmethod
    def verifier_texte_non_blanc(cls, valeur: str) -> str:
        """Refuse les chaînes vides ou composées uniquement d'espaces."""
        if not valeur.strip():
            raise ValueError("Le texte ne doit pas être vide ou composé d'espaces")
        return valeur


class PredictResponse(BaseModel):
    """Réponse de prédiction."""

    label: str = Field(
        ...,
        description="POSITIVE, NEGATIVE ou INDETERMINE",
    )
    score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confiance de la classe prédite",
    )
    text: str = Field(
        ...,
        description="Aperçu du texte analysé (100 caractères)",
    )


class HealthResponse(BaseModel):
    """Réponse de l'endpoint de santé."""

    status: str = Field(..., description="OK si le modèle est chargé")
    model: str = Field(..., description="Nom du modèle servi")


class ErrorResponse(BaseModel):
    """Format standard des erreurs FastAPI."""

    detail: str
