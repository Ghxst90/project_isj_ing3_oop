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


def saisir_texte_strict(message, longueur_min=2):
    """Force la saisie d'un texte réel (refuse si c'est uniquement numérique comme '1')."""
    while True:
        valeur = input(message).strip()
        if valeur and not valeur.isdigit() and len(valeur) >= longueur_min:
            return valeur
        print(f"   Entrée invalide : Veuillez saisir un texte valide (min {longueur_min} caractères, pas uniquement des chiffres).")


def saisir_ip(message):
    """Force l'utilisateur à saisir une adresse IP strictement valide au format X.X.X.X"""
    while True:
        ip = input(message).strip()
        parties = ip.split('.')
        if len(parties) == 4:
            valide = True
            for partie in parties:
                if not partie.isdigit() or not (0 <= int(partie) <= 255):
                    valide = False
                    break
            if valide:
                return ip
        print("   Format d'adresse IP invalide. Veuillez entrer un format valide (ex: 192.168.1.1).")


def saisir_identifiant_strict(message, type_champ="Identifiant", longueur_min=4):
    """Force un format d'identifiant ou de SSID sécurisé (pas uniquement des chiffres, longueur min)."""
    while True:
        valeur = input(message).strip()
        if len(valeur) < longueur_min:
            print(f"  {type_champ} trop court (min {longueur_min} caractères).")
            continue
        if valeur.isdigit():
            print(f"  {type_champ} invalide : ne doit pas contenir uniquement des chiffres.")
            continue
        return valeur


def saisir_mot_de_passe_strict(message, longueur_min=6):
    """Force un niveau de sécurité minimal pour le mot de passe du Firewall."""
    while True:
        valeur = input(message).strip()
        if len(valeur) < longueur_min:
            print(f"   Mot de passe trop faible (min {longueur_min} caractères pour la sécurité).")
            continue
        return valeur


def menu_ajouter_equipement(topologie):
    """Ajoute un équipement à la topologie avec validations strictes."""
    print("\n  Types disponibles :")
    print("  1. Routeur")
    print("  2. Switch")
    print("  3. Serveur")
    print("  4. Firewall")
    print("  5. Point d'accès Wi-Fi")
    print("  6. Terminal")

    choix = saisir_int("  Votre choix : ", 1, 6)
    
    nom    = saisir_texte_strict("  Nom       : ")
    marque = saisir_texte_strict("  Marque    : ")
    ip     = saisir_ip("  Adresse IP: ")

    try:
        if choix == 1:
            eq = Routeur(nom, marque, ip)
        elif choix == 2:
            eq = Switch(nom, marque, ip)
        elif choix == 3:
            eq = Serveur(nom, marque, ip)
        elif choix == 4:
            # Contraintes renforcées sur le Login (admin, etc.) et le Mot de passe
            login = saisir_identifiant_strict("  Login admin   : ", "Le login", longueur_min=4)
            mdp   = saisir_mot_de_passe_strict("  Mot de passe  : ", longueur_min=8)
            eq = Firewall(nom, marque, ip, login, mdp)
        elif choix == 5:
            # Contraintes renforcées sur le SSID (ex: "WiFi-ISJ")
            ssid  = saisir_identifiant_strict("  SSID (Nom Wi-Fi) : ", "Le SSID", longueur_min=3)
            canal = saisir_int("  Canal (1-13)     : ", 1, 13)
            eq = PointAccesWifi(nom, marque, ip, ssid, canal)
        elif choix == 6:
            eq = Terminal(nom, marque, ip)

        topologie.ajouter_equipement(eq)
        print(f"\n  [SUCCÈS] L'équipement '{nom}' ({marque} - {ip}) a bien été intégré à la topologie !")

    except ValueError as e:
        print(f"\n  [ERREUR] Impossible d'ajouter l'équipement : {e}")
    
    print("-" * 50)
    input("  Appuyez sur ENTRÉE pour revenir au menu principal...")


def menu_supprimer_equipement(topologie):
    """Supprime un équipement de la topologie."""
    nom = saisir_non_vide("  Nom de l'équipement à supprimer : ")
    topologie.supprimer_equipement(nom)
    print(f"\n  [INFO] Ordre de suppression envoyé pour l'équipement : '{nom}'.")
    print("-" * 50)
    input("  Appuyez sur ENTRÉE pour revenir au menu principal...")


def menu_ajouter_lien(topologie):
    """Ajoute un lien entre deux équipements avec vérification des entiers."""
    print("\n  Équipements disponibles :")
    for nom in topologie.get_equipements():
        print(f"    - {nom}")

    nom1 = saisir_non_vide("\n  Équipement 1 : ")
    nom2 = saisir_non_vide("  Équipement 2 : ")
    bp   = saisir_int("  Bande passante (Mbps) : ", mini=1)
    lat  = saisir_int("  Latence (ms)          : ", mini=0)
    topologie.ajouter_lien(nom1, nom2, bp, lat)
    print(f"\n  [SUCCÈS] Lien physique établi avec succès entre '{nom1}' et '{nom2}'.")
    print("-" * 50)
    input("  Appuyez sur ENTRÉE pour revenir au menu principal...")


def menu_supprimer_lien(topologie):
    """Supprime un lien entre deux équipements."""
    nom1 = saisir_non_vide("  Équipement 1 : ")
    nom2 = saisir_non_vide("  Équipement 2 : ")
    topologie.supprimer_lien(nom1, nom2)
    print(f"\n  [INFO] Ordre de coupure du lien entre '{nom1}' et '{nom2}' appliqué.")
    print("-" * 50)
    input("  Appuyez sur ENTRÉE pour revenir au menu principal...")


def menu_afficher_topologie(topologie):
    """Affiche la topologie complète."""
    print("\n" + "-"*15 + " ARCHITECTURE DE LA TOPOLOGIE " + "-"*15)
    topologie.afficher()
    print("-" * 60)
    input("  Visualisation terminée. Appuyez sur ENTRÉE pour revenir au menu...")


def menu_envoyer_paquet(simulateur):
    """Envoie un paquet à travers le réseau après validation des paramètres d'entrée."""
    print("\n  Protocoles disponibles : TCP | UDP | ICMP")
    source      = saisir_ip("  IP source      : ")
    destination = saisir_ip("  IP destination : ")
    
    while True:
        protocole = saisir_non_vide("  Protocole      : ").upper()
        if protocole in ["TCP", "UDP", "ICMP"]:
            break
        print("  Protocole invalide. Utilisez uniquement TCP, UDP ou ICMP.")

    taille   = saisir_int("  Taille (octets)  : ", mini=1)
    priorite = saisir_int("  Priorité (1-5)   : ", mini=1, maxi=5)

    nom_source = saisir_non_vide("  Nom équipement source      : ")
    nom_dest   = saisir_non_vide("  Nom équipement destination : ")

    paquet = Paquet(source, destination, protocole, taille, priorite)
    
    print("\n" + "="*15 + " DÉBUT DE LA SIMULATION RÉSEAU " + "="*15)
    
    try:
        simulateur.envoyer_paquet(paquet, nom_source, nom_dest)
    except KeyError as e:
        print(f"\n  ERREUR DE ROUTAGE : L'équipement {e} n'existe pas dans la topologie actuelle.")
        print("  Vérifiez les noms saisis ou affichez la topologie (Option 5) pour contrôler.")
    except Exception as e:
        print(f"\n  ERREUR INCONNUE lors de la simulation : {e}")

    print("=" * 61)
        
    print("-" * 50)
    input("  Simulation terminée. Appuyez sur ENTRÉE pour revenir au menu principal...")


def menu_statistiques(simulateur):
    """Affiche les statistiques de simulation."""
    print("\n" + "-"*18 + " STATISTIQUES GLOBALES " + "-"*18)
    simulateur.afficher_statistiques()
    print("-" * 59)
    input("  Appuyez sur ENTRÉE pour revenir au menu principal...")


def afficher_menu():
    """Affiche le menu principal d'origine."""
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
    print("-"*50)
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
            print("\n[FIN] Fermeture du simulateur. Au revoir !")
            break
        else:
            print(" Choix invalide. Veuillez saisir un nombre entre 0 et 7.")


if __name__ == "__main__":
    main()