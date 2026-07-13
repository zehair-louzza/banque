"""
Démonstration de régression - VERSION BUGGUÉE
Ce fichier montre ce qui se passe si on change -= en += dans retirer()
"""

from exceptions import MontantInvalideError, SoldeInsuffisantError


class CompteBancaireBugge:
    """
    VERSION AVEC BUG : au lieu de retirer, on AJOUTE le montant !
    """
    
    def __init__(self, solde_initial=0):
        if solde_initial < 0:
            raise MontantInvalideError(
                "Le solde initial ne peut pas être négatif."
            )
        self._solde = float(solde_initial)
    
    def deposer(self, montant):
        try:
            montant = float(montant)
        except (ValueError, TypeError):
            raise MontantInvalideError(
                "Le montant doit être un nombre valide."
            )
        
        if montant <= 0:
            raise MontantInvalideError(
                "Le montant du dépôt doit être strictement positif."
            )
        
        self._solde += montant
    
    def retirer(self, montant):
        """BUG ICI : on ajoute au lieu de retirer !"""
        try:
            montant = float(montant)
        except (ValueError, TypeError):
            raise MontantInvalideError(
                "Le montant doit être un nombre valide."
            )
        
        if montant <= 0:
            raise MontantInvalideError(
                "Le montant du retrait doit être strictement positif."
            )
        
        if montant > self._solde:
            raise SoldeInsuffisantError(self._solde, montant)
        
        self._solde += montant  # BUG : au lieu de -= montant
    
    def consulter_solde(self):
        return self._solde
