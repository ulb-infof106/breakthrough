"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA3 INFO
"""


class Player:
    """
    Classe qui représente le joueur
    """

    def __init__(self, playerID, board):
        """
        Constructeur de la classe représentant le joueur
        :param playerID: ID du joueur pour pouvoir l'identifier
        :param board: plateau du joueur
        """
        self.playerID = playerID
        self.posList = []
        self.setPosList(board)

    def setPosList(self, board):
        """
        Méthode initialisant la liste des positions des pions du joueur. Les positions sont récupérées à partir du
        plateau du jeu
        :param board: plateau du jeu
        :return:
        """
        if self.playerID == 1:
            for i in range(board.getlineDimension()):
                for j in range(board.getColumnDimension()):
                    if board.getBoard()[i][j] == 1:
                        self.posList.append([i, j])
        elif self.playerID == 2:
            for i in range(board.getlineDimension()):
                for j in range(board.getColumnDimension()):
                    if board.getBoard()[i][j] == 2:
                        self.posList.append([i, j])
        self.posList.sort()

    def updatePosList(self, sourcePos, destinationPos, nextPlayerPosList):
        """
        Méthode qui met à jour la liste des positions d'un joueur après un coup. On change la position de la source
        du mouvement à 0 et on met la position de la destination du mouvement à l'id du joueur qui vient de jouer. De
        plus, si le joueur vient de manger un pion de l'autre joueur, on retire ce pion de la liste des pions de
        l'adversaire.
        :param sourcePos: source
        :param destinationPos:
        :param nextPlayerPosList:
        :return:
        """
        sourcePos = list(sourcePos)
        destinationPos = list(destinationPos)

        self.posList.remove(sourcePos)
        self.posList.append(destinationPos)

        if destinationPos in nextPlayerPosList:
            nextPlayerPosList.remove(destinationPos)
            return destinationPos
        return

    def getPosList(self):
        """
        Getter qui renvoie la liste des pions du joueur
        :return: liste des pions du joueur
        """
        return self.posList

    def getPlayerID(self):
        """
        Getter qui renvoie l'ID du joueur
        :return: l'ID du joueur
        """
        return self.playerID
