"""
Configuration de la base de données SQLite via SQLAlchemy.
Expose l'engine, la SessionLocal, la Base déclarative et la dépendance get_db.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Base SQLite locale (fichier books.db à la racine de api_livres).
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

# check_same_thread=False est requis par SQLite avec FastAPI (multi-thread).
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base déclarative dont héritent les modèles ORM.
Base = declarative_base()


def get_db():
    """Dépendance FastAPI : fournit une session et la ferme après usage."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
