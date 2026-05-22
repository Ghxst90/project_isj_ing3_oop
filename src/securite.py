import ipaddress
 
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
        """Retourne True si le paquet satisfait tous les criteres de la regle."""
 
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