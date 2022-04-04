"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA3 INFO
"""

import Utils


class Move:
    """
    Classe qui représente un mouvement du joueur. Une nouvelle instance de move est créé à chaque mouvement.
    """

    def __init__(self, player, source, destination):
        """
        Source est la liste des mouvements qui peuvent être joués
        : param player : joueur effectuant le coup
        """

        self.player = player
        self.source = source
        self.destination = destination

    def getSource(self):
        """
        Getter qui renvoie la position source du mouvement.
        : return : la position source du mouvement
        """
        return self.source

    def getDestination(self):
        """
        Getter qui renvoie la position de destination du mouvement
        : return : La position de destination du mouvement
        """
        return self.destination