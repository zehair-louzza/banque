<!-- Corrected markdown table -->
# Projet Mini-Système Bancaire Robuste

## Structure du projet

```
banque/
├── src/
│   ├── __init__.py
│   ├── exceptions.py         # Exceptions personnalisées
│   ├── compte_bancaire.py    # Logique métier
│   └── main.py               # Point d'entrée (interaction utilisateur)
└── test/
    ├── __init__.py
    └── test_compte_bancaire.py  # Suite de tests pytest
```

---

## Comment lancer les tests

### Installation de pytest (si nécessaire)
```bash
pip install pytest
```

### Lancer tous les tests
```bash
pytest test/test_compte_bancaire.py -v
```

### Lancer les tests avec les marqueurs
```bash
pytest test/test_compte_bancaire.py -v --tb=short
pytest test/test_compte_bancaire.py -v -m "not skip"  # Exclure les tests marqués skip
```

### Lancer un test spécifique
```bash
pytest test/test_compte_bancaire.py::TestCasOK::test_depot_valide_augmente_solde -v
```

---

## Règles métier appliquées

1. **Montant strictement positif** : Tout dépôt/retrait doit avoir un montant > 0.
   - Exception levée : `MontantInvalideError`
   - Cas testés : montants négatifs, nuls, non numériques

2. **Solde ne peut pas devenir négatif** : Un retrait ne peut pas dépasser le solde disponible.
   - Exception levée : `SoldeInsuffisantError`
   - Cas testés : retrait > solde, retrait = solde (OK)

3. **Solde initial valide** : Un compte ne peut pas être créé avec un solde initial négatif.
   - Exception levée : `MontantInvalideError`

4. **Gestion des erreurs de conversion** : Les entrées utilisateur sont converties en nombres.
   - Exception capturée : `ValueError` → remontée comme `MontantInvalideError`

---

## Simulation de régression (Partie F)

### État normal : tous les tests passent
```bash
pytest test/test_compte_bancaire.py -v
# Résultat : 15 passed (tous les tests réussissent)
```

### Régression simulée : modification du code métier

**Fichier `src/compte_bancaire.py` - Ligne ~70 :**

**Avant (code correct) :**
```python
self._solde -= montant
```

**Après (régression) :**
```python
self._solde += montant  # BUG : on ajoute au lieu de retirer !
```

### Détection de la régression

En relançant les tests :
```bash
pytest test/test_compte_bancaire.py -v
```

**Tests qui échouent :**
- `test_retrait_valide_diminue_solde`
- `test_multiples_retraits_successifs`
- `test_depot_et_retrait_succession`
- `test_retrait_egal_au_solde`
- `test_solde_zero_puis_depot`

**Explanation :**
> Le premier test `test_retrait_valide_diminue_solde` échoue car au lieu de diminuer le solde de 30€ (100 - 30 = 70), le code ajoute 30€ (100 + 30 = 130). Cela viole la règle métier "un retrait doit diminuer le solde". Les autres tests échouent en cascade car ils supposent que les retraits réduisent le solde.

---

## Marqueurs pytest utilisés (Partie G)

### 1. Skip simple (raison informelle)
```python
@pytest.mark.skip(reason="Fonctionnalité future : frais bancaires non implémentée")
def test_application_frais_mensuels(self):
    pass
```
**Utilisé pour :** Ignorer les tests en attente de fonctionnalités futures.

### 2. Skip conditionnel (skipif)
```python
@pytest.mark.skipif(sys.version_info < (3, 9), reason="Requiert Python 3.9+")
def test_type_hints_compatibilité(self):
    pass
```
**Utilisé pour :** Ignorer les tests selon une condition (ici : version Python < 3.9).

### 3. Résultat visible dans pytest
```bash
pytest test/test_compte_bancaire.py -v
# Affiche :
# test_compte_bancaire.py::TestMarqueurs::test_application_frais_mensuels SKIPPED  [...]
# test_compte_bancaire.py::TestMarqueurs::test_type_hints_compatibilité SKIPPED  [...]
```

---

## Couverture des tests (Partie E)

| Catégorie | Cas testés |
|-----------|-----------|
| **Dépôts** | Montant valide, montant négatif/nul, montant texte, montants décimaux, gros montants |
| **Retraits** | Montant valide, montant négatif/nul, montant texte, solde insuffisant, retrait = solde |
| **Consultations** | Solde initial, solde après opérations |
| **Créations** | Solde initial valide, solde initial négatif |
| **Séquences** | Multiples dépôts, multiples retraits, alternance dépôt/retrait |
| **Edge cases** | Solde zéro, compte bien épuisé puis dépôt |

**Total : 17 tests fonctionnels + 3 tests avec marqueurs = 20 tests**

---

## Exécution complète du projet

### Lancer les tests
```bash
cd banque
pytest test/test_compte_bancaire.py -v
```

### Lancer l'application interactive
```bash
cd src
python main.py
```

Exemple d'interactionnelle :
```
Bienvenue dans le système bancaire!
Entrez le solde initial du compte (€): 100
✓ Compte créé avec un solde de 100€

=== MENU COMPTE BANCAIRE ===
1. Déposer
2. Retirer
3. Consulter solde
4. Quitter
============================

Choisissez une action (1-4): 1
Montant à déposer (€): 50
✓ Dépôt de 50€ effectué.
  Nouveau solde : 150€
```

---

## Notes finales

- ✅ **Exceptions personnalisées** : `MontantInvalideError`, `SoldeInsuffisantError`
- ✅ **Gestion des erreurs** : Messages métier + traceback technique
- ✅ **Tests unitaires** : Séparation src/ et test/, pas d'effet de bord
- ✅ **Détection de régression** : Changement volontaire au retrait break 5+ tests
- ✅ **Marqueurs pytest** : skip + skipif utilisés
- ✅ **Couverture** : 17 tests fonctionnels + 3 marqués + séquences complexes
