"""
Routes de l'API livres. Cette couche gère uniquement le HTTP :
codes de statut, erreurs 404, et délégation au service pour le métier.

Note d'ordre des routes : /books/top et /books/search sont déclarées AVANT
/books/{book_id} pour éviter que FastAPI n'interprète "top" ou "search"
comme un identifiant de livre.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import schemas, services
from .database import get_db

router = APIRouter()


@router.get("/")
def racine():
    """Point de santé de l'API."""
    return {"message": "API Books OK"}


@router.post("/books", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def creer_livre(payload: schemas.BookCreate, db: Session = Depends(get_db)):
    """Ajoute un livre et retourne le livre créé (201)."""
    return services.create_book(db, payload)


@router.get("/books", response_model=list[schemas.BookResponse])
def lister_livres(db: Session = Depends(get_db)):
    """Retourne la liste des livres."""
    return services.get_all_books(db)


# ----- Bonus : routes spécifiques placées avant /books/{book_id} -----
@router.get("/books/top", response_model=list[schemas.BookResponse])
def livres_recommandes(db: Session = Depends(get_db)):
    """Bonus : livres dont la note est >= 4."""
    return services.get_top_books(db)


@router.get("/books/search", response_model=list[schemas.BookResponse])
def rechercher_par_auteur(author: str, db: Session = Depends(get_db)):
    """Bonus : recherche de livres par auteur."""
    return services.search_books_by_author(db, author)


@router.get("/books/{book_id}", response_model=schemas.BookResponse)
def obtenir_livre(book_id: int, db: Session = Depends(get_db)):
    """Retourne un livre par identifiant ou une erreur 404."""
    book = services.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Livre introuvable.")
    return book


@router.put("/books/{book_id}", response_model=schemas.BookResponse)
def modifier_livre(book_id: int, payload: schemas.BookCreate, db: Session = Depends(get_db)):
    """Modifie un livre ou retourne une erreur 404."""
    book = services.update_book(db, book_id, payload)
    if book is None:
        raise HTTPException(status_code=404, detail="Livre introuvable.")
    return book


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_livre(book_id: int, db: Session = Depends(get_db)):
    """Supprime un livre ou retourne une erreur 404."""
    if not services.delete_book(db, book_id):
        raise HTTPException(status_code=404, detail="Livre introuvable.")
    return None


@router.get("/books/{book_id}/status", response_model=schemas.BookStatus)
def statut_livre(book_id: int, db: Session = Depends(get_db)):
    """Retourne le statut métier du livre (recommended / average / bad)."""
    book = services.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Livre introuvable.")
    return schemas.BookStatus(id=book.id, status=services.compute_status(book))
