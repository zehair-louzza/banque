# Partie 3 — API REST de gestion de livres (FastAPI)

API REST permettant de gérer une collection de livres. Elle utilise **FastAPI**, **Pydantic**, **SQLAlchemy** et **SQLite**.

## Structure

```
api_livres/
├── requirements.txt
├── README.md
├── conftest.py            # rend `src` importable pour pytest
├── src/
│   ├── __init__.py
│   ├── main.py            # instanciation FastAPI + création des tables
│   ├── database.py        # engine, session, Base, dépendance get_db
│   ├── models.py          # modèle SQLAlchemy Book (table books)
│   ├── schemas.py         # schemas Pydantic (validation / sérialisation)
│   ├── services.py        # logique métier + accès base (CRUD, compute_status)
│   └── routes.py          # endpoints HTTP
└── tests/
    └── test_books.py
```

## Installation

```bash
pip install -r requirements.txt
```

## Lancement de l'API

Depuis `Partie_03/api_livres/` :

```bash
uvicorn src.main:app --reload
```

Documentation interactive : http://127.0.0.1:8000/docs

## Endpoints

| Méthode | Endpoint | Comportement |
|---------|----------|--------------|
| GET | `/` | `{"message": "API Books OK"}` |
| POST | `/books` | crée un livre, retourne le livre (201) |
| GET | `/books` | liste des livres |
| GET | `/books/{id}` | un livre ou 404 |
| PUT | `/books/{id}` | modifie un livre ou 404 |
| DELETE | `/books/{id}` | supprime un livre ou 404 |
| GET | `/books/{id}/status` | statut métier du livre |
| GET | `/books/top` | *(bonus)* livres avec note >= 4 |
| GET | `/books/search?author=...` | *(bonus)* recherche par auteur |

## Règle métier `compute_status`

- `rating >= 4` → `"recommended"`
- `rating >= 2` → `"average"`
- `rating < 2` → `"bad"`

## Choix techniques

- **Séparation en couches** : `routes` (HTTP) → `services` (métier + DB) → `models` (ORM) / `schemas` (validation). Les routes ne contiennent aucune règle métier.
- **Validation Pydantic** avec `Field` : `title`/`author` ≥ 2 caractères, `year` ≥ 1900, `rating` entre 0 et 5. Une donnée invalide renvoie automatiquement une erreur 422.
- **`get_db`** en dépendance FastAPI : ouvre une session par requête et la ferme proprement (pas de fuite de connexion).
- **Ordre des routes** : `/books/top` et `/books/search` sont déclarées avant `/books/{book_id}` pour éviter que « top »/« search » soient pris pour un identifiant.
- **DELETE** renvoie 204 (No Content) car il n'y a pas de corps à retourner.

## Tests

Depuis `Partie_03/api_livres/` :

```bash
pytest
```

Les tests utilisent une base SQLite **en mémoire** (via un override de `get_db`) pour rester isolés de la base réelle.

## Note de régression (Partie 4.2)

Si `compute_status` était modifiée pour tester `rating > 4` au lieu de `rating >= 4`, un livre noté 4 basculerait à tort de `"recommended"` vers `"average"`. Le test paramétré `test_compute_status[4-recommended]` échouerait alors immédiatement en affichant `average != recommended`. Ce test verrouille donc les seuils métier et détecte toute régression sur les bornes de notation.

## Limites connues

- La base `books.db` est un fichier local recréé au premier lancement ; aucune migration n'est gérée (SQLAlchemy `create_all`).
- Pas d'authentification : l'API est ouverte, adaptée à un contexte d'examen local.
