import os
import re
from functions import *

def main():
    # Ouvrir un fichier pour écrire la sortie
    with open("test.txt", 'w') as f:
        message = "Projet de théorie des graphes\n\n"
        print(message)
        f.write(message)

        message = "Par Ryan Crohas, Rayan Djalali-Moghadam, Mathieu Gasnier, Ethan Guingand, Arthur Lainault\n\n"
        print(message)
        f.write(message)

        # Dossier contenant les fichiers de contraintes
        folder = "tables"
        if not os.path.isdir(folder):
            message = "Le dossier 'tables' n'existe pas. Fin du programme.\n"
            print(message)
            f.write(message)
            return

        while True:
            # Lister les fichiers disponibles dans le dossier et les trier par numéro croissant
            files = []
            for file in os.listdir(folder):
                if file.endswith(".txt"):
                    # Extraction du premier nombre présent dans le nom du fichier
                    m = re.search(r'\d+', file)
                    num = int(m.group()) if m else float('inf')
                    files.append((num, file))
            files.sort(key=lambda x: x[0])

            if not files:
                message = "Aucun fichier de contraintes trouvé dans le dossier. Fin du programme.\n"
                print(message)
                f.write(message)
                return

            # Afficher les options de fichiers
            message = "\nSélectionnez le fichier de contraintes à utiliser (ou tapez 'quitter' pour quitter) :\n\n"
            print(message)
            f.write(message)
            for i, (_, filename) in enumerate(files, start=1):
                message = f"{i}. {filename}"
                print(message)
                f.write(message + "\n")

            choix = input("\nEntrez le numéro du fichier à utiliser (ou 'quitter' pour quitter) : ")
            if choix.lower() == "quitter":
                message = "Fin du programme.\n"
                print(message)
                f.write(message)
                break

            try:
                choix = int(choix)
                if 1 <= choix <= len(files):
                    file_selected = os.path.join(folder, files[choix - 1][1])
                else:
                    message = "Choix invalide."
                    print(message)
                    f.write(message)
                    continue
            except ValueError:
                message = "Entrée non valide."
                print(message)
                f.write(message)
                continue

            message = f"Fichier sélectionné : {file_selected}\n"
            print(message)
            f.write(message)

            # Lecture et traitement du fichier sélectionné
            tableau = lecture_tableau(file_selected)
            if not tableau:
                continue

            # Affichage du tableau de contraintes
            message = "* Affichage du tableau de contraintes :"
            print(message)
            f.write(message + "\n")
            for tache in tableau:
                message = f"{tache}"
                print(message)
                f.write(message + "\n")

            # Ajout des tâches alpha et omega
            tableau = ajouter_alpha_omega(tableau)

            # Création et affichage de la matrice d'adjacence
            matrice = creer_matrice_adjacence(tableau)
            message = "\nMatrice d'adjacence :\n"
            print(message)
            f.write(message)
            afficher_matrice(matrice, f)

            # Vérification du graphe
            if verification_graphe(tableau, f):

                # Calcul des rangs et de l'ordre topologique
                rangs, ordre_topo = calculer_rangs(tableau)

                # Calcul des calendriers (dates au plus tôt et au plus tard)
                temps_tot, temps_tar = calcul_calendrier(tableau)

                # Calcul des marges totales
                marge_totale = [temps_tar[t] - temps_tot[t] for t in range(len(tableau))]

                # Affichage des résultats
                message = "\n* Résultats des calculs du calendrier et des marges :"
                print(message)
                f.write(message)
                afficher_resultats(tableau, temps_tot, temps_tar, rangs, ordre_topo, f)

                # Affichage du chemin critique
                message = "* Chemin(s) critique(s) :\n"
                print(message)
                print(chemin_critique(tableau, temps_tot, marge_totale))
                f.write(message)
                f.write(chemin_critique(tableau, temps_tot, marge_totale))

            else:
                message = "\n-> Ce n’est pas un graphe d’ordonnancement\n"
                print(message)
                f.write(message)

            # Demander si l'utilisateur souhaite traiter un autre fichier
            rep = input("\nVoulez-vous traiter un autre fichier ? (O/N) : ")
            if rep.lower() not in ["o", "oui"]:
                message = "Fin du programme.\n"
                print(message)
                f.write(message)
                break

if __name__ == "__main__":
    main()
