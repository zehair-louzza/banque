"""
Tests de l'API livres (Partie 3 et Partie 4).

On utilise une base SQLite en mémoire, isolée de la vraie base, grâce à
l'override de la dépendance get_db. Cela garantit des tests indépendants et
reproductibles.

Couverture :
- statut métier compute_status avec plusieurs notes (recommended/average/bad) ;
- cycle CRUD complet via l'API (create, read, update, delete) ;
- gestion des erreurs 404 et validation Pydantic (422) ;
- un marqueur pytest (skip).
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.main import app
from src import models, services, schemas

# Base SQLite en mémoire partagée entre connexions (StaticPool).
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Vide la table avant chaque test pour garantir l'indépendance."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


# --------------------------------------------------------------------------
# Tests de la logique métier compute_status (>= 3 notes différentes)
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "rating,attendu",
    [(5, "recommended"), (4, "recommended"), (3, "average"), (2, "average"), (1, "bad"), (0, "bad")],
)
def test_compute_status(rating, attendu):
    """compute_status renvoie le bon statut selon la note."""
    book = models.Book(title="X", author="Y", year=2000, rating=rating)
    assert services.compute_status(book) == attendu


# --------------------------------------------------------------------------
# Tests des routes (CRUD + codes HTTP)
# --------------------------------------------------------------------------
def test_racine():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "API Books OK"}


def test_creer_livre_retourne_201():
    payload = {"title": "Clean Code", "author": "Robert C. Martin", "year": 2008, "rating": 5}
    resp = client.post("/books", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == 1
    assert data["title"] == "Clean Code"


def test_lister_livres():
    client.post("/books", json={"title": "Livre A", "author": "Auteur A", "year": 2001, "rating": 3})
    resp = client.get("/books")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_obtenir_livre_par_id():
    client.post("/books", json={"title": "Livre B", "author": "Auteur B", "year": 2010, "rating": 4})
    resp = client.get("/books/1")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Livre B"


def test_obtenir_livre_inexistant_404():
    resp = client.get("/books/999")
    assert resp.status_code == 404


def test_modifier_livre():
    client.post("/books", json={"title": "Ancien", "author": "Auteur", "year": 2005, "rating": 2})
    resp = client.put(
        "/books/1",
        json={"title": "Nouveau", "author": "Auteur", "year": 2005, "rating": 4},
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "Nouveau"
    assert resp.json()["rating"] == 4


def test_modifier_livre_inexistant_404():
    resp = client.put(
        "/books/999",
        json={"title": "Nouveau", "author": "Auteur", "year": 2005, "rating": 4},
    )
    assert resp.status_code == 404


def test_supprimer_livre():
    client.post("/books", json={"title": "A supprimer", "author": "Auteur", "year": 2005, "rating": 3})
    resp = client.delete("/books/1")
    assert resp.status_code == 204
    assert client.get("/books/1").status_code == 404


def test_supprimer_livre_inexistant_404():
    resp = client.delete("/books/999")
    assert resp.status_code == 404


def test_statut_livre():
    client.post("/books", json={"title": "Top", "author": "Auteur", "year": 2020, "rating": 5})
    resp = client.get("/books/1/status")
    assert resp.status_code == 200
    assert resp.json() == {"id": 1, "status": "recommended"}


# --------------------------------------------------------------------------
# Tests de validation Pydantic
# --------------------------------------------------------------------------
def test_validation_titre_trop_court_422():
    resp = client.post("/books", json={"title": "A", "author": "Auteur", "year": 2005, "rating": 3})
    assert resp.status_code == 422


def test_validation_rating_hors_bornes_422():
    resp = client.post("/books", json={"title": "Titre", "author": "Auteur", "year": 2005, "rating": 9})
    assert resp.status_code == 422


def test_validation_annee_trop_ancienne_422():
    resp = client.post("/books", json={"title": "Titre", "author": "Auteur", "year": 1800, "rating": 3})
    assert resp.status_code == 422


# --------------------------------------------------------------------------
# Bonus
# --------------------------------------------------------------------------
def test_bonus_top_books():
    client.post("/books", json={"title": "Bon", "author": "Auteur A", "year": 2005, "rating": 5})
    client.post("/books", json={"title": "Moyen", "author": "Auteur B", "year": 2005, "rating": 2})
    resp = client.get("/books/top")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["title"] == "Bon"


def test_bonus_search_by_author():
    client.post("/books", json={"title": "L1", "author": "Robert Martin", "year": 2005, "rating": 4})
    client.post("/books", json={"title": "L2", "author": "Autre Auteur", "year": 2005, "rating": 3})
    resp = client.get("/books/search", params={"author": "Robert"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_bonus_search_par_titre():
    client.post("/books", json={"title": "Clean Code", "author": "R. Martin", "year": 2008, "rating": 5})
    client.post("/books", json={"title": "Le Petit Prince", "author": "Saint-Exupery", "year": 1943, "rating": 4})
    resp = client.get("/books/search", params={"q": "clean"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["title"] == "Clean Code"


def test_bonus_search_q_titre_ou_auteur():
    client.post("/books", json={"title": "Python Avance", "author": "Dupont", "year": 2020, "rating": 5})
    client.post("/books", json={"title": "Autre", "author": "Python Fan", "year": 2020, "rating": 3})
    resp = client.get("/books/search", params={"q": "python"})
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_bonus_search_sans_parametre_400():
    resp = client.get("/books/search")
    assert resp.status_code == 400


# --------------------------------------------------------------------------
# Marqueur pytest (Partie 4.3)
# --------------------------------------------------------------------------
@pytest.mark.skip(reason="Pagination des livres non encore implémentée.")
def test_pagination_future():
    """Test futur : pagination de la liste des livres (à implémenter)."""
    pass
