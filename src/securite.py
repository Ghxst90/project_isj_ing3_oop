import ipaddress
import datetime

class RegleFiltrage:
    """
    Représente une règle de filtrage réseau.
    Critères optionnels : ip_source, protocole, port, plage_reseau.
    Algorithme : AND logique — tous les critères renseignés doivent correspondre.
    """

def __init__(self, action, ip_source=None, protocole=None,
                port=None, plage_reseau=None):
        if action not in ("AUTORISER", "BLOQUER"):
            raise ValueError("action doit etre 'AUTORISER' ou 'BLOQUER'")
        self.__action = action
        self.__ip_source = ip_source
        self.__protocole = protocole
        self.__port = port
        self.__plage_reseau = plage_reseau
 
def get_action(self):
        return self.__action
 
def correspond(self, paquet):

 
        # Critere 1 : IP source exacte
        if self.__ip_source is not None:
            if paquet.get_source() != self.__ip_source:
                return False
 
        # Critere 2 : Protocole (TCP / UDP / ICMP)
        if self.__protocole is not None:
            if paquet.get_protocole().upper() != self.__protocole.upper():
                return False
 
        # Critere 3 : Port destination
        if self.__port is not None:
            if paquet.get_destination() != str(self.__port):
                return False
 
        # Critere 4 : Plage reseau CIDR (utilise le module ipaddress de la stdlib)
        if self.__plage_reseau is not None:
            try:
                reseau = ipaddress.ip_network(self.__plage_reseau, strict=False)
                ip_src = ipaddress.ip_address(paquet.get_source())
                if ip_src not in reseau:
                    return False
            except ValueError:
                return False # IP ou CIDR invalide => regle ignoree
 
        return True # Tous les criteres satisfaits => regle s'applique
 
def __str__(self):
        criteres = []
        if self.__ip_source: criteres.append(f"ip={self.__ip_source}")
        if self.__protocole: criteres.append(f"proto={self.__protocole}")
        if self.__port: criteres.append(f"port={self.__port}")
        if self.__plage_reseau: criteres.append(f"plage={self.__plage_reseau}")
        detail = ', '.join(criteres) if criteres else 'tout le trafic'
        return f"{self.__action} [{detail}]"
    
    
class JournalSecurite:
 
    def __init__(self):
        self.__entrees = [] # list of tuples
 
    def enregistrer(self, action, paquet, raison=""):
        """Ajoute une entree avec horodatage automatique."""
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__entrees.append((ts, action, str(paquet), raison))
 
    def get_entrees(self):
        """Retourne une copie defensive de la liste des entrees."""
        return list(self.__entrees)
 
    def afficher(self):
        """Affiche le journal complet en console."""
        print("\n=== JOURNAL DU FIREWALL ===")
        if not self.__entrees:
            print(" (journal vide)")
        for ts, action, paquet_str, raison in self.__entrees:
            print(f" [{ts}] {action:<10} | {paquet_str} | {raison}")
        print("===========================\n")
 
    def exporter(self, chemin="rapport_simnet.txt"):
        """Exporte le journal dans un fichier texte (mode ajout)."""
        with open(chemin, "a", encoding="utf-8") as f:
            f.write("\n=== JOURNAL DU FIREWALL ===\n")
            for ts, action, paquet_str, raison in self.__entrees:
                f.write(f"[{ts}] {action:<10} | {paquet_str} | {raison}\n")
            f.write("===========================\n")
        print(f"[JOURNAL] Journal exporte dans '{chemin}'" )
        
        
        
class GestionnaireFirewall:
    
      """
    Orchestre la securite du reseau :
    - Authentification administrateur (login / mot de passe)
    - Gestion des regles de filtrage (ajout, suppression, affichage)
    - Inspection des paquets (algorithme first-match)
    - Journalisation horodatee de chaque decision
    """
 
def __init__(self, firewall):
        self.__firewall = firewall # objet Firewall (equipements.py)
        self.__regles = [] # list[RegleFiltrage]
        self.__journal = JournalSecurite()
        self.__authentifie = False
 
    #  Authentification 
def authentifier(self, login, mdp):
        """Verifie login/mdp contre les credentials du Firewall. Retourne bool."""
        if (login == self.__firewall.get_login() and
                mdp == self.__firewall.get_mot_de_passe()):
            self.__authentifie = True
            print(f"[FIREWALL] Authentification reussie pour '{login}'.")
            return True
        print("[FIREWALL] Echec : identifiants incorrects.")
        return False
 
def deconnecter(self):
        """Ferme la session administrateur."""
        self.__authentifie = False
        print("[FIREWALL] Session administrateur fermee.")
 
    #  Gestion des regles 
def ajouter_regle(self, regle):
        """Ajoute une RegleFiltrage. Necessite une session authentifiee."""
        if not self.__authentifie:
            print("[FIREWALL] Acces refuse. Authentifiez-vous d'abord.")
            return
        self.__regles.append(regle)
        print(f"[FIREWALL] Regle ajoutee : {regle}")
 
def supprimer_regle(self, index):
        """Supprime la regle a l'index donne."""
        if not self.__authentifie:
            print("[FIREWALL] Acces refuse.")
            return
        if 0 <= index < len(self.__regles):
            supprimee = self.__regles.pop(index)
            print(f"[FIREWALL] Regle supprimee : {supprimee}")
        else:
            print(f"[FIREWALL] Index invalide ({index}).")
 
def afficher_regles(self):
        """Affiche toutes les regles actives numerotees."""
        print(f"\n-- Regles du Firewall '{self.__firewall.get_nom()}' --")
        if not self.__regles:
            print(" (aucune regle definie)")
        for i, r in enumerate(self.__regles):
            print(f" [{i}] {r}")
        print()
 
    #  Inspection des paquets (first-match) 
def inspecter_paquet(self, paquet):
        """
        Parcourt les regles dans l'ordre d'insertion.
        La premiere regle dont correspond(paquet)==True s'applique.
        Si aucune regle ne correspond, la politique par defaut est AUTORISER.
        Retourne : 'AUTORISER' ou 'BLOQUER'
        """
        for regle in self.__regles:
            if regle.correspond(paquet):
                action = regle.get_action()
                self.__journal.enregistrer(
                    action, paquet, raison=f"Regle: {regle}")
                print(f"[FIREWALL] {self.__firewall.get_nom()} "
                      f"=> {action} | {paquet}")
                return action
 
        # Aucune regle ne correspond => politique par defaut : AUTORISER
        self.__journal.enregistrer(
            "AUTORISER", paquet, raison="Aucune regle applicable (defaut)")
        print(f"[FIREWALL] {self.__firewall.get_nom()} "
              f"=> AUTORISER (defaut) | {paquet}")
        return "AUTORISER"
 
    #  Journal
def afficher_journal(self):
        """Affiche le journal complet du firewall."""
        self.__journal.afficher()
 
def exporter_journal(self, chemin="rapport_simnet.txt"):
        """Exporte le journal dans un fichier texte."""
        self.__journal.exporter(chemin)
 
def get_journal(self):
        """Retourne l'objet JournalSecurite (pour le Moniteur, Membre 4)."""
        return self.__journal
 
def get_firewall(self):
        """Retourne l'objet Firewall associe."""
        return self.__firewall        
    
    
    


"""
securite.py — Module 3 : Securite et Filtrage
SIMNet — Simulateur de Reseau Intelligent en Python
Institut Saint Jean — INGENIEUR 3 SRT — 2025/2026
"""
import datetime
import ipaddress
from equipements import Firewall
 
 
# 
class RegleFiltrage:
    """
    Modele une regle de filtrage reseau.
    Combine une action (AUTORISER/BLOQUER) avec des criteres optionnels.
    Algorithme : AND logique sur tous les criteres non-None.
    """
 
    def __init__(self, action, ip_source=None, protocole=None,
                 port=None, plage_reseau=None):
        if action not in ("AUTORISER", "BLOQUER"):
            raise ValueError("action doit etre 'AUTORISER' ou 'BLOQUER'")
        self.__action = action
        self.__ip_source = ip_source
        self.__protocole = protocole
        self.__port = port
        self.__plage_reseau = plage_reseau
 
    def get_action(self):
        return self.__action
 
    def correspond(self, paquet):
        """True si le paquet satisfait tous les criteres de la regle."""
        if self.__ip_source and paquet.get_source() != self.__ip_source:
            return False
        if self.__protocole and paquet.get_protocole().upper() != self.__protocole.upper():
            return False
        if self.__port and paquet.get_destination() != str(self.__port):
            return False
        if self.__plage_reseau:
            try:
                reseau = ipaddress.ip_network(self.__plage_reseau, strict=False)
                if ipaddress.ip_address(paquet.get_source()) not in reseau:
                    return False
            except ValueError:
                return False
        return True
 
    def __str__(self):
        c = []
        if self.__ip_source: c.append(f"ip={self.__ip_source}")
        if self.__protocole: c.append(f"proto={self.__protocole}")
        if self.__port: c.append(f"port={self.__port}")
        if self.__plage_reseau: c.append(f"plage={self.__plage_reseau}")
        return f"{self.__action} [{', '.join(c) if c else 'tout le trafic'}]"
# 
class JournalSecurite:
    """
    Journal horodate de toutes les decisions du Firewall.
    Chaque entree : (timestamp, action, paquet_str, raison).
    """
 
    def __init__(self):
        self.__entrees = []
 
    def enregistrer(self, action, paquet, raison=""):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__entrees.append((ts, action, str(paquet), raison))
 
    def get_entrees(self):
        return list(self.__entrees)
 
    def afficher(self):
        print("\n=== JOURNAL DU FIREWALL ===")
        if not self.__entrees:
            print(" (journal vide)")
        for ts, action, pstr, raison in self.__entrees:
            print(f" [{ts}] {action:<10} | {pstr} | {raison}")
        print("===========================\n")
 
    def exporter(self, chemin="rapport_simnet.txt"):
        with open(chemin, "a", encoding="utf-8") as f:
            f.write("\n=== JOURNAL DU FIREWALL ===\n")
            for ts, action, pstr, raison in self.__entrees:
                f.write(f"[{ts}] {action:<10} | {pstr} | {raison}\n")
            f.write("===========================\n")
        print(f"[JOURNAL] Exporte dans '{chemin}'")
 
 
# 
class GestionnaireFirewall:
    """
    Orchestre la securite : auth, regles, inspection first-match, journal.
    """
 
    def __init__(self, firewall):
        self.__firewall = firewall
        self.__regles = []
        self.__journal = JournalSecurite()
        self.__authentifie = False
 
    def authentifier(self, login, mdp):
        if (login == self.__firewall.get_login() and
                mdp == self.__firewall.get_mot_de_passe()):
            self.__authentifie = True
            print(f"[FIREWALL] Auth reussie pour '{login}'.")
            return True
        print("[FIREWALL] Echec : identifiants incorrects.")
        return False
 
    def deconnecter(self):
        self.__authentifie = False
        print("[FIREWALL] Session admin fermee.")
 
    def ajouter_regle(self, regle):
        if not self.__authentifie:
            print("[FIREWALL] Acces refuse. Authentifiez-vous.")
            return
        self.__regles.append(regle)
        print(f"[FIREWALL] Regle ajoutee : {regle}")
 
    def supprimer_regle(self, index):
        if not self.__authentifie:
            print("[FIREWALL] Acces refuse.")
            return
        if 0 <= index < len(self.__regles):
            print(f"[FIREWALL] Regle supprimee : {self.__regles.pop(index)}")
        else:
            print(f"[FIREWALL] Index invalide ({index}).")
 
    def afficher_regles(self):
        print(f"\n-- Regles Firewall '{self.__firewall.get_nom()}' --")
        if not self.__regles:
            print(" (aucune regle)")
        for i, r in enumerate(self.__regles):
            print(f" [{i}] {r}")
        print()
 
    def inspecter_paquet(self, paquet):
        """First-match : retourne 'AUTORISER' ou 'BLOQUER'."""
        for regle in self.__regles:
            if regle.correspond(paquet):
                action = regle.get_action()
                self.__journal.enregistrer(action, paquet, f"Regle: {regle}")
                print(f"[FIREWALL] {self.__firewall.get_nom()} => {action} | {paquet}")
                return action
        self.__journal.enregistrer("AUTORISER", paquet, "Defaut (aucune regle)")
        print(f"[FIREWALL] {self.__firewall.get_nom()} => AUTORISER (defaut) | {paquet}")
        return "AUTORISER"
 
    def afficher_journal(self):
        self.__journal.afficher()
 
    def exporter_journal(self, chemin="rapport_simnet.txt"):
        self.__journal.exporter(chemin)
    def get_journal(self):
        return self.__journal
    def get_firewall(self):
        return self.__firewall