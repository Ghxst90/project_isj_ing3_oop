from equipements import Routeur, Switch, Serveur, Firewall, PointAccesWifi, Terminal
from topologie   import Topologie, Lien
from paquets     import Paquet, Simulateur



def saisir_int(message, mini=None, maxi=None):
    """Demande un entier à l'utilisateur avec validation."""
    while True:
        try:
            valeur = int(input(message))
            if mini is not None and valeur < mini:
                print(f"  Valeur minimale : {mini}")
                continue
            if maxi is not None and valeur > maxi:
                print(f"  Valeur maximale : {maxi}")
                continue
            return valeur
        except ValueError:
            print("  Veuillez entrer un nombre entier.")


def saisir_non_vide(message):
    """Demande une chaîne non vide à l'utilisateur."""
    while True:
        valeur = input(message).strip()
        if valeur:
            return valeur
        print("  Ce champ ne peut pas être vide.")


def menu_ajouter_equipement(topologie):
    """Ajoute un équipement à la topologie."""
    print("\n  Types disponibles :")
    print("  1. Routeur")
    print("  2. Switch")
    print("  3. Serveur")
    print("  4. Firewall")
    print("  5. Point d'accès Wi-Fi")
    print("  6. Terminal")

    choix = saisir_int("  Votre choix : ", 1, 6)
    nom    = saisir_non_vide("  Nom       : ")
    marque = saisir_non_vide("  Marque    : ")
    ip     = saisir_non_vide("  Adresse IP: ")

    try:
        if choix == 1:
            eq = Routeur(nom, marque, ip)
        elif choix == 2:
            eq = Switch(nom, marque, ip)
        elif choix == 3:
            eq = Serveur(nom, marque, ip)
        elif choix == 4:
            login = saisir_non_vide("  Login     : ")
            mdp   = saisir_non_vide("  Mot de passe : ")
            eq = Firewall(nom, marque, ip, login, mdp)
        elif choix == 5:
            ssid  = saisir_non_vide("  SSID  : ")
            canal = saisir_int("  Canal (1-13) : ", 1, 13)
            eq = PointAccesWifi(nom, marque, ip, ssid, canal)
        elif choix == 6:
            eq = Terminal(nom, marque, ip)

        topologie.ajouter_equipement(eq)

    except ValueError as e:
        print(f"  Erreur : {e}")


def menu_supprimer_equipement(topologie):
    """Supprime un équipement de la topologie."""
    nom = saisir_non_vide("  Nom de l'équipement à supprimer : ")
    topologie.supprimer_equipement(nom)




def menu_ajouter_lien(topologie):
    """Ajoute un lien entre deux équipements."""
    print("\n  Équipements disponibles :")
    for nom in topologie.get_equipements():
        print(f"    - {nom}")

    nom1 = saisir_non_vide("  Équipement 1 : ")
    nom2 = saisir_non_vide("  Équipement 2 : ")
    bp   = saisir_int("  Bande passante (Mbps) : ", 1)
    lat  = saisir_int("  Latence (ms)          : ", 1)
    topologie.ajouter_lien(nom1, nom2, bp, lat)


def menu_supprimer_lien(topologie):
    """Supprime un lien entre deux équipements."""
    nom1 = saisir_non_vide("  Équipement 1 : ")
    nom2 = saisir_non_vide("  Équipement 2 : ")
    topologie.supprimer_lien(nom1, nom2)


def menu_afficher_topologie(topologie):
    """Affiche la topologie complète."""
    topologie.afficher()


def menu_envoyer_paquet(simulateur):
    """Envoie un paquet à travers le réseau."""
    print("\n  Protocoles disponibles : TCP | UDP | ICMP")
    source      = saisir_non_vide("  IP source      : ")
    destination = saisir_non_vide("  IP destination : ")
    protocole   = saisir_non_vide("  Protocole      : ").upper()

    if protocole not in ["TCP", "UDP", "ICMP"]:
        print("  Protocole invalide. Utilisez TCP, UDP ou ICMP.")
        return

    taille   = saisir_int("  Taille (octets)  : ", 1)
    priorite = saisir_int("  Priorité (1-5)   : ", 1, 5)

    nom_source = saisir_non_vide("  Nom équipement source      : ")
    nom_dest   = saisir_non_vide("  Nom équipement destination : ")

    paquet = Paquet(source, destination, protocole, taille, priorite)
    simulateur.envoyer_paquet(paquet, nom_source, nom_dest)


def menu_statistiques(simulateur):
    """Affiche les statistiques de simulation."""
    simulateur.afficher_statistiques()



def afficher_menu():
    """Affiche le menu principal."""
    print("\n" + "=" * 50)
    print("       SIMNet — Simulateur de Réseau")
    print("=" * 50)
    print("  -- Équipements --")
    print("  1. Ajouter un équipement")
    print("  2. Supprimer un équipement")
    print("  -- Topologie --")
    print("  3. Ajouter un lien")
    print("  4. Supprimer un lien")
    print("  5. Afficher la topologie")
    print("  -- Simulation --")
    print("  6. Envoyer un paquet")
    print("  7. Afficher les statistiques")
    print("  -- Quitter --")
    print("  0. Quitter")
    print("=" * 50)


def main():
    """Point d'entrée principal de SIMNet."""

    topologie  = Topologie()
    simulateur = Simulateur(topologie)

    print("Bienvenue dans SIMNet — Simulateur de Réseau Intelligent")

    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            menu_ajouter_equipement(topologie)
        elif choix == "2":
            menu_supprimer_equipement(topologie)
        elif choix == "3":
            menu_ajouter_lien(topologie)
        elif choix == "4":
            menu_supprimer_lien(topologie)
        elif choix == "5":
            menu_afficher_topologie(topologie)
        elif choix == "6":
            menu_envoyer_paquet(simulateur)
        elif choix == "7":
            menu_statistiques(simulateur)
        elif choix == "0":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez saisir un nombre entre 0 et 7.")


if __name__ == "__main__":
    main()