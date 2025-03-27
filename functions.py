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
    matrice = [[0] * (N) for _ in range(N)]

    # Remplir la matrice avec les contraintes
    for tache in tableau:
        numero_tache = tache['numero_tache']
        for predecesseur in tache['predecesseurs']:
            matrice[predecesseur][numero_tache] = 1



    return matrice



def afficher_matrice(matrice):
    N = len(matrice) - 2
    # Créer les en-têtes de colonnes
    en_tetes_colonnes = ["α"] + [f"Tâche {i}" for i in range(1, N + 1)] + ["ω"]

    # Créer les en-têtes de lignes
    en_tetes_lignes = ["α"] + [f"Tâche {i}" for i in range(1, N + 1)] + ["ω"]

    # Préparer les données pour tabulate
    table = [en_tetes_colonnes] + [[en_tetes_lignes[i]] + ligne for i, ligne in enumerate(matrice)]

    # Afficher la matrice avec tabulate
    print(tabulate(table, headers="firstrow", tablefmt="grid"))


def ajouter_alpha_omega(tableau):
    # Identifier les tâches sans prédécesseurs
    taches_sans_predecesseurs = [t['numero_tache'] for t in tableau if not t['predecesseurs']]

    # Identifier les tâches qui ne sont pas des prédécesseurs d'autres tâches
    taches_sans_successeurs = []
    tous_predecesseurs = set(p for t in tableau for p in t['predecesseurs'])
    taches_sans_successeurs = [t['numero_tache'] for t in tableau if t['numero_tache'] not in tous_predecesseurs]

    # Ajouter alpha
    alpha = {
        'numero_tache': 0,  # Par convention, alpha est souvent la tâche 0
        'duree': 0,         # Alpha n'a pas de durée
        'predecesseurs': [] # Alpha n'a pas de prédécesseurs
    }
    tableau.insert(0, alpha)

    # Ajouter omega
    omega = {
        'numero_tache': max(t['numero_tache'] for t in tableau) + 1,  # Omega est la tâche avec le numéro le plus élevé + 1
        'duree': 0,                                                   # Omega n'a pas de durée
        'predecesseurs': taches_sans_successeurs                      # Omega a pour prédécesseurs les tâches sans successeurs
    }
    tableau.append(omega)

    # Mettre à jour les prédécesseurs des tâches sans prédécesseurs pour inclure alpha
    for t in tableau:
        if t['numero_tache'] in taches_sans_predecesseurs:
            t['predecesseurs'].append(alpha['numero_tache'])

    return tableau


def verification_graphe(tableau):
    """Vérifie que le graphe peut servir pour l'ordonnancement."""
    # Vérification des arcs négatifs
    print("* Vérification des arcs négatifs")
    for tache in tableau:
        if tache['duree'] < 0:
            print("-> Le graphe contient au moins un arc à valeur négative")
            return False
    print("-> Le graphe ne contient pas d'arc à valeur négative\n")

    # Détection de circuit
    print("* Détection de circuit")
    print("* Méthode d’élimination des points d’entrée\n")

    # Créer une copie des contraintes
    contraintes_copie = {t['numero_tache']: list(t['predecesseurs']) for t in tableau}
    sommets = set(t['numero_tache'] for t in tableau)

    while sommets:
        # Trouver les points d'entrée (sommets sans prédécesseurs)
        points_entree = [s for s in sommets if len(contraintes_copie[s]) == 0]
        if not points_entree:
            print("\n-> Il y a un circuit")
            return False

        print("Points d'entrée :", " ".join(map(str, points_entree)))
        print("Suppression des points d'entrée")

        # Supprimer les points d'entrée
        for s in points_entree:
            sommets.remove(s)
            del contraintes_copie[s]

        # Mettre à jour les contraintes
        for s in contraintes_copie:
            contraintes_copie[s] = [p for p in contraintes_copie[s] if p not in points_entree]

        if sommets:
            print("Sommets restant :", " ".join(map(str, sorted(sommets))))
            print("")
        else:
            print("Sommets restant : Aucun")

    print("\n-> Il n’y a pas de circuit")
    print("-> C'est un graphe d'ordonnancement")
    return True

def calculer_rangs(tableau):
    """
    Calcule les rangs de tous les sommets du graphe en utilisant un parcours en largeur.
    Retourne un dictionnaire des rangs et une liste représentant l'ordre topologique.
    """
    # Créer une copie des contraintes
    contraintes_copie = {t['numero_tache']: list(t['predecesseurs']) for t in tableau}
    sommets = set(t['numero_tache'] for t in tableau)
    rang = {}
    rang_courant = 0

    while sommets:
        # Trouver les points d'entrée (sommets sans prédécesseurs)
        points_entree = [s for s in sommets if len(contraintes_copie[s]) == 0]
        # Si aucun point d'entrée n'est trouvé, cela signifie qu'il y a un circuit
        if not points_entree:
            raise ValueError("Le graphe contient un circuit, impossible de calculer les rangs.")

        # Assigner le rang courant aux points d'entrée
        for s in points_entree:
            rang[s] = rang_courant

        # Supprimer les points d'entrée
        for s in points_entree:
            sommets.remove(s)
            del contraintes_copie[s]

        # Mettre à jour les contraintes
        for s in contraintes_copie:
            contraintes_copie[s] = [p for p in contraintes_copie[s] if p not in points_entree]

        rang_courant += 1

    # Tri des tâches par rang croissant
    sommets_tries = sorted(rang.items(), key=lambda item: item[1])

    # Créer une liste des rangs pour chaque tâche
    rangs = [None] * len(tableau)
    for s, r_val in rang.items():
        rangs[s] = r_val
    # Stocker l'ordre topologique
    ordre_topo = [sommet for sommet, _ in sommets_tries]
    return rangs, ordre_topo



def calcul_calendrier(tableau):
    """Calcule les dates au plus tôt et au plus tard en se basant sur les rangs calculés."""
    nb_taches = len(tableau)
    rangs, ordre_topo = calculer_rangs(tableau)
    max_r = max(rangs)

    # Initialiser les listes pour les temps au plus tôt et au plus tard
    temps_tot = [0] * nb_taches
    temps_tar = [float('inf')] * nb_taches

    # Créer une liste des durées des tâches
    durees = [tache['duree'] for tache in tableau]

    # Créer une liste des contraintes (prédécesseurs)
    contraintes = [tache['predecesseurs'] for tache in tableau]

    # Calcul du calendrier au plus tôt
    for r in range(max_r + 1):
        for t in range(nb_taches):
            if rangs[t] == r:
                # Calculer le temps au plus tôt en tenant compte de tous les prédécesseurs
                temps_tot[t] = max([temps_tot[pred] + durees[pred] for pred in contraintes[t]], default=0)

    # La date au plus tard de la tâche finale (oméga) est égale à sa date au plus tôt
    temps_tar[-1] = temps_tot[-1]

    # Calcul du calendrier au plus tard (en ordre inverse)
    for r in range(max_r, -1, -1):
        for t in range(nb_taches):
            if rangs[t] == r:
                for succ in range(nb_taches):
                    if t in contraintes[succ]:
                        temps_tar[t] = min(temps_tar[t], temps_tar[succ] - durees[t])

    return temps_tot, temps_tar


def afficher_resultats(tableau, temps_tot, temps_tar, rangs, ordre_topo):
    # Créer une liste des durées des tâches
    durees = [tache['duree'] for tache in tableau]

    # Créer une liste des contraintes (prédécesseurs)
    contraintes = [tache['predecesseurs'] for tache in tableau]

    # Calculer les marges totales
    marge_totale = [temps_tar[t] - temps_tot[t] for t in range(len(tableau))]

    # Préparer les données pour l'affichage
    resultats = []
    for t in ordre_topo:
        pred_assoc = ""
        if contraintes[t]:
            finish_times = [temps_tot[p] + durees[p] for p in contraintes[t]]
            max_finish = max(finish_times)
            best_preds = [str(p) for p, finish in zip(contraintes[t], finish_times) if finish == max_finish]
            pred_assoc = "(" + ", ".join(best_preds) + ")"

        succ_assoc = ""
        succs = [s for s in range(len(tableau)) if t in contraintes[s]]
        if succs:
            time_tar = [temps_tar[s] - durees[t] for s in succs]
            min_time_tar = min(time_tar)
            best_succs = [str(s) for s, time in zip(succs, time_tar) if time == min_time_tar]
            succ_assoc = "(" + ", ".join(best_succs) + ")"

        resultats.append([
            rangs[t],
            t,
            f"{temps_tot[t]}{pred_assoc}",
            f"{temps_tar[t]}{succ_assoc}",
            marge_totale[t]
        ])
    # Afficher les résultats avec tabulate
    headers = ["Rang", "Sommet", "Date au + tôt", "Date au + tard", "Marge totale"]
    print(tabulate(resultats, headers=headers, tablefmt="grid"))
    return marge_totale


def chemin_critique(tableau, temps_tot, marge_totale):
    final_node = len(tableau) - 1
    project_duration = temps_tot[final_node]
    durees = [tache['duree'] for tache in tableau]
    memo = {}

    # Créer une liste des contraintes (prédécesseurs)
    contraintes = [tache['predecesseurs'] for tache in tableau]

    def dfs(node):
        # Si on atteint le nœud final, retourner un chemin contenant uniquement ce nœud.
        if node == final_node:
            return [[final_node]]
        if node in memo:
            return memo[node]
        paths = []
        # Récupérer les successeurs de 'node' en se basant sur les contraintes
        # On ne considère que les successeurs qui :
        # • Ont une marge totale de 0,
        # • Respectent la condition critique : temps_tot[node] + duree[node] == temps_tot[succ]
        successeurs = []
        for succ in range(len(tableau)):
            if node in contraintes[succ]:
                if marge_totale[succ] == 0 and (
                        temps_tot[node] + durees[node] == temps_tot[succ]):
                    successeurs.append(succ)
        # Traiter les successeurs dans l'ordre croissant (ordre alphabétique)
        successeurs.sort()
        for s in successeurs:
            for sub_path in dfs(s):
                paths.append([node] + sub_path)
        memo[node] = paths
        return paths

    # Lancer la recherche depuis le nœud de départ (α = 0)
    all_paths = dfs(0)
    # Filtrer pour ne garder que les chemins dont la durée totale est exactement celle du projet.
    critical_paths = []
    for path in all_paths:
        # Calcul de la somme des durées sur le chemin
        path_duration = sum(durees[node] for node in path)
        if path_duration == project_duration:
            critical_paths.append(path)
    # Formatage de l'affichage : un chemin par ligne avec les nœuds séparés par " -> "
    formatted_paths = ["• " + " -> ".join(map(str, path)) for path in critical_paths]
    return "\n".join(formatted_paths)

