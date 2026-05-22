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
 
    # TODO : ajouter les méthodes dans les tâches suivantes
