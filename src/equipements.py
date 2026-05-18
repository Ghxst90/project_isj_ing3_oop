from abc import ABC, abstractmethod


class Equipement(ABC):
    """Représente un équipement réseau générique (classe abstraite)."""

    def __init__(self, nom, marque, adresse_ip):
        self.__nom        = nom
        self.__marque     = marque
        self.__adresse_ip = adresse_ip
        self.__statut     = "actif"


    def get_nom(self):
        return self.__nom

    def get_marque(self):
        return self.__marque

    def get_adresse_ip(self):
        return self.__adresse_ip

    def get_statut(self):
        return self.__statut


    def set_adresse_ip(self, nouvelle_ip):
        self.__adresse_ip = nouvelle_ip


    def activer(self):
        """Active l'équipement."""
        self.__statut = "actif"
        print(f"{self.__nom} est maintenant ACTIF.")

    def desactiver(self):
        """Désactive l'équipement."""
        self.__statut = "inactif"
        print(f"{self.__nom} est maintenant INACTIF.")

    def est_actif(self):
        """Retourne True si l'équipement est actif."""
        return self.__statut == "actif"

    @abstractmethod
    def afficher_info(self):
        """Affiche les infos de l'équipement (à redéfinir dans chaque sous-classe)."""
        pass

    def __str__(self):
        return f"{self.__nom} | {self.__adresse_ip} | {self.__statut}"


class Routeur(Equipement):
    """Routeur réseau. Gère une table de routage."""

    def __init__(self, nom, marque, adresse_ip):
        super().__init__(nom, marque, adresse_ip)
        self.__table_routage = {} 

    def get_table_routage(self):
        return self.__table_routage

    def ajouter_route(self, destination, prochain_saut):
        """Ajoute une route dans la table de routage."""
        self.__table_routage[destination] = prochain_saut
        print(f"[ROUTEUR] Route ajoutée : {destination} -> {prochain_saut}")

    def supprimer_route(self, destination):
        """Supprime une route de la table de routage."""
        if destination in self.__table_routage:
            del self.__table_routage[destination]
            print(f"[ROUTEUR] Route supprimée : {destination}")
        else:
            print(f"[ROUTEUR] Route introuvable : {destination}")

    def afficher_info(self):
        print(f"\n--- ROUTEUR ---")
        print(f"  Nom       : {self.get_nom()}")
        print(f"  Marque    : {self.get_marque()}")
        print(f"  IP        : {self.get_adresse_ip()}")
        print(f"  Statut    : {self.get_statut()}")
        print(f"  Routage   : {self.__table_routage if self.__table_routage else '(vide)'}")



class Switch(Equipement):
    """Switch réseau. Gère une liste de VLANs."""

    def __init__(self, nom, marque, adresse_ip):
        super().__init__(nom, marque, adresse_ip)
        self.__vlans = []

    def get_vlans(self):
        return self.__vlans

    def ajouter_vlan(self, vlan_id):
        """Ajoute un VLAN."""
        if vlan_id not in self.__vlans:
            self.__vlans.append(vlan_id)
            print(f"[SWITCH] VLAN {vlan_id} ajouté.")
        else:
            print(f"[SWITCH] VLAN {vlan_id} déjà présent.")

    def supprimer_vlan(self, vlan_id):
        """Supprime un VLAN."""
        if vlan_id in self.__vlans:
            self.__vlans.remove(vlan_id)
            print(f"[SWITCH] VLAN {vlan_id} supprimé.")
        else:
            print(f"[SWITCH] VLAN {vlan_id} introuvable.")

    def afficher_info(self):
        print(f"\n--- SWITCH ---")
        print(f"  Nom       : {self.get_nom()}")
        print(f"  Marque    : {self.get_marque()}")
        print(f"  IP        : {self.get_adresse_ip()}")
        print(f"  Statut    : {self.get_statut()}")
        print(f"  VLANs     : {self.__vlans if self.__vlans else '(aucun)'}")


class Serveur(Equipement):
    """Serveur réseau. Expose une liste de services."""

    def __init__(self, nom, marque, adresse_ip):
        super().__init__(nom, marque, adresse_ip)
        self.__services = []

    def get_services(self):
        return self.__services

    def ajouter_service(self, service):
        """Ajoute un service exposé par le serveur."""
        if service not in self.__services:
            self.__services.append(service)
            print(f"[SERVEUR] Service '{service}' ajouté.")
        else:
            print(f"[SERVEUR] Service '{service}' déjà enregistré.")

    def afficher_info(self):
        print(f"\n--- SERVEUR ---")
        print(f"  Nom       : {self.get_nom()}")
        print(f"  Marque    : {self.get_marque()}")
        print(f"  IP        : {self.get_adresse_ip()}")
        print(f"  Statut    : {self.get_statut()}")
        print(f"  Services  : {self.__services if self.__services else '(aucun)'}")



class Firewall(Equipement):
    """
    Firewall réseau.
    Stocke les identifiants de configuration (login/mot de passe).
    La logique d'authentification, de filtrage et le journal
    sont entièrement gérés dans securite.py (Membre 3).
    """

    def __init__(self, nom, marque, adresse_ip, login, mot_de_passe):
        super().__init__(nom, marque, adresse_ip)
        self.__login        = login
        self.__mot_de_passe = mot_de_passe

    def get_login(self):
        return self.__login

    def get_mot_de_passe(self):
        return self.__mot_de_passe

    def afficher_info(self):
        print(f"\n--- FIREWALL ---")
        print(f"  Nom       : {self.get_nom()}")
        print(f"  Marque    : {self.get_marque()}")
        print(f"  IP        : {self.get_adresse_ip()}")
        print(f"  Statut    : {self.get_statut()}")
        print(f"  Login     : {self.__login}")


class PointAccesWifi(Equipement):
    """Point d'accès Wi-Fi. Possède un SSID et un canal."""

    def __init__(self, nom, marque, adresse_ip, ssid, canal):
        super().__init__(nom, marque, adresse_ip)
        self.__ssid  = ssid
        self.__canal = canal

    def get_ssid(self):
        return self.__ssid

    def get_canal(self):
        return self.__canal

    def afficher_info(self):
        print(f"\n--- POINT ACCÈS WIFI ---")
        print(f"  Nom       : {self.get_nom()}")
        print(f"  Marque    : {self.get_marque()}")
        print(f"  IP        : {self.get_adresse_ip()}")
        print(f"  Statut    : {self.get_statut()}")
        print(f"  SSID      : {self.__ssid}")
        print(f"  Canal     : {self.__canal}")



class Terminal(Equipement):
    """Terminal client (PC, smartphone, etc.)."""

    def __init__(self, nom, marque, adresse_ip):
        super().__init__(nom, marque, adresse_ip)

    def afficher_info(self):
        print(f"\n--- TERMINAL ---")
        print(f"  Nom       : {self.get_nom()}")
        print(f"  Marque    : {self.get_marque()}")
        print(f"  IP        : {self.get_adresse_ip()}")
        print(f"  Statut    : {self.get_statut()}")