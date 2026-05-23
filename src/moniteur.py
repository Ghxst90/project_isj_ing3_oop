import datetime
from collections import defaultdict


class Moniteur:
    """
    Moniteur réseau pour SIMNet.
    Collecte les statistiques par équipement et par lien,
    conserve l'historique des 10 derniers paquets et
    génère un rapport texte exportable.
    """

    def __init__(self, topologie, simulateur):
        self.__topologie         = topologie
        self.__simulateur        = simulateur
        self.__stats_eq          = defaultdict(lambda: {'transmis': 0, 'perdus': 0})
        self.__utilisation_liens = defaultdict(float)
        self.__debut             = datetime.datetime.now()

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

    def get_stats_equipement(self, nom):
        """Retourne {"transmis": n, "perdus": n} pour un équipement."""
        return dict(self.__stats_eq[nom])

    def get_utilisation_lien(self, nom1, nom2):
        """Retourne les octets cumulés sur un lien."""
        return self.__utilisation_liens[self.__cle_lien(nom1, nom2)]

    def get_equipements_actifs(self):
        """Liste des équipements actuellement actifs."""
        return [
            nom for nom, eq in self.__topologie.get_equipements().items()
            if eq.est_actif()
        ]

    def get_equipements_inactifs(self):
        """Liste des équipements actuellement inactifs."""
        return [
            nom for nom, eq in self.__topologie.get_equipements().items()
            if not eq.est_actif()
        ]

    def get_historique(self):
        """Retourne les 10 derniers paquets du simulateur."""
        return self.__simulateur.get_historique()[-10:]

    def afficher_tableau_bord(self):
        """Affiche un tableau de bord récapitulatif dans la console."""
        print('\n' + '=' * 55)
        print('        TABLEAU DE BORD — SIMNet MONITEUR')
        print('=' * 55)

        print('\n--- Équipements actifs ---')
        actifs = self.get_equipements_actifs()
        if actifs:
            for nom in actifs:
                s = self.__stats_eq[nom]
                print(f"  [OK] {nom:20s}  transmis={s['transmis']}  perdus={s['perdus']}")
        else:
            print('  (aucun)')

        print('\n--- Équipements inactifs ---')
        inactifs = self.get_equipements_inactifs()
        if inactifs:
            for nom in inactifs:
                print(f'  [X] {nom}')
        else:
            print('  (aucun)')

        print('\n--- Utilisation des liens ---')
        if self.__utilisation_liens:
            for lien_cle, octets in self.__utilisation_liens.items():
                print(f'  {lien_cle:35s}  {octets:>10.0f} octets')
        else:
            print('  (aucun trafic enregistré)')

        print('\n--- Historique des 10 derniers paquets ---')
        historique = self.get_historique()
        if historique:
            for statut, paquet in historique:
                print(f'  [{statut:5s}] {paquet}')
        else:
            print('  (aucun paquet)')

        print('\n' + '=' * 55 + '\n')