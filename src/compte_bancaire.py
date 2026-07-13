"""
Module CompteBancaire : gère un compte bancaire avec règles métier.
Les règles métier sont appliquées via des exceptions personnalisées.
"""

from exceptions import MontantInvalideError, SoldeInsuffisantError


class CompteBancaire:
    """
    Classe représentant un compte bancaire.
    
    Règles métier :
    1. Un montant doit être numérique et strictement positif.
    2. Un retrait ne peut pas dépasser le solde disponible.
    3. Le solde ne doit jamais devenir négatif.
    """
    
    def __init__(self, solde_initial=0):
        """
        Initialise un compte bancaire avec un solde initial.
        
        Args:
            solde_initial (float): Solde initial du compte (par défaut 0).
            
        Raises:
            MontantInvalideError: Si le solde initial est négatif.
        """
        if solde_initial < 0:
            raise MontantInvalideError(
                "Le solde initial ne peut pas être négatif."
            )
        self._solde = float(solde_initial)
    
    def deposer(self, montant):
        """
        Effectue un dépôt sur le compte.
        
        Args:
            montant (float): Montant à déposer.
            
        Raises:
            MontantInvalideError: Si le montant n'est pas strictement positif.
        """
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
        """
        Effectue un retrait sur le compte.
        
        Args:
            montant (float): Montant à retirer.
            
        Raises:
            MontantInvalideError: Si le montant n'est pas strictement positif.
            SoldeInsuffisantError: Si le montant dépasse le solde disponible.
        """
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
        
        self._solde -= montant
    
    def consulter_solde(self):
        """
        Consulte le solde actuel du compte.
        
        Returns:
            float: Solde actuel du compte.
        """
        return self._solde
