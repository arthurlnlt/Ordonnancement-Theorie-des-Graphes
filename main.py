import os
import re
from functions import *

def main():
    print("Projet de théorie des graphes\n")
    print("Par Ryan Crohas, Rayan Djalali-Moghadam, Mathieu Gasnier, Ethan Guingand, Arthur Lainault\n")

    # Dossier contenant les fichiers de contraintes
    folder = "tables"
    if not os.path.isdir(folder):
        print("Le dossier 'tables' n'existe pas. Fin du programme.")
        return

    while True:
        # Lister les fichiers disponibles dans le dossier et les trier par numéro croissant
        files = []
        for f in os.listdir(folder):
            if f.endswith(".txt"):
                # Extraction du premier nombre présent dans le nom du fichier
                m = re.search(r'\d+', f)
                num = int(m.group()) if m else float('inf')
                files.append((num, f))
        files.sort(key=lambda x: x[0])

        if not files:
            print("Aucun fichier de contraintes trouvé dans le dossier. Fin du programme.")
            return

        # Afficher les options de fichiers
        print("\nSélectionnez le fichier de contraintes à utiliser (ou tapez 'quitter' pour quitter) :\n")
        for i, (_, filename) in enumerate(files, start=1):
            print(f"{i}. {filename}")

        choix = input("\nEntrez le numéro du fichier à utiliser (ou 'quitter' pour quitter) : ")
        if choix.lower() == "quitter":
            print("Fin du programme.")
            break

        try:
            choix = int(choix)
            if 1 <= choix <= len(files):
                file_selected = os.path.join(folder, files[choix - 1][1])
            else:
                print("Choix invalide.")
                continue
        except ValueError:
            print("Entrée non valide.")
            continue

        print(f"\nFichier sélectionné : {file_selected}\n")

        # Lecture et traitement du fichier sélectionné
        tableau = lecture_tableau(file_selected)
        if not tableau:
            continue

        # Affichage du tableau de contraintes
        print("* Affichage du tableau de contraintes :")
        for tache in tableau:
            print(tache)

        # Ajout des tâches alpha et omega
        tableau = ajouter_alpha_omega(tableau)

        # Création et affichage de la matrice d'adjacence
        matrice = creer_matrice_adjacence(tableau)
        print("\nMatrice d'adjacence :")
        afficher_matrice(matrice)

        # Vérification du graphe
        if verification_graphe(tableau):
            print("\n-> C’est un graphe d’ordonnancement\n")

            # Calcul des rangs et de l'ordre topologique
            rangs, ordre_topo = calculer_rangs(tableau)

            # Calcul des calendriers (dates au plus tôt et au plus tard)
            temps_tot, temps_tar = calcul_calendrier(tableau)

            # Calcul des marges totales
            marge_totale = [temps_tar[t] - temps_tot[t] for t in range(len(tableau))]

            # Affichage des résultats
            print("\n* Résultats des calculs du calendrier et des marges :")
            afficher_resultats(tableau, temps_tot, temps_tar, rangs, ordre_topo)

            # Affichage du chemin critique
            print("\n* Chemin(s) critique(s) :")
            print(chemin_critique(tableau, temps_tot, marge_totale))
        else:
            print("\n-> Ce n’est pas un graphe d’ordonnancement")

        # Demander si l'utilisateur souhaite traiter un autre fichier
        rep = input("\nVoulez-vous traiter un autre fichier ? (O/N) : ")
        if rep.lower() not in ["o", "oui"]:
            print("Fin du programme.")
            break

if __name__ == "__main__":
    main()
