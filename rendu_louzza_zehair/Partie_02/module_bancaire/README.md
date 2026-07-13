# Partie 2 — Module bancaire

Mini-module bancaire illustrant la programmation orientée objet, les règles métier et les exceptions personnalisées.

---

## 🟢 Marche à suivre pas-à-pas (VS Code)

> Toutes les commandes se lancent dans le **terminal intégré de VS Code**
> (menu **Terminal > Nouveau terminal**). Copiez-collez-les une par une.

### Étape 1 — Créer l'environnement virtuel (une seule fois)

Depuis la **racine** `rendu_louzza_zehair` (un seul `.venv` sert pour tout le rendu) :

```powershell
python -m venv .venv
```

> Déjà fait via `setup.bat` ou pour la Partie 3 ? Passez à l'étape 2.

### Étape 2 — Activer l'environnement virtuel

**Windows (PowerShell)**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Après activation, la ligne du terminal commence par `(.venv)`.

> Si PowerShell bloque (« exécution de scripts désactivée »), lancez une fois :
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```
> puis réessayez l'activation.

### Étape 3 — Se placer dans le dossier de la partie 2

```powershell
cd Partie_02\module_bancaire
```

> Sur macOS / Linux, utilisez les slashs : `cd Partie_02/module_bancaire`

### Étape 4 — Installer pytest

```powershell
pip install pytest
```

### Étape 5 — Lancer les tests

```powershell
pytest
```

✅ Résultat attendu :
```
10 passed, 1 skipped
```

> ⚠️ Ne cliquez PAS sur le bouton ▶️ « Run » de VS Code sur `compte.py` ou
> `test_compte.py` : ces fichiers ne s'exécutent pas seuls. Utilisez `pytest`.

### Étape 6 (optionnelle) — Lancer l'application interactive

Pour tester manuellement les dépôts / retraits via un menu :

```powershell
python -m src.main
```

> Écrivez bien `python -m src.main` (avec un point, sans `.py`).
> N'écrivez jamais `python src\main.py`.

---

## À copier-coller d'un seul bloc (Windows)

Depuis la racine `rendu_louzza_zehair` :

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
cd Partie_02\module_bancaire
pip install pytest
pytest
```

---

## Structure

```
module_bancaire/
├── README.md
├── pyproject.toml         # config pytest (pythonpath : rend `src` importable)
├── src/
│   ├── __init__.py
│   ├── exceptions.py      # MontantInvalideError, SoldeInsuffisantError
│   ├── compte.py          # classe CompteBancaire (logique métier)
│   └── main.py            # interaction utilisateur (seul fichier avec print)
└── tests/
    └── test_compte.py     # tests pytest
```

## Règles métier

1. Le solde initial ne peut pas être négatif.
2. Un dépôt doit être strictement positif.
3. Un retrait doit être strictement positif.
4. Un retrait ne peut pas dépasser le solde disponible.

## Choix techniques

- **Exceptions personnalisées** héritant de `Exception` : `MontantInvalideError` (montant non numérique, nul ou négatif) et `SoldeInsuffisantError` (retrait > solde). Elles portent un message métier clair.
- **Séparation des responsabilités** : la logique métier (`compte.py`) ne fait aucun `print()` ; l'affichage est isolé dans `main.py`.
- **Validation centralisée** : la méthode privée `_to_number()` convertit et valide tout montant, ce qui évite la duplication entre `deposer`, `retirer` et le constructeur.
- **`afficher()`** retourne un dictionnaire (`{"titulaire": ..., "solde": ...}`) plutôt que d'imprimer, pour rester testable et réutilisable.
- **Imports relatifs** (`from .exceptions import ...`) : `src` est un vrai package Python.

## Dépannage

| Erreur | Solution |
|--------|----------|
| `No module named 'pytest'` | Activez le venv puis `pip install pytest` |
| `No module named 'src'` | Lancez `pytest` depuis `Partie_02\module_bancaire`, pas depuis un autre dossier |
| `attempted relative import with no known parent package` | Vous avez cliqué « Run » sur un fichier : lancez plutôt `pytest` ou `python -m src.main` |

## Note de régression (Partie 4.2)

Si la méthode `retirer()` était modifiée pour faire `self.solde += montant` au lieu de `self.solde -= montant`, le test `test_retrait_valide_diminue_solde` échouerait immédiatement : partant d'un solde de 100 et retirant 30, on obtiendrait 130 au lieu de 70. Ce test échoue car il vérifie la règle métier fondamentale « un retrait diminue le solde ». La régression serait donc détectée dès le premier lancement de `pytest`, avant tout impact en production.
