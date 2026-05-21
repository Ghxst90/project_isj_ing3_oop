import heapq
from topologie import Topologie, Lien


class Paquet:
    """Représente un paquet de données circulant dans le réseau."""

    def __init__(self, source, destination, protocole, taille, priorite):
        self.__source      = source
        self.__destination = destination
        self.__protocole   = protocole
        self.__taille      = taille
        self.__priorite    = priorite

    def get_source(self):
        return self.__source

    def get_destination(self):
        return self.__destination

    def get_protocole(self):
        return self.__protocole

    def get_taille(self):
        return self.__taille

    def get_priorite(self):
        return self.__priorite

    def __str__(self):
        return (f"Paquet [{self.__protocole}] "
                f"{self.__source} -> {self.__destination} | "
                f"{self.__taille} octets | priorité {self.__priorite}")


class Simulateur:
    """Moteur de simulation : trouve les chemins et fait circuler les paquets."""

    def __init__(self, topologie):
        self.__topologie       = topologie
        self.__paquets_envoyes = 0
        self.__paquets_perdus  = 0
        self.__debit_cumule    = 0
        self.__temps_transit   = 0
        self.__historique      = []

    def __construire_graphe(self):
        """Construit un graphe à partir des liens de la topologie."""
        graphe = {}
        for eq in self.__topologie.get_equipements():
            graphe[eq] = []
        for lien in self.__topologie.get_liens():
            nom1  = lien.get_equipement1().get_nom()
            nom2  = lien.get_equipement2().get_nom()
            poids = lien.get_latence()
            graphe[nom1].append((poids, nom2))
            graphe[nom2].append((poids, nom1))
        return graphe

    def __dijkstra(self, source, destination):
        """Trouve le chemin le plus court entre source et destination."""
        graphe      = self.__construire_graphe()
        distances   = {noeud: float('inf') for noeud in graphe}
        distances[source] = 0
        predecesseurs = {noeud: None for noeud in graphe}
        file = [(0, source)]

        while file:
            dist_actuelle, noeud_actuel = heapq.heappop(file)
            if noeud_actuel == destination:
                break
            for poids, voisin in graphe[noeud_actuel]:
                nouvelle_dist = dist_actuelle + poids
                if nouvelle_dist < distances[voisin]:
                    distances[voisin]     = nouvelle_dist
                    predecesseurs[voisin] = noeud_actuel
                    heapq.heappush(file, (nouvelle_dist, voisin))

        chemin = []
        noeud  = destination
        while noeud is not None:
            chemin.insert(0, noeud)
            noeud = predecesseurs[noeud]

        if len(chemin) == 0 or chemin[0] != source:
            return None
        return chemin

    def envoyer_paquet(self, paquet, nom_source, nom_destination):
        """Envoie un paquet de nom_source vers nom_destination."""
        print(f"\n[SIMULATEUR] Envoi : {paquet}")
        print(f"[SIMULATEUR] Recherche du chemin : {nom_source} -> {nom_destination}")

        chemin = self.__dijkstra(nom_source, nom_destination)

        if chemin is None:
            print(f"[SIMULATEUR] Destination inatteignable !")
            self.__paquets_perdus += 1
            self.__historique.append(("PERDU", paquet))
            return

        print(f"[SIMULATEUR] Chemin trouvé : {' -> '.join(chemin)}")

        liens       = self.__topologie.get_liens()
        temps_total = 0

        for i in range(len(chemin) - 1):
            nom1, nom2 = chemin[i], chemin[i + 1]
            for lien in liens:
                e1 = lien.get_equipement1().get_nom()
                e2 = lien.get_equipement2().get_nom()
                if {e1, e2} == {nom1, nom2}:
                    temps_total += lien.get_latence()
                    print(f"  saut : {nom1} -> {nom2} "
                          f"({lien.get_latence()} ms, "
                          f"{lien.get_bande_passante()} Mbps)")
                    break

        self.__paquets_envoyes += 1
        self.__debit_cumule    += paquet.get_taille()
        self.__temps_transit   += temps_total
        self.__historique.append(("OK", paquet))

        print(f"[SIMULATEUR] Temps de transit : {temps_total} ms")
        print(f"[SIMULATEUR] Paquet livré avec succès.")

    def get_paquets_envoyes(self):
        return self.__paquets_envoyes

    def get_paquets_perdus(self):
        return self.__paquets_perdus

    def get_debit_cumule(self):
        return self.__debit_cumule

    def get_temps_transit(self):
        return self.__temps_transit

    def get_historique(self):
        return self.__historique

    def afficher_statistiques(self):
        """Affiche les statistiques globales de la simulation."""
        print("\n=== STATISTIQUES DE SIMULATION ===")
        print(f"  Paquets envoyés  : {self.__paquets_envoyes}")
        print(f"  Paquets perdus   : {self.__paquets_perdus}")
        print(f"  Débit cumulé     : {self.__debit_cumule} octets")
        print(f"  Temps de transit : {self.__temps_transit} ms")
        print(f"\n  -- 10 derniers paquets --")
        for statut, paquet in self.__historique[-10:]:
            print(f"  [{statut}] {paquet}")
        print("==================================\n")