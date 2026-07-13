# Partie 2 — Module bancaire

Mini-module bancaire indépendant illustrant la programmation orientée objet, les règles métier et les exceptions personnalisées.

## Structure

```
module_bancaire/
├── conftest.py            # rend `src` importable pour pytest
├── src/
│   ├── __init__.py
│   ├── exceptions.py      # MontantInvalideError, SoldeInsuffisantError
│   ├── compte.py          # classe CompteBancaire (logique métier)
│   └── main.py            # interaction utilisateur (seul fichier avec print)
└── tests/
    └── test_compte.py     # tests pytest
```

## Choix techniques

- **Exceptions personnalisées** héritant de `Exception` : `MontantInvalideError` (montant non numérique, nul ou négatif) et `SoldeInsuffisantError` (retrait > solde). Elles portent un message métier clair.
- **Séparation des responsabilités** : la logique métier (`compte.py`) ne fait aucun `print()` ; l'affichage est isolé dans `main.py`.
- **Validation centralisée** : la méthode privée `_to_number()` convertit et valide tout montant, ce qui évite la duplication entre `deposer`, `retirer` et le constructeur.
- **`afficher()`** retourne un dictionnaire (`{"titulaire": ..., "solde": ...}`) plutôt que d'imprimer, pour rester testable et réutilisable.
- **Imports relatifs** (`from .exceptions import ...`) : `src` est un vrai package Python.

## Règles métier

1. Le solde initial ne peut pas être négatif.
2. Un dépôt doit être strictement positif.
3. Un retrait doit être strictement positif.
4. Un retrait ne peut pas dépasser le solde disponible.

## Lancer les tests

Depuis `Partie_02/module_bancaire/` :

```bash
pytest
```

## Lancer l'application interactive

```bash
python -m src.main
```

## Note de régression (Partie 4.2)

Si la méthode `retirer()` était modifiée pour faire `self.solde += montant` au lieu de `self.solde -= montant`, le test `test_retrait_valide_diminue_solde` échouerait immédiatement : partant d'un solde de 100 et retirant 30, on obtiendrait 130 au lieu de 70. Ce test échoue car il vérifie la règle métier fondamentale « un retrait diminue le solde ». La régression serait donc détectée dès le premier lancement de `pytest`, avant tout impact en production.
