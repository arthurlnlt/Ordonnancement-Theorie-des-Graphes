from tabulate import tabulate



def lecture_tableau(fichier):
    tableau = []
    try:
        with open(fichier, 'r') as file:
            for ligne in file:
                # Supprimer les espaces en trop et diviser la ligne en éléments
                elements = ligne.strip().split()
                # Le premier élément est le numéro de tâche
                numero_tache = int(elements[0])
                # Le deuxième élément est la durée de la tâche
                duree = int(elements[1])
                # Les autres éléments sont les contraintes (prédécesseurs)
                predecesseurs = list(map(int, elements[2:]))

                # Ajouter les informations au tableau
                tableau.append({
                    'numero_tache': numero_tache,
                    'duree': duree,
                    'predecesseurs': predecesseurs
                })

        return tableau

    except FileNotFoundError:
        print(f"Le fichier {fichier} n'a pas été trouvé.")
        return None
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None



def creer_matrice_adjacence(tableau):
    N = len(tableau)
    # Initialiser la matrice d'adjacence avec des zéros
    matrice = [[0] * (N + 2) for _ in range(N + 2)]

    # Remplir la matrice avec les contraintes
    for tache in tableau:
        numero_tache = tache['numero_tache']
        for predecesseur in tache['predecesseurs']:
            matrice[predecesseur][numero_tache] = 1

    # Ajouter les arcs pour les sommets fictifs α et ω
    taches_sans_predecesseur = [tache['numero_tache'] for tache in tableau if not tache['predecesseurs']]
    for tache in taches_sans_predecesseur:
        matrice[0][tache] = 1

    # Trouver les tâches sans successeurs
    taches_sans_successeur = set(range(1, N + 1))
    for tache in tableau:
        for predecesseur in tache['predecesseurs']:
            if predecesseur in taches_sans_successeur:
                taches_sans_successeur.remove(predecesseur)

    for tache in taches_sans_successeur:
        matrice[tache][N + 1] = 1

    return matrice

def afficher_matrice(matrice):
    N = len(matrice) - 2
    # Créer les en-têtes
    en_tetes = ["α"] + [f"Tâche {i}" for i in range(1, N + 1)] + ["ω"]

    # Préparer les données pour tabulate
    table = [en_tetes] + [[f"Tâche {i}" if i != 0 else "α" if i == 0 else "ω"] + ligne for i, ligne in enumerate(matrice)]

    # Afficher la matrice avec tabulate
    print(tabulate(table, headers="firstrow", tablefmt="grid"))



def verifier_graphe(matrice):
    # Nombre total de sommets (incluant α et ω)
    total_sommets = len(matrice)

    # Vérification des arcs à valeur négative
    for i in range(total_sommets):
        for j in range(total_sommets):
            if matrice[i][j] < 0:
                return False, "Le graphe contient des arcs à valeur négative."

    # Détection de circuit avec l'algorithme de Kahn (tri topologique)
    degres_entree = [0] * total_sommets
    for i in range(total_sommets):
        for j in range(total_sommets):
            if matrice[i][j] > 0:
                degres_entree[j] += 1

    file_attente = [i for i in range(total_sommets) if degres_entree[i] == 0]
    ordre_topologique = []

    while file_attente:
        sommet = file_attente.pop(0)
        ordre_topologique.append(sommet)
        for j in range(total_sommets):
            if matrice[sommet][j] > 0:
                degres_entree[j] -= 1
                if degres_entree[j] == 0:
                    file_attente.append(j)

    if len(ordre_topologique) == total_sommets:
        return True, "Le graphe ne contient pas de circuit et n'a pas d'arcs à valeur négative."
    else:
        return False, "Le graphe contient un circuit."



def calculer_rangs(matrice):
    total_sommets = len(matrice)
    degres_entree = [0] * total_sommets
    rangs = [0] * total_sommets

    # Calculer le degré d'entrée de chaque sommet
    for i in range(total_sommets):
        for j in range(total_sommets):
            if matrice[i][j] > 0:
                degres_entree[j] += 1

    # Initialiser la file d'attente avec les sommets sans prédécesseurs
    file_attente = [i for i in range(total_sommets) if degres_entree[i] == 0]
    ordre_topologique = []

    # Calculer les rangs
    rang = 0
    while file_attente:
        sommet = file_attente.pop(0)
        ordre_topologique.append(sommet)
        rangs[sommet] = rang
        rang += 1
        for j in range(total_sommets):
            if matrice[sommet][j] > 0:
                degres_entree[j] -= 1
                if degres_entree[j] == 0:
                    file_attente.append(j)

    if len(ordre_topologique) == total_sommets:
        return rangs
    else:
        raise ValueError("Le graphe contient un cycle, les rangs ne peuvent pas être calculés.")







def calculer_calendriers(matrice, tableau):
    total_sommets = len(matrice)
    calendrier_plus_tot = [0] * total_sommets
    calendrier_plus_tard = [0] * total_sommets
    marges = [0] * total_sommets

    # Calcul du calendrier au plus tôt
    for i in range(total_sommets):
        if i == 0:
            calendrier_plus_tot[i] = 0
        else:
            # Trouver la durée de la tâche
            tache = next((t for t in tableau if t['numero_tache'] == i), None)
            duree = tache['duree'] if tache else 0
            calendrier_plus_tot[i] = max([calendrier_plus_tot[j] for j in range(total_sommets) if matrice[j][i] > 0], default=0) + duree

    # Calcul du calendrier au plus tard
    date_fin_projet = calendrier_plus_tot[-1]
    calendrier_plus_tard[-1] = date_fin_projet

    for i in range(total_sommets - 2, -1, -1):
        if i == 0:
            calendrier_plus_tard[i] = 0
        else:
            # Trouver la durée de la tâche
            tache = next((t for t in tableau if t['numero_tache'] == i), None)
            duree = tache['duree'] if tache else 0
            calendrier_plus_tard[i] = min([calendrier_plus_tard[j] for j in range(total_sommets) if matrice[i][j] > 0], default=date_fin_projet) - duree

    # Calcul des marges
    for i in range(1, total_sommets - 1):
        marges[i] = calendrier_plus_tard[i] - calendrier_plus_tot[i]

    return calendrier_plus_tot, calendrier_plus_tard, marges




def calculer_chemin_critique(matrice, calendrier_plus_tot, calendrier_plus_tard):
    total_sommets = len(matrice)
    marges = [calendrier_plus_tard[i] - calendrier_plus_tot[i] for i in range(total_sommets)]

    # Trouver les tâches critiques
    taches_critiques = [i for i in range(1, total_sommets - 1) if marges[i] == 0]

    # Construire le chemin critique
    chemin_critique = []
    for tache in taches_critiques:
        chemin_critique.append(tache)

    # Afficher le chemin critique
    print("Le chemin critique est :")
    for tache in chemin_critique:
        print(f"Tâche {tache}", end=" -> ")
    print("Fin")

    return chemin_critique




