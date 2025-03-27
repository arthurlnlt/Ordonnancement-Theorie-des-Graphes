from functions import *

tableau = lecture_tableau('test.txt')
if tableau:
    matrice = creer_matrice_adjacence(tableau)
    print("Matrice d'adjacence :")
    afficher_matrice(matrice)
    est_valide, message = verifier_graphe(matrice)
    print("Le graphe est-il valide ?")
    print(est_valide,":", message)

    rangs = calculer_rangs(matrice)
    print("Rangs des sommets :")
    for i, rang in enumerate(rangs):
        if i == 0:
            print(f"α: rang {rang}")
        elif i == len(tableau) - 1:
            print(f"ω: rang {rang}")
        else:
            print(f"Tâche {i}: rang {rang}")

    calendrier_plus_tot, calendrier_plus_tard, marges = calculer_calendriers(matrice, tableau)

    print("\nCalendrier au plus tôt :")
    for i, date in enumerate(calendrier_plus_tot):
        if i == 0:
            print(f"α: {date}")
        elif i == len(matrice) - 1:
            print(f"ω: {date}")
        else:
            print(f"Tâche {i}: {date}")

    print("\nCalendrier au plus tard :")
    for i, date in enumerate(calendrier_plus_tard):
        if i == 0:
            print(f"α: {date}")
        elif i == len(matrice) - 1:
            print(f"ω: {date}")
        else:
            print(f"Tâche {i}: {date}")

    print("\nMarges :")
    for i, marge in enumerate(marges):
        if i == 0 or i == len(matrice) - 1:
            continue
        print(f"Tâche {i}: {marge}")

    calculer_chemin_critique(matrice, calendrier_plus_tot, calendrier_plus_tard)