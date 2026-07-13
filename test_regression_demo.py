"""
Script de démonstration : Comment la régression est détectée par les tests
Ce script montre ce qui se passe avec la version bugguée.
"""

import sys
sys.path.insert(0, './src')

from REGRESSION_DEMO import CompteBancaireBugge

print("=" * 70)
print("DÉMONSTRATION : DÉTECTION DE RÉGRESSION")
print("=" * 70)

print("\nTest 1 : test_retrait_valide_diminue_solde")
print("-" * 70)
print("Code attendu :")
print("  compte = CompteBancaire(100)")
print("  compte.retirer(30)")
print("  assert compte.consulter_solde() == 70")
print()

compte = CompteBancaireBugge(100)
print(f"✓ Compte créé avec solde de 100€")
print(f"  Solde initial = {compte.consulter_solde()}€")

compte.retirer(30)
print(f"✗ Après retrait de 30€ :")
print(f"  Solde attendu : 70€")
print(f"  Solde obtenu  : {compte.consulter_solde()}€")
print(f"  ❌ ASSERTION ÉCHOUÉE : 130 != 70")

print("\n" + "=" * 70)
print("RAPPORT DE RÉGRESSION")
print("=" * 70)
print("""
TEST ÉCHOUÉ :
  - test_retrait_valide_diminue_solde

CAUSE :
  La fonction retirer() ajoute le montant au solde au lieu de le retirer.
  Ligne 49 : self._solde += montant  (BUGUÉ)
  Au lieu de : self._solde -= montant  (CORRECT)

TESTS EN CASCADE QUI ÉCHOUENT :
  1. test_retrait_valide_diminue_solde - Le retrait n'augmente pas le solde
  2. test_multiples_retraits_successifs - Les retraits donnent un mauvais total
  3. test_depot_et_retrait_succession - Le solde final est incorrect
  4. test_retrait_egal_au_solde - Le solde dépasse le maximum allowed
  5. test_solde_zero_puis_depot - Comportement imprévisible après zéro

IMPACT :
  ⚠️  La règle métier "Le solde ne doit jamais devenir négatif" n'est pas respectée
  ⚠️  Les retraits AUGMENTENT le solde au lieu de le diminuer
  ⚠️  Comportement bancaire complètement inversé = données corrompues
""")

print("\nFix : Restaurer la ligne correcte")
print("-" * 70)
print("Correction à la ligne 49 de compte_bancaire.py :")
print("  AVANT (bugué)  : self._solde += montant")
print("  APRÈS (correct): self._solde -= montant")
