"""
Exceptions personnalisées pour le module bancaire.
Ces exceptions portent des messages "métier" clairs pour l'utilisateur.
"""


class MontantInvalideError(Exception):
    """
    Exception déclenchée quand un montant est invalide.
    Cas d'erreur : montant négatif, nul ou non numérique.
    Message : clair pour l'utilisateur final.
    """
    def __init__(self, message="Le montant doit être strictement positif."):
        self.message = message
        super().__init__(self.message)


class SoldeInsuffisantError(Exception):
    """
    Exception déclenchée quand le solde est insuffisant pour un retrait.
    Cas d'erreur : montant du retrait > solde disponible.
    Message : indique le solde actuel et ce qui est demandé.
    """
    def __init__(self, solde_actuel, montant_demande):
        self.solde_actuel = solde_actuel
        self.montant_demande = montant_demande
        self.message = (
            f"Solde insuffisant. Solde actuel: {solde_actuel}€, "
            f"montant demandé: {montant_demande}€"
        )
        super().__init__(self.message)
