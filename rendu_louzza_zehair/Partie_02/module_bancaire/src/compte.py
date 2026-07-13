"""
Module compte : classe CompteBancaire avec ses règles métier.
Aucune fonction métier ne contient de print() : l'affichage relève de main.py.
Les erreurs métier sont signalées via des exceptions personnalisées.
"""

# Import relatif : compte.py et exceptions.py appartiennent au même package src.
from .exceptions import MontantInvalideError, SoldeInsuffisantError


class CompteBancaire:
    """
    Représente un compte bancaire.

    Attributs :
        titulaire (str) : nom du titulaire du compte.
        solde (float)   : solde courant du compte.

    Règles métier :
        - le solde initial ne peut pas être négatif ;
        - un dépôt doit être strictement positif ;
        - un retrait doit être strictement positif ;
        - un retrait ne peut pas dépasser le solde disponible.
    """

    def __init__(self, titulaire, solde=0):
        # Validation du solde initial : il ne peut pas être négatif.
        solde = self._to_number(solde)
        if solde < 0:
            raise MontantInvalideError("Le solde initial ne peut pas être négatif.")
        self.titulaire = titulaire
        self.solde = float(solde)

    @staticmethod
    def _to_number(valeur):
        """Convertit une valeur en float ou lève MontantInvalideError si impossible."""
        try:
            return float(valeur)
        except (ValueError, TypeError):
            raise MontantInvalideError("Le montant doit être un nombre valide.")

    def deposer(self, montant):
        """Ajoute un montant strictement positif au solde."""
        montant = self._to_number(montant)
        if montant <= 0:
            raise MontantInvalideError("Le dépôt doit être strictement positif.")
        self.solde += montant

    def retirer(self, montant):
        """Retire un montant strictement positif sans dépasser le solde."""
        montant = self._to_number(montant)
        if montant <= 0:
            raise MontantInvalideError("Le retrait doit être strictement positif.")
        if montant > self.solde:
            raise SoldeInsuffisantError(self.solde, montant)
        self.solde -= montant

    def consulter_solde(self):
        """Retourne le solde courant."""
        return self.solde

    def afficher(self):
        """Retourne un dictionnaire décrivant l'état du compte."""
        return {"titulaire": self.titulaire, "solde": self.solde}
