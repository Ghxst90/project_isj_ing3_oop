from equipements import Routeur, Switch, Serveur, Firewall, PointAccesWifi, Terminal
from topologie   import Topologie, Lien
from paquets     import Paquet, Simulateur
from moniteur    import Moniteur  
from securite import RegleFiltrage
import datetime


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
    """Force la saisie d'un texte réel (refuse si c'est uniquement numérique)."""
    while True:
        valeur = input(message).strip()
        if valeur and not valeur.isdigit() and len(valeur) >= longueur_min:
            return valeur
        print(f"   Entrée invalide : Veuillez saisir un texte valide (min {longueur_min} caractères).")

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
        print("   Format d'adresse IP invalide (ex: 192.168.1.1).")


def saisir_identifiant_strict(message, type_champ="Identifiant", longueur_min=4):
    """Force un format d'identifiant ou de SSID sécurisé."""
    while True:
        valeur = input(message).strip()
        if len(valeur) < longueur_min:
            print(f"   {type_champ} trop court (min {longueur_min} caractères).")
            continue
        if valeur.isdigit():
            print(f"   {type_champ} invalide : ne doit pas contenir uniquement des chiffres.")
            continue
        return valeur


def saisir_mot_de_passe_strict(message, longueur_min=6):
    """Force un niveau de sécurité minimal pour le mot de passe du Firewall."""
    while True:
        valeur = input(message).strip()
        if len(valeur) < longueur_min:
            print(f"   Mot de passe trop faible (min {longueur_min} caractères).")
            continue
        return valeur


def menu_ajouter_equipement(topologie):
    """Ajoute un équipement à la topologie avec validations strictes."""
    print("\n  Types disponibles :")
    print("  1. Routeur | 2. Switch | 3. Serveur | 4. Firewall | 5. Point d'accès Wi-Fi | 6. Terminal")

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
            login = saisir_identifiant_strict("  Login admin   : ", "Le login", longueur_min=4)
            mdp   = saisir_mot_de_passe_strict("  Mot de passe  : ", longueur_min=6)
            eq = Firewall(nom, marque, ip, login, mdp)
        elif choix == 5:
            ssid  = saisir_identifiant_strict("  SSID (Nom Wi-Fi) : ", "Le SSID", longueur_min=3)
            canal = saisir_int("  Canal (1-13)     : ", 1, 13)
            eq = PointAccesWifi(nom, marque, ip, ssid, canal)
        elif choix == 6:
            eq = Terminal(nom, marque, ip)

        topologie.ajouter_equipement(eq)
        print(f"\n  [SUCCÈS] L'équipement '{nom}' a bien été intégré !")
    except ValueError as e:
        print(f"\n  [ERREUR] Impossible d'ajouter l'équipement : {e}")
    
    print("-" * 50)
    input("  Appuyez sur ENTRÉE pour continuer...")


def menu_supprimer_equipement(topologie):
    """Supprime un équipement de la topologie."""
    nom = saisir_non_vide("  Nom de l'équipement à supprimer : ")
    topologie.supprimer_equipement(nom)
    print(f"\n  [INFO] Ordre de suppression envoyé pour : '{nom}'.")
    print("-" * 50)
    input("  Appuyez sur ENTRÉE pour continuer...")


def menu_ajouter_lien(topologie):
    """Ajoute un lien entre deux équipements."""
    nom1 = saisir_non_vide("  Équipement 1 : ")
    nom2 = saisir_non_vide("  Équipement 2 : ")
    bp   = saisir_int("  Bande passante (Mbps) : ", mini=1)
    lat  = saisir_int("  Latence (ms)          : ", mini=0)
    topologie.ajouter_lien(nom1, nom2, bp, lat)
    print(f"\n  [SUCCÈS] Lien physique établi entre '{nom1}' et '{nom2}'.")
    print("-" * 50)
    input("  Appuyez sur ENTRÉE pour continuer...")


def menu_supprimer_lien(topologie):
    """Supprime un lien entre deux équipements."""
    nom1 = saisir_non_vide("  Équipement 1 : ")
    nom2 = saisir_non_vide("  Équipement 2 : ")
    topologie.supprimer_lien(nom1, nom2)
    print(f"\n  [INFO] Ordre de coupure appliqué.")
    print("-" * 50)
    input("  Appuyez sur ENTRÉE pour continuer...")


def menu_afficher_topologie(topologie):
    """Affiche la topologie complète."""
    print("\n" + "-"*15 + " ARCHITECTURE DE LA TOPOLOGIE " + "-"*15)
    topologie.afficher()
    print("-" * 60)
    input("   Visualisation terminée. Appuyez sur ENTRÉE...")


def menu_envoyer_paquet(simulateur):
    """Envoie un paquet à travers le réseau."""
    print("\n  Protocoles disponibles : TCP | UDP | ICMP")
    source      = saisir_ip("   IP source      : ")
    destination = saisir_ip("   IP destination : ")
    
    while True:
        protocole = saisir_non_vide("   Protocole      : ").upper()
        if protocole in ["TCP", "UDP", "ICMP"]:
            break
        print("   Protocole invalide. Utilisez uniquement TCP, UDP ou ICMP.")

    taille   = saisir_int("   Taille (octets)  : ", mini=1)
    priorite = saisir_int("   Priorité (1-5)   : ", mini=1, maxi=5)

    nom_source = saisir_non_vide("   Nom équipement source      : ")
    nom_dest   = saisir_non_vide("   Nom équipement destination : ")

    paquet = Paquet(source, destination, protocole, taille, priorite)
    
    print("\n" + "="*15 + " DÉBUT DE LA SIMULATION RÉSEAU " + "="*15)
    try:
        simulateur.envoyer_paquet(paquet, nom_source, nom_dest)
    except KeyError as e:
        print(f"\n   ERREUR DE ROUTAGE : L'équipement {e} n'existe pas.")
    except Exception as e:
        print(f"\n   ERREUR INCONNUE : {e}")
    print("=" * 61)
        
    print("-" * 50)
    input("   Simulation terminée. Appuyez sur ENTRÉE...")


def menu_statistiques(simulateur):
    """Affiche les statistiques de simulation de base."""
    print("\n" + "-"*18 + " STATISTIQUES GLOBALES " + "-"*18)
    simulateur.afficher_statistiques()
    print("-" * 59)
    input("   Appuyez sur ENTRÉE...")




def afficher_tableau_bord_externe(moniteur):
    """Lecture externe et sécurisée des attributs du moniteur."""
    print('\n' + '=' * 55)
    print('        TABLEAU DE BORD — SIMNet (Mode Lecteur)')
    print('=' * 55)
    
    try:
        # Accès direct aux attributs privés via le nom manglé (_Classe__attribut)
        stats = moniteur._Moniteur__stats_eq
        liens = moniteur._Moniteur__utilisation_liens
        
        print('\n--- Équipements ---')
        if stats:
            for nom, s in stats.items():
                print(f"  [✓] {nom:20s}  transmis={s['transmis']}  perdus={s['perdus']}")
        else:
            print('  (Aucune statistique d\'équipement disponible)')

        print('\n--- Utilisation des liens ---')
        if liens:
            for lien, octets in liens.items():
                print(f'  {lien:35s}  {octets:>10.0f} octets')
        else:
            print('  (Aucun trafic enregistré)')
            
    except Exception:
        print("\n  [INFO] Le moniteur n'a pas encore reçu de données de simulation.")
    
    print('=' * 55)


def menu_moniteur(moniteur):
    """Affiche le tableau de bord via la fonction utilitaire externe."""
    afficher_tableau_bord_externe(moniteur)
    input("\n   Appuyez sur ENTRÉE pour revenir au menu...")



def generer_rapport_moniteur(moniteur):
    """Génère un rapport texte complet avec les stats et l'historique des paquets."""
    try:
        # Accès aux attributs privés via name mangling
        stats = moniteur._Moniteur__stats_eq
        liens = moniteur._Moniteur__utilisation_liens
        
        # Récupération de l'historique via la méthode existante dans moniteur.py
        historique = moniteur.get_historique() 
        
        with open("rapport_simnet.txt", "w", encoding="utf-8") as f:
            f.write("=== RAPPORT DE MONITORING SIMNET ===\n")
            f.write(f"Date du rapport : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            f.write("--- STATISTIQUES ÉQUIPEMENTS ---\n")
            if stats:
                for nom, s in stats.items():
                    f.write(f"Équipement: {nom} | Transmis: {s['transmis']} | Perdus: {s['perdus']}\n")
            else:
                f.write("Aucune donnée.\n")
                
            f.write("\n--- UTILISATION DES LIENS ---\n")
            if liens:
                for lien, octets in liens.items():
                    f.write(f"Lien {lien}: {octets:.0f} octets\n")
            else:
                f.write("Aucun trafic enregistré.\n")
            
            # --- AJOUT DE L'HISTORIQUE ---
            f.write("\n--- HISTORIQUE DES 10 DERNIERS PAQUETS ---\n")
            if historique:
                for i, paquet_info in enumerate(historique, 1):
                    f.write(f"{i}. {paquet_info}\n")
            else:
                f.write("Aucun paquet traité pour le moment.\n")
        
        print("\n  [SUCCÈS] Rapport 'rapport_simnet.txt' généré avec succès !")
    except Exception as e:
        print(f"\n  [ERREUR] Impossible de générer le rapport : {e}")

def menu_securite(topologie):
    """Gère la sécurité avec un bloc de protection total contre les erreurs."""
    print("\n" + "="*30)
    print("      ADMINISTRATION FIREWALL")
    print("="*30)

    try:
        # 1. Vérification : y a-t-il des firewalls ?
        firewalls = [n for n, e in topologie.equipements.items() if e.__class__.__name__ == "Firewall"]
        if not firewalls:
            print("   Aucun Firewall enregistré dans la topologie.")
            return

        # 2. Saisie et recherche
        nom_fw = input("  Nom du Firewall : ").strip()
        eq = topologie.get_equipement(nom_fw)
        
        if not eq or eq.__class__.__name__ != "Firewall":
            print(f"   '{nom_fw}' est introuvable ou n'est pas un Firewall.")
            return

        # 3. Accès sécurisé au gestionnaire avec gestion d'exception
        # On tente de trouver l'attribut privé du gestionnaire
        gestionnaire = getattr(eq, "_Firewall__gestionnaire", None)
        
        if gestionnaire is None:
            print("   Le gestionnaire de sécurité n'est pas actif sur cet équipement.")
            return

        # Si on arrive ici, tout est OK
        print(f"\n  -- Gestion Firewall '{nom_fw}' --")
        print("  1. Ajouter une règle | 2. Afficher les règles | 3. Supprimer une règle")
        choix = input("  Choix : ")
        
        if choix == "1":
            from securite import RegleFiltrage
            action = input("  Action (AUTORISER/BLOQUER) : ").upper()
            ip = input("  IP source (ou Entrée) : ") or None
            proto = input("  Protocole (TCP/UDP/ICMP ou Entrée) : ") or None
            gestionnaire.ajouter_regle(RegleFiltrage(action, ip_source=ip, protocole=proto))
            print("   Règle ajoutée.")
            
        elif choix == "2":
            gestionnaire.afficher_regles()
            
        elif choix == "3":
            idx = int(input("  Index de la règle : "))
            gestionnaire.supprimer_regle(idx)

    except Exception as e:
        # ICI : Si une erreur survient (ex: attribut introuvable), ça ne plante plus
        print(f"\n   Une erreur est survenue lors de l'accès au Firewall : {e}")
        print("  (Le gestionnaire est peut-être mal initialisé dans la classe Firewall)")
    
    input("\n  Appuyez sur ENTRÉE pour revenir...")
def afficher_menu():
    """Affiche le menu principal étendu."""
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
    print("  -- Simulation & Métriques --")
    print("  6. Envoyer un paquet")
    print("  7. Afficher les statistiques générales")
    print("  8. Afficher le TABLEAU DE BORD (Moniteur)  [NOUVEAU]")
    print("  9. Générer un rapport de monitoring")
    print("  10. Gérer les règles de sécurité du Firewall")
    print("-"*50)
    print("  0. Quitter")
    print("=" * 50)


def main():
    """Point d'entrée principal de SIMNet."""
    topologie  = Topologie()
    simulateur = Simulateur(topologie)
    
    # Initialisation du moniteur réseau avec les instances requises
    moniteur = Moniteur(topologie, simulateur)

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
        elif choix == "8":
            menu_moniteur(moniteur)
        elif choix == "9":
             generer_rapport_moniteur(moniteur)
        elif choix == "10":
            menu_securite(topologie)
        elif choix == "0":
            print("\n[FIN] Fermeture du simulateur. Au revoir !")
            break
        else:
            print(" Choix invalide. Veuillez saisir un nombre entre 0 et 9.")


if __name__ == "__main__":
    main()