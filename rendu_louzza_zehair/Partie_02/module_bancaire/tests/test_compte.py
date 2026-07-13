"""
Tests unitaires du module bancaire (Partie 2 et Partie 4).

Couverture des tests obligatoires (Partie 4.1) :
- un dépôt valide augmente le solde ;
- un retrait valide diminue le solde ;
- un retrait supérieur au solde déclenche SoldeInsuffisantError ;
- un montant négatif ou nul déclenche MontantInvalideError.

Un marqueur pytest (skip) est ajouté (Partie 4.3).
"""
import sys

import pytest

from src.compte import CompteBancaire
from src.exceptions import MontantInvalideError, SoldeInsuffisantError


# --------------------------------------------------------------------------
# Cas nominaux (règles métier valides)
# --------------------------------------------------------------------------
def test_depot_valide_augmente_solde():
    """Un dépôt valide augmente le solde."""
    compte = CompteBancaire("Louzza", 100)
    compte.deposer(50)
    assert compte.consulter_solde() == 150


def test_retrait_valide_diminue_solde():
    """Un retrait valide diminue le solde."""
    compte = CompteBancaire("Louzza", 100)
    compte.retirer(30)
    assert compte.consulter_solde() == 70


def test_afficher_retourne_dictionnaire():
    """La méthode afficher() retourne bien un dictionnaire complet."""
    compte = CompteBancaire("Zehair", 200)
    assert compte.afficher() == {"titulaire": "Zehair", "solde": 200.0}


# --------------------------------------------------------------------------
# Cas d'erreur métier
# --------------------------------------------------------------------------
def test_retrait_superieur_au_solde_leve_solde_insuffisant():
    """Un retrait supérieur au solde déclenche SoldeInsuffisantError."""
    compte = CompteBancaire("Louzza", 50)
    with pytest.raises(SoldeInsuffisantError):
        compte.retirer(100)


def test_depot_montant_negatif_leve_montant_invalide():
    """Un dépôt négatif déclenche MontantInvalideError."""
    compte = CompteBancaire("Louzza", 100)
    with pytest.raises(MontantInvalideError):
        compte.deposer(-10)


def test_depot_montant_nul_leve_montant_invalide():
    """Un dépôt nul déclenche MontantInvalideError."""
    compte = CompteBancaire("Louzza", 100)
    with pytest.raises(MontantInvalideError):
        compte.deposer(0)


def test_retrait_montant_negatif_leve_montant_invalide():
    """Un retrait négatif déclenche MontantInvalideError."""
    compte = CompteBancaire("Louzza", 100)
    with pytest.raises(MontantInvalideError):
        compte.retirer(-5)


def test_solde_initial_negatif_leve_montant_invalide():
    """Un solde initial négatif déclenche MontantInvalideError."""
    with pytest.raises(MontantInvalideError):
        CompteBancaire("Louzza", -100)


def test_montant_non_numerique_leve_montant_invalide():
    """Un montant non numérique déclenche MontantInvalideError."""
    compte = CompteBancaire("Louzza", 100)
    with pytest.raises(MontantInvalideError):
        compte.deposer("abc")


# --------------------------------------------------------------------------
# Marqueur pytest (Partie 4.3)
# --------------------------------------------------------------------------
@pytest.mark.skip(reason="Fonctionnalité de frais bancaires non encore implémentée.")
def test_application_frais_mensuels():
    """Test futur : application de frais mensuels (à implémenter)."""
    compte = CompteBancaire("Louzza", 100)
    # compte.appliquer_frais(5)
    # assert compte.consulter_solde() == 95
    pass


@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="Nécessite Python 3.9+ pour les type hints."
)
def test_type_hints_python_39():
    """Vérification de compatibilité Python 3.9+."""
    compte: CompteBancaire = CompteBancaire("Louzza", 100)
    assert isinstance(compte, CompteBancaire)
