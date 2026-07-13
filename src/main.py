"""
Point d'entrée : interaction utilisateur avec gestion contrôlée des erreurs.
Affiche des messages métier pour l'utilisateur + traceback pour le développeur.
"""

import traceback
import sys
from compte_bancaire import CompteBancaire
from exceptions import MontantInvalideError, SoldeInsuffisantError


def afficher_menu():
    """Affiche le menu des actions disponibles."""
    print("\n=== MENU COMPTE BANCAIRE ===")
    print("1. Déposer")
    print("2. Retirer")
    print("3. Consulter solde")
    print("4. Quitter")
    print("============================\n")


def main():
    """
    Fonction principale : gère l'interaction avec l'utilisateur.
    Gère les erreurs de conversion et les exceptions métier.
    """
    print("Bienvenue dans le système bancaire!")
    
    # Initialiser le compte avec un solde de départ
    try:
        solde_depart = input("Entrez le solde initial du compte (€): ")
        compte = CompteBancaire(float(solde_depart))
        print(f"✓ Compte créé avec un solde de {compte.consulter_solde()}€")
    except ValueError:
        print("✗[MÉTIER] Erreur : le solde initial doit être un nombre.")
        print("\n[TECHNIQUE] Traceback :")
        traceback.print_exc()
        return
    except MontantInvalideError as e:
        print(f"✗[MÉTIER] Erreur métier : {e.message}")
        print("\n[TECHNIQUE] Traceback :")
        traceback.print_exc()
        return
    
    # Boucle principale
    while True:
        afficher_menu()
        choix = input("Choisissez une action (1-4): ").strip()
        
        if choix == "4":
            print("Au revoir!")
            break
        
        elif choix == "1":  # Dépôt
            try:
                montant = input("Montant à déposer (€): ").strip()
                compte.deposer(montant)
                print(f"✓ Dépôt de {montant}€ effectué.")
                print(f"  Nouveau solde : {compte.consulter_solde()}€")
            except ValueError:
                print("✗[MÉTIER] Erreur : le montant doit être un nombre valid.")
                print("\n[TECHNIQUE] Traceback :")
                traceback.print_exc()
            except MontantInvalideError as e:
                print(f"✗[MÉTIER] Erreur métier : {e.message}")
                print("\n[TECHNIQUE] Traceback :")
                traceback.print_exc()
        
        elif choix == "2":  # Retrait
            try:
                montant = input("Montant à retirer (€): ").strip()
                compte.retirer(montant)
                print(f"✓ Retrait de {montant}€ effectué.")
                print(f"  Nouveau solde : {compte.consulter_solde()}€")
            except ValueError:
                print("✗[MÉTIER] Erreur : le montant doit être un nombre valide.")
                print("\n[TECHNIQUE] Traceback :")
                traceback.print_exc()
            except MontantInvalideError as e:
                print(f"✗[MÉTIER] Erreur métier : {e.message}")
                print("\n[TECHNIQUE] Traceback :")
                traceback.print_exc()
            except SoldeInsuffisantError as e:
                print(f"✗[MÉTIER] Erreur métier : {e.message}")
                print("\n[TECHNIQUE] Traceback :")
                traceback.print_exc()
        
        elif choix == "3":  # Consulter solde
            solde = compte.consulter_solde()
            print(f"✓ Solde actuel : {solde}€")
        
        else:
            print("✗ Choix invalide. Veuillez entrer 1, 2, 3 ou 4.")


if __name__ == "__main__":
    main()
