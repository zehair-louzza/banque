# Examen final — Programmation avec Python

MBA Big Data & Intelligence Artificielle — M2 · UE05.B · 2025-2026

Rendu complet de l'examen pratique, organisé en 4 parties conformément au sujet.

## Structure

```
rendu_louzza_zehair/
├── Partie_01/
│   └── reponses_partie_1.md          # Questions de cours
├── Partie_02/
│   └── module_bancaire/              # POO, règles métier, exceptions
│       ├── README.md
│       ├── src/ (compte.py, exceptions.py, main.py)
│       └── tests/ (test_compte.py)
└── Partie_03/
    └── api_livres/                   # API REST FastAPI + SQLite + SQLAlchemy
        ├── README.md
        ├── requirements.txt
        ├── src/ (main, database, models, schemas, services, routes)
        └── tests/ (test_books.py)
```

## Lancer les tests

```bash
# Partie 2
cd Partie_02/module_bancaire && pytest

# Partie 3
cd Partie_03/api_livres && pip install -r requirements.txt && pytest
```

## Lancer l'API (Partie 3)

```bash
cd Partie_03/api_livres
uvicorn src.main:app --reload
```

Documentation interactive : http://127.0.0.1:8000/docs

## État des tests

- Partie 2 : 10 tests passés, 1 skippé (marqueur pytest)
- Partie 3 : 21 tests passés, 1 skippé (marqueur pytest)

Chaque partie technique contient son propre `README.md` détaillant les choix techniques, les commandes, la note de régression et les limites.
