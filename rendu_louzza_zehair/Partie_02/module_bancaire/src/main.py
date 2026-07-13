"""
Point d'entrée interactif du module bancaire.
Seul ce fichier contient des print() (interaction utilisateur).
Lancement : python -m src.main  (depuis Partie_02/module_bancaire/)
"""
from src.compte import CompteBancaire
from src.exceptions import MontantInvalideError, SoldeInsuffisantError


def main():
    print("=== Module bancaire ===")
    titulaire = input("Nom du titulaire : ")
    try:
        solde = float(input("Solde initial (€) : "))
        compte = CompteBancaire(titulaire, solde)
    except (ValueError, MontantInvalideError) as err:
        print(f"Erreur : {err}")
        return

    while True:
        print("\n1. Déposer  2. Retirer  3. Consulter  4. Quitter")
        choix = input("Choix : ").strip()
        try:
            if choix == "1":
                compte.deposer(float(input("Montant à déposer : ")))
                print(f"Nouveau solde : {compte.consulter_solde()}€")
            elif choix == "2":
                compte.retirer(float(input("Montant à retirer : ")))
                print(f"Nouveau solde : {compte.consulter_solde()}€")
            elif choix == "3":
                print(compte.afficher())
            elif choix == "4":
                break
            else:
                print("Choix invalide.")
        except (MontantInvalideError, SoldeInsuffisantError) as err:
            print(f"Erreur : {err}")
        except ValueError:
            print("Erreur : veuillez saisir un nombre valide.")


if __name__ == "__main__":
    main()
