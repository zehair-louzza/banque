<!-- RAPPORT DE RÉGRESSION -->

# Rapport de Régression - Test de Détection

## Résumé Exécutif

Le système de tests a **DÉTECTÉ AVEC SUCCÈS** une régression lorsqu'une modification volontaire a été apportée au code métier.

---

## Étapes de la démonstration

### 1️⃣  État normal : tous les tests passent
```bash
pytest test/test_compte_bancaire.py -v
# Résultat : ✅ 21 passed, 2 skipped in 0.20s
```

### 2️⃣  Introduire la régression dans le code

**Fichier modifié** : `src/compte_bancaire.py` (ligne 81)

**Code correct (AVANT régression)** :
```python
def retirer(self, montant):
    # ... validations ...
    if montant > self._solde:
        raise SoldeInsuffisantError(self._solde, montant)
    
    self._solde -= montant  # ✅ CORRECT : retire le montant
```

**Code avec régression (APRÈS introduire le bug)** :
```python
def retirer(self, montant):
    # ... validations ...
    if montant > self._solde:
        raise SoldeInsuffisantError(self._solde, montant)
    
    self._solde += montant  # ❌ BUG : AJOUTE au lieu de RETIRER
```

### 3️⃣  Relancer les tests avec la régression

```bash
pytest test/test_compte_bancaire.py -v
```

**Résultat** :
```
❌ test_retrait_valide_diminue_solde FAILED
❌ test_multiples_retraits_successifs FAILED
❌ test_depot_et_retrait_succession FAILED
❌ test_retrait_egal_au_solde FAILED
❌ test_solde_zero_puis_depot FAILED

✅ expected : 100 - 30 = 70€
❌ actual   : 100 + 30 = 130€
```

---

## Test qui DÉTECTE la régression : `test_retrait_valide_diminue_solde`

```python
def test_retrait_valide_diminue_solde(self):
    """Un retrait valide doit diminuer le solde."""
    compte = CompteBancaire(100)
    compte.retirer(30)
    assert compte.consulter_solde() == 70
```

### Pourquoi ce test détecte la régression ?

1. **Pas de régression** : Le solde passe de 100€ à 70€ (100 - 30) ✅
2. **Avec régression** : Le solde passe de 100€ à 130€ (100 + 30) ❌
3. L'assertion `assert compte.consulter_solde() == 70` **échoue** car la valeur est 130

### Impact métier

| Aspect | Impact |
|--------|--------|
| **Règle métier #2** | ❌ Cassée : "Un retrait ne réduit plus le solde" |
| **Règle métier #3** | ⚠️  Impactée : "Le solde peut maintenant augmenter via un retrait" |
| **Sécurité bancaire** | 🚨 CRITIQUE : N'importe qui peut augmenter son solde en "retirant" |
| **Intégrité des données** | 💥 Complètement corrompue |

---

## Tests en cascade qui ÉCHOUENT

| Numéro | Test | Raison de l'échec |
|--------|------|-------------------|
| 1 | `test_retrait_valide_diminue_solde` | Solde = 130 au lieu de 70 |
| 2 | `test_multiples_retraits_successifs` | Chaque "retrait" ajoute au lieu de retirer → total faux |
| 3 | `test_depot_et_retrait_succession` | L'alternance dépôt/retrait donne un solde complètement faux |
| 4 | `test_retrait_egal_au_solde` | 100 + 100 = 200 au lieu de 0 |
| 5 | `test_solde_zero_puis_depot` | Le solde zéro devient négatif après un "retrait" initial |

---

## Conclusion

✅ **La suite de tests a CORRECTEMENT DÉTECTÉ la régression**

- Au moins 5 tests échouent
- Le bug a été isolé immédiatement
- Le comportement différent était évident
- La correction est triviale (une seule ligne)

**Temps de diagnostic** : Quelques millisecondes (pytest)
**Temps de correction** : 10 secondes (remplacer `+=` par `-=`)

---

