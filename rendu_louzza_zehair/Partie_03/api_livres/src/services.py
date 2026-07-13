"""
Couche service : logique métier et accès à la base de données.
Les routes appellent ces fonctions ; aucune règle métier ne vit dans routes.py.
Les fonctions renvoient None quand une ressource est absente (les routes
traduisent cela en erreur HTTP 404).
"""
from sqlalchemy.orm import Session

from . import models, schemas


def create_book(db: Session, payload: schemas.BookCreate) -> models.Book:
    """Crée un livre en base à partir des données validées."""
    book = models.Book(
        title=payload.title,
        author=payload.author,
        year=payload.year,
        rating=payload.rating,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_all_books(db: Session):
    """Retourne la liste de tous les livres."""
    return db.query(models.Book).all()


def get_book_by_id(db: Session, book_id: int):
    """Retourne un livre par son identifiant, ou None s'il n'existe pas."""
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, payload: schemas.BookCreate):
    """Met à jour un livre existant, ou None s'il n'existe pas."""
    book = get_book_by_id(db, book_id)
    if book is None:
        return None
    book.title = payload.title
    book.author = payload.author
    book.year = payload.year
    book.rating = payload.rating
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> bool:
    """Supprime un livre. Retourne True si supprimé, False s'il n'existait pas."""
    book = get_book_by_id(db, book_id)
    if book is None:
        return False
    db.delete(book)
    db.commit()
    return True


def compute_status(book: models.Book) -> str:
    """
    Statut métier d'un livre selon sa note :
        rating >= 4 -> "recommended"
        rating >= 2 -> "average"
        rating <  2 -> "bad"
    """
    if book.rating >= 4:
        return "recommended"
    if book.rating >= 2:
        return "average"
    return "bad"


def search_books_by_author(db: Session, author: str):
    """Bonus : recherche des livres par auteur (correspondance partielle)."""
    return (
        db.query(models.Book)
        .filter(models.Book.author.ilike(f"%{author}%"))
        .all()
    )


def get_top_books(db: Session):
    """Bonus : retourne les livres dont la note est >= 4."""
    return db.query(models.Book).filter(models.Book.rating >= 4).all()
