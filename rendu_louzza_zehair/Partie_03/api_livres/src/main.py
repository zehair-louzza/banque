"""
Point d'entrée de l'API FastAPI.
Lancement depuis Partie_03/api_livres/ :
    uvicorn src.main:app --reload
"""
from fastapi import FastAPI

from . import models
from .database import engine
from .routes import router

# Création automatique des tables au démarrage.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Books", version="1.0.0")

app.include_router(router)
