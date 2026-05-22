# moniteur.py — structure initiale
import datetime
import os
from collections import defaultdict
 
 
class Moniteur:
    """
    Moniteur réseau pour SIMNet.
    Collecte les statistiques par équipement et par lien,
    conserve l'historique des 10 derniers paquets et
    génère un rapport texte exportable.
    """
 
    def __init__(self, topologie, simulateur):
        """
        :param topologie: instance de Topologie
        :param simulateur: instance de Simulateur
        """
        self.__topologie  = topologie
        self.__simulateur = simulateur
        self.__stats_eq   = defaultdict(lambda: {'transmis': 0, 'perdus': 0})
        self.__utilisation_liens = defaultdict(float)
        self.__debut = datetime.datetime.now()
 

     def enregistrer_paquet(self, statut, paquet, chemin=None):
        """
        :param statut: 'OK' ou 'PERDU'
        :param paquet: instance de Paquet
        :param chemin: liste ordonnée de noms d'équipements (ou None)
        """
        if statut == 'OK':
            if chemin:
                for nom in chemin:
                    self.__stats_eq[nom]['transmis'] += 1
                for i in range(len(chemin) - 1):
                    cle = self.__cle_lien(chemin[i], chemin[i + 1])
                    self.__utilisation_liens[cle] += paquet.get_taille()
        else:
            self.__stats_eq[paquet.get_source()]['perdus'] += 1
 
    def __cle_lien(self, nom1, nom2):
        """Clé canonique pour un lien (ordre alphabétique)."""
        a, b = sorted([nom1, nom2])
        return f'{a}<->{b}'

