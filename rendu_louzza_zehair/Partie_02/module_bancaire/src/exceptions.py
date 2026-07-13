"""
Exceptions personnalisées pour le module bancaire.
Ces exceptions héritent de Exception et portent un message métier clair.
"""


class MontantInvalideError(Exception):
    """
    Levée quand un montant est invalide.
    Cas d'erreur : montant non numérique, nul ou négatif.
    """

    def __init__(self, message="Le montant doit être un nombre strictement positif."):
        self.message = message
        super().__init__(self.message)


class SoldeInsuffisantError(Exception):
    """
    Levée quand un retrait dépasse le solde disponible.
    Le message indique le solde actuel et le montant demandé.
    """

    def __init__(self, solde_actuel, montant_demande):
        self.solde_actuel = solde_actuel
        self.montant_demande = montant_demande
        self.message = (
            f"Solde insuffisant : solde actuel {solde_actuel}€, "
            f"montant demandé {montant_demande}€."
        )
        super().__init__(self.message)
