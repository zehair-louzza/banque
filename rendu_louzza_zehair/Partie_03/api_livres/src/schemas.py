"""
Schemas Pydantic pour la validation et la sérialisation.
- BookCreate  : données envoyées par le client (entrée).
- BookResponse: données renvoyées par l'API (sortie).
- BookStatus  : réponse pour le statut métier d'un livre.
"""
from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    """Données de création d'un livre, avec contraintes de validation."""

    title: str = Field(..., min_length=2)   # au moins 2 caractères
    author: str = Field(..., min_length=2)  # au moins 2 caractères
    year: int = Field(..., ge=1900)         # >= 1900
    rating: int = Field(..., ge=0, le=5)    # entre 0 et 5


class BookResponse(BaseModel):
    """Représentation d'un livre renvoyée par l'API."""

    id: int
    title: str
    author: str
    year: int
    rating: int

    # Permet de construire le schéma directement depuis un objet ORM.
    model_config = {"from_attributes": True}


class BookStatus(BaseModel):
    """Statut métier d'un livre (recommended / average / bad)."""

    id: int
    status: str
