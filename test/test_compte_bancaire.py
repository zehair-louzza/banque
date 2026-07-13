"""
Tests unitaires pour le module bancaire.
Utilise pytest pour tester les règles métier et la gestion des exceptions.

Structure des tests :
- D1 : Cas "OK" (dépôt, retrait, consultation)
- D2 : Cas d'erreurs métier (montant invalide, solde insuffisant)
- E  : Couverture supplémentaire (multiples opérations, montants décimaux)
- G  : Marqueurs pytest (skip, skipif)
"""

import pytest
import sys
import os

# Ajoute le répertoire src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from compte_bancaire import CompteBancaire
from exceptions import MontantInvalideError, SoldeInsuffisantError


# ============================================================================
# D1 : TESTS DES CAS "OK"
# ============================================================================

class TestCasOK:
    """Tests des cas de fonctionnement normal."""
    
    def test_depot_valide_augmente_solde(self):
        """Un dépôt valide doit augmenter le solde."""
        compte = CompteBancaire(100)
        compte.deposer(50)
        assert compte.consulter_solde() == 150
    
    def test_retrait_valide_diminue_solde(self):
        """Un retrait valide doit diminuer le solde."""
        compte = CompteBancaire(100)
        compte.retirer(30)
        assert compte.consulter_solde() == 70
    
    def test_consultation_solde_initial(self):
        """Consulter le solde initial doit renvoyer la bonne valeur."""
        solde_initial = 250.50
        compte = CompteBancaire(solde_initial)
        assert compte.consulter_solde() == solde_initial
    
    def test_consultation_solde_apres_operations(self):
        """Consulter le solde après opérations."""
        compte = CompteBancaire(100)
        compte.deposer(50)
        compte.retirer(20)
        assert compte.consulter_solde() == 130


# ============================================================================
# D2 : TESTS DES CAS D'ERREURS MÉTIER
# ============================================================================

class TestErreursMétier:
    """Tests des exceptions métier."""
    
    # Montant invalide pour dépôt
    def test_depot_montant_negatif_leve_exception(self):
        """Un dépôt avec montant négatif doit lever MontantInvalideError."""
        compte = CompteBancaire(100)
        with pytest.raises(MontantInvalideError):
            compte.deposer(-50)
    
    def test_depot_montant_nul_leve_exception(self):
        """Un dépôt avec montant nul doit lever MontantInvalideError."""
        compte = CompteBancaire(100)
        with pytest.raises(MontantInvalideError):
            compte.deposer(0)
    
    # Montant invalide pour retrait
    def test_retrait_montant_negatif_leve_exception(self):
        """Un retrait avec montant négatif doit lever MontantInvalideError."""
        compte = CompteBancaire(100)
        with pytest.raises(MontantInvalideError):
            compte.retirer(-30)
    
    def test_retrait_montant_nul_leve_exception(self):
        """Un retrait avec montant nul doit lever MontantInvalideError."""
        compte = CompteBancaire(100)
        with pytest.raises(MontantInvalideError):
            compte.retirer(0)
    
    # Solde insuffisant
    def test_retrait_superieur_au_solde_leve_exception(self):
        """Un retrait supérieur au solde doit lever SoldeInsuffisantError."""
        compte = CompteBancaire(50)
        with pytest.raises(SoldeInsuffisantError):
            compte.retirer(100)
    
    # Compte initial invalide
    def test_compte_solde_initial_negatif_leve_exception(self):
        """Un compte avec solde initial négatif doit lever MontantInvalideError."""
        with pytest.raises(MontantInvalideError):
            CompteBancaire(-100)
    
    # Montant non numérique
    def test_depot_montant_texte_leve_exception(self):
        """Un dépôt avec montant textuel doit lever MontantInvalideError."""
        compte = CompteBancaire(100)
        with pytest.raises(MontantInvalideError):
            compte.deposer("abc")
    
    def test_retrait_montant_texte_leve_exception(self):
        """Un retrait avec montant textuel doit lever MontantInvalideError."""
        compte = CompteBancaire(100)
        with pytest.raises(MontantInvalideError):
            compte.retirer("xyz")


# ============================================================================
# E : TESTS SUPPLÉMENTAIRES - COUVERTURE ÉTENDUE
# ============================================================================

class TestCouvertureEtendue:
    """Tests supplémentaires pour couvrir plusieurs comportements."""
    
    def test_multiples_depots_successifs(self):
        """Plusieurs dépôts successifs doivent augmenter le solde correctement."""
        compte = CompteBancaire(0)
        compte.deposer(100)
        compte.deposer(50)
        compte.deposer(25)
        assert compte.consulter_solde() == 175
    
    def test_multiples_retraits_successifs(self):
        """Plusieurs retraits successifs doivent diminuer le solde correctement."""
        compte = CompteBancaire(200)
        compte.retirer(50)
        compte.retirer(30)
        compte.retirer(20)
        assert compte.consulter_solde() == 100
    
    def test_depot_et_retrait_succession(self):
        """Dépôt suivi d'un retrait doit laisser le solde correct."""
        compte = CompteBancaire(100)
        compte.deposer(150)  # Solde = 250
        compte.retirer(75)   # Solde = 175
        compte.deposer(50)   # Solde = 225
        compte.retirer(125)  # Solde = 100
        assert compte.consulter_solde() == 100
    
    def test_montant_decimal_accepte(self):
        """Les montants décimaux doivent être acceptés et traités correctement."""
        compte = CompteBancaire(100.50)
        compte.deposer(25.75)
        compte.retirer(10.25)
        assert compte.consulter_solde() == pytest.approx(116)
    
    def test_gros_montant(self):
        """Les gros montants doivent être traités correctement."""
        compte = CompteBancaire(1000000)
        compte.deposer(500000)
        compte.retirer(250000)
        assert compte.consulter_solde() == 1250000
    
    def test_retrait_egal_au_solde(self):
        """Un retrait égal au solde doit réduire le solde à zéro."""
        compte = CompteBancaire(100)
        compte.retirer(100)
        assert compte.consulter_solde() == 0
    
    def test_solde_zero_puis_depot(self):
        """Après épuisement du solde, un dépôt doit fonctionner."""
        compte = CompteBancaire(100)
        compte.retirer(100)
        assert compte.consulter_solde() == 0
        compte.deposer(50)
        assert compte.consulter_solde() == 50
    
    def test_compte_crée_sans_solde_initial(self):
        """Un compte créé sans solde initial doit avoir 0€."""
        compte = CompteBancaire()
        assert compte.consulter_solde() == 0


# ============================================================================
# G : MARQUEURS PYTEST
# ============================================================================

class TestMarqueurs:
    """Tests avec marqueurs pytest (skip, skipif)."""
    
    @pytest.mark.skip(reason="Fonctionnalité future : frais bancaires non implémentée")
    def test_application_frais_mensuels(self):
        """Test futur : appliquer des frais mensuels (à implémenter)."""
        compte = CompteBancaire(100)
        # compte.appliquer_frais_mensuels()
        # assert compte.consulter_solde() == 95
        pass
    
    @pytest.mark.skipif(sys.version_info < (3, 9), reason="Requiert Python 3.9+")
    def test_type_hints_compatibilité(self):
        """Test des type hints (Python 3.9+)."""
        compte: CompteBancaire = CompteBancaire(100)
        assert isinstance(compte, CompteBancaire)
    
    @pytest.mark.skip(reason="À revoir : validation des soldes très négatifs")
    def test_tres_negatif_edge_case(self):
        """Edge case : soldes extrêmement négatifs."""
        pass
