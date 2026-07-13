"""
Modèle SQLAlchemy Book correspondant à la table `books`.
"""
from sqlalchemy import Column, Integer, String

from .database import Base


class Book(Base):
    """Table books : représente un livre persisté en base."""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)  # clé primaire auto-générée
    title = Column(String, nullable=False)              # obligatoire
    author = Column(String, nullable=False)             # obligatoire
    year = Column(Integer, nullable=False)              # année de publication
    rating = Column(Integer, nullable=False)            # note entre 0 et 5
