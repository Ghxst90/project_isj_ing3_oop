from abc import ABC, abstractmethod

class Equipement(ABC):
    """Représente un équipement réseau générique (classe abstraite)."""

    def __init__(self, nom, marque, adresse_ip):
        self._nom        = nom
        self._marque     = marque
        self._adresse_ip = adresse_ip
        self._statut     = "actif"

    def activer(self):
        """Active l'équipement."""
        self._statut = "actif"
        print(f"{self._nom} est maintenant ACTIF.")

    def desactiver(self):
        """Désactive l'équipement."""
        self._statut = "inactif"
        print(f"{self._nom} est maintenant INACTIF.")

    def est_actif(self):
        """Retourne True si l'équipement est actif."""
        return self._statut == "actif"

    @abstractmethod
    def afficher_info(self):
        """Affiche les infos de l'équipement (à redéfinir dans chaque sous-classe)."""
        pass

    def __str__(self):
        return f"{self._nom} | {self._adresse_ip} | {self._statut}"


class Routeur(Equipement):
    """Routeur réseau. Gère une table de routage."""

    def __init__(self, nom, marque, adresse_ip):
        super().__init__(nom, marque, adresse_ip)
        self._table_routage = {} 

    def ajouter_route(self, destination, prochain_saut):
        """Ajoute une route dans la table de routage."""
        self._table_routage[destination] = prochain_saut
        print(f"[ROUTEUR] Route ajoutée : {destination} -> {prochain_saut}")

    def supprimer_route(self, destination):
        """Supprime une route de la table de routage."""
        if destination in self._table_routage:
            del self._table_routage[destination]
            print(f"[ROUTEUR] Route supprimée : {destination}")
        else:
            print(f"[ROUTEUR] Route introuvable : {destination}")

    def afficher_info(self):
        print(f"\n--- ROUTEUR ---")
        print(f"  Nom       : {self._nom}")
        print(f"  Marque    : {self._marque}")
        print(f"  IP        : {self._adresse_ip}")
        print(f"  Statut    : {self._statut}")
        print(f"  Routage   : {self._table_routage if self._table_routage else '(vide)'}")


class Switch(Equipement):
    """Switch réseau. Gère une liste de VLANs."""

    def __init__(self, nom, marque, adresse_ip):
        super().__init__(nom, marque, adresse_ip)
        self._vlans = []

    def ajouter_vlan(self, vlan_id):
        """Ajoute un VLAN."""
        if vlan_id not in self._vlans:
            self._vlans.append(vlan_id)
            print(f"[SWITCH] VLAN {vlan_id} ajouté.")
        else:
            print(f"[SWITCH] VLAN {vlan_id} déjà présent.")

    def supprimer_vlan(self, vlan_id):
        """Supprime un VLAN."""
        if vlan_id in self._vlans:
            self._vlans.remove(vlan_id)
            print(f"[SWITCH] VLAN {vlan_id} supprimé.")
        else:
            print(f"[SWITCH] VLAN {vlan_id} introuvable.")

    def afficher_info(self):
        print(f"\n--- SWITCH ---")
        print(f"  Nom       : {self._nom}")
        print(f"  Marque    : {self._marque}")
        print(f"  IP        : {self._adresse_ip}")
        print(f"  Statut    : {self._statut}")
        print(f"  VLANs     : {self._vlans if self._vlans else '(aucun)'}")


class Serveur(Equipement):
    """Serveur réseau. Expose une liste de services."""

    def __init__(self, nom, marque, adresse_ip):
        super().__init__(nom, marque, adresse_ip)
        self._services = []

    def ajouter_service(self, service):
        """Ajoute un service exposé par le serveur."""
        if service not in self._services:
            self._services.append(service)
            print(f"[SERVEUR] Service '{service}' ajouté.")
        else:
            print(f"[SERVEUR] Service '{service}' déjà enregistré.")

    def afficher_info(self):
        print(f"\n--- SERVEUR ---")
        print(f"  Nom       : {self._nom}")
        print(f"  Marque    : {self._marque}")
        print(f"  IP        : {self._adresse_ip}")
        print(f"  Statut    : {self._statut}")
        print(f"  Services  : {self._services if self._services else '(aucun)'}")


class Firewall(Equipement):
    """
    Firewall réseau.
    Définit l'équipement de base avec login/mot de passe.
    La logique de filtrage et le journal sont gérés dans securite.py.
    """

    def __init__(self, nom, marque, adresse_ip, login, mot_de_passe):
        super().__init__(nom, marque, adresse_ip)
        self._login        = login
        self._mot_de_passe = mot_de_passe

    def afficher_info(self):
        print(f"\n--- FIREWALL ---")
        print(f"  Nom       : {self._nom}")
        print(f"  Marque    : {self._marque}")
        print(f"  IP        : {self._adresse_ip}")
        print(f"  Statut    : {self._statut}")
        print(f"  Login     : {self._login}")


class PointAccesWifi(Equipement):
    """Point d'accès Wi-Fi. Possède un SSID et un canal."""

    def __init__(self, nom, marque, adresse_ip, ssid, canal):
        super().__init__(nom, marque, adresse_ip)
        self._ssid  = ssid
        self._canal = canal

    def afficher_info(self):
        print(f"\n--- POINT ACCÈS WIFI ---")
        print(f"  Nom       : {self._nom}")
        print(f"  Marque    : {self._marque}")
        print(f"  IP        : {self._adresse_ip}")
        print(f"  Statut    : {self._statut}")
        print(f"  SSID      : {self._ssid}")
        print(f"  Canal     : {self._canal}")


class Terminal(Equipement):
    """Terminal client (PC, smartphone, etc.)."""

    def __init__(self, nom, marque, adresse_ip):
        super().__init__(nom, marque, adresse_ip)

    def afficher_info(self):
        print(f"\n--- TERMINAL ---")
        print(f"  Nom       : {self._nom}")
        print(f"  Marque    : {self._marque}")
        print(f"  IP        : {self._adresse_ip}")
        print(f"  Statut    : {self._statut}")