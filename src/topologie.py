from equipements import Equipement


class Lien:
    """Représente un lien (câble) entre deux équipements réseau."""

    def __init__(self, equipement1, equipement2, bande_passante, latence):
        self.__equipement1    = equipement1
        self.__equipement2    = equipement2
        self.__bande_passante = bande_passante  # en Mbps
        self.__latence        = latence          # en ms

    def get_equipement1(self):
        return self.__equipement1

    def get_equipement2(self):
        return self.__equipement2

    def get_bande_passante(self):
        return self.__bande_passante

    def get_latence(self):
        return self.__latence

    def __str__(self):
        return (f"{self.__equipement1.get_nom()} <--> "
                f"{self.__equipement2.get_nom()} | "
                f"{self.__bande_passante} Mbps | {self.__latence} ms")

class Topologie:
    """Représente le plan complet du réseau : équipements et liens."""

    def __init__(self):
        self.__equipements = {}  # dictionnaire : nom -> objet Equipement
        self.__liens       = []  # liste de tous les liens

    def ajouter_equipement(self, equipement):
        """Ajoute un équipement au réseau."""
        nom = equipement.get_nom()
        if nom not in self.__equipements:
            self.__equipements[nom] = equipement
            print(f"[TOPOLOGIE] Équipement '{nom}' ajouté.")
        else:
            print(f"[TOPOLOGIE] '{nom}' existe déjà.")

    def supprimer_equipement(self, nom):
        """Supprime un équipement du réseau."""
        if nom in self.__equipements:
            del self.__equipements[nom]
            self.__liens = [l for l in self.__liens
                           if l.get_equipement1().get_nom() != nom
                           and l.get_equipement2().get_nom() != nom]
            print(f"[TOPOLOGIE] Équipement '{nom}' supprimé.")
        else:
            print(f"[TOPOLOGIE] '{nom}' introuvable.")

    def ajouter_lien(self, nom1, nom2, bande_passante, latence):
        """Crée un lien entre deux équipements existants."""
        if nom1 in self.__equipements and nom2 in self.__equipements:
            lien = Lien(self.__equipements[nom1],
                        self.__equipements[nom2],
                        bande_passante, latence)
            self.__liens.append(lien)
            print(f"[TOPOLOGIE] Lien ajouté : {lien}")
        else:
            print(f"[TOPOLOGIE] Équipement(s) introuvable(s).")

    def supprimer_lien(self, nom1, nom2):
        """Supprime le lien entre deux équipements."""
        avant = len(self.__liens)
        self.__liens = [l for l in self.__liens
                       if not ({l.get_equipement1().get_nom(),
                                l.get_equipement2().get_nom()} == {nom1, nom2})]
        if len(self.__liens) < avant:
            print(f"[TOPOLOGIE] Lien {nom1} <--> {nom2} supprimé.")
        else:
            print(f"[TOPOLOGIE] Lien introuvable.")

    def get_equipements(self):
        return self.__equipements

    def get_liens(self):
        return self.__liens

    def afficher(self):
        """Affiche tous les équipements et liens du réseau."""
        print("\n=== TOPOLOGIE DU RÉSEAU ===")
        print(f"\n-- Équipements ({len(self.__equipements)}) --")
        for eq in self.__equipements.values():
            print(f"  {eq}")
        print(f"\n-- Liens ({len(self.__liens)}) --")
        for lien in self.__liens:
            print(f"  {lien}")
        print("===========================\n")

