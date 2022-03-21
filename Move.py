
"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA3 INFO
"""

import Utils


class Move:
    """
    Classe qui représente un mouvement du joueur. Une nouvelle instance de move est crée à chaque mouvement.
    """

    def __init__(self, player, board):
        """
        source est la liste des mouvements qui peuvent être joués
        :param player: joueur effectuant le coup
        :param board: plateau du jeu
        """

        self.player = player
        self.possibleSources = self.initValidPeg(board)
        #self.inputSelectPeg(board)
        #self.destination = Utils.inputUser(board)

    def initValidPeg(self, board):
        """
        Méthode qui trouve un premier pion valide à proposer au joueur. On itère sur la liste des pions du joueur, et
        si le pion est jouable, on renvoie son emplacement, sinon, on en trouve un nouveau
        :param board: Plateau du jeu
        :return: la position du pion jouable trouvé
        """
        # on itère sur la liste des pions du joueur, si le mouvement est correct on renvoie le mouvement, sinon on
        # réessaye
        possibleSources = []
        for sourcePos in self.player.getPosList():
            if Utils.checkPos(board, sourcePos, self.player.getPlayerID()):
                possibleSources.append(sourcePos)
        return possibleSources


    def getSource(self):
        """
        Getter qui renvoie la position source du mouvement.
        :return: la position source du mouvement
        """
        return self.source

    def getDestination(self):
        """
        Getter qui renvoie la position de destination du mouvement
        :return: La position de destination du mouvement
        """
        return self.destination

    def inputSelectPeg(self, board):
        while True:
            inp = input("Veuillez sélectionner un pion:")
            if inp == "j":
                self.source = self.findLeftPeg(board)
                board.displayProposedMove(self.source)
            elif inp == "l":
                self.source = self.findRightPeg(board)
                board.displayProposedMove(self.source)
            elif inp == "k":
                self.source = self.findDownPeg(board)
                board.displayProposedMove(self.source)
            elif inp == "i":
                self.source = self.findUpPeg(board)
                board.displayProposedMove(self.source)
            elif inp == "y":
                return self.source

    def findLeftPeg(self, board):
        """
        Méthode qui permet de trouver un pion pour lequel il existe un mouvement valide à gauche du pion initial
        on veut trouver une position valide la plus proche du point où on se trouve. Si on est au bord du plateau, on
        recommence tout à droite. On se sert de la dernière position trouvée pour se situer
        :param board: plateau
        :return: coordonnées matricielles du pion
        """

        coord1 = self.source[0]
        coord2 = self.source[1]
        found = False

        while not found:
            if coord2 == 0:
                coord2 = board.getlineDimension() - 1
            else:
                coord2 = coord2 - 1
            found = Utils.checkPos(board, (coord1, coord2), self.player.getPlayerID())
            if found:
                return coord1, coord2

    def findRightPeg(self, board):
        """
        Méthode qui permet de trouver un mouvement valide à droite du pion initial
        :param board: plateau
        :return: coordonnées matricielles du pion
        """
        coord1 = self.source[0]
        coord2 = self.source[1]
        found = False
        while not found:
            if coord2 == board.getlineDimension() - 1:
                coord2 = 0
            else:
                coord2 = coord2 + 1
            found = Utils.checkPos(board, (coord1, coord2), self.player.getPlayerID())
            if found:
                return coord1, coord2

    def findUpPeg(self, board):
        """
        Méthode qui permet de trouver un mouvement valide en haut du pion initial
        on parcourt la liste des pions du joueur en regardant si on en trouve un qui est sur la ligne supérieure. Si on
        n'en trouve pas, on regarde sur celle encore supérieure, etc, jusqu'à arriver au bord du plateau, cas dans
        lequel on est replacé sur la ligne la plus basse du plateau.
        :param board: plateau
        :return: coordonnées matricielles du pion
        """
        if self.source[0] == 0:
            coord1 = board.getlineDimension() - 1
        else:
            coord1 = self.source[0]
        possibleMoves = []
        found = False
        while not found:
            for pos in self.player.getPosList():
                if pos[0] == coord1 - 1 and Utils.checkPos(board, (coord1 - 1, pos[1]),
                                                           self.player.getPlayerID()):
                    possibleMoves.append((coord1 - 1, pos[1]))

            if len(possibleMoves) == 0:
                if coord1 > 1:
                    coord1 -= 1
                else:
                    coord1 = board.getlineDimension()
            else:
                pos = Utils.manhattanCalculation(self.source, possibleMoves)
                found = True
                return pos

    def findDownPeg(self, board):
        """
         Méthode qui permet de trouver un mouvement valable sur un pion situé en dessous du pion initial. Fonctionne
         similairement à la méthode findUpPeg
        :param board: plateau
        :return: coordonnées matricielles du pion
        """
        if self.source[0] == board.getlineDimension() - 1:
            coord1 = 0
        else:
            coord1 = self.source[0]
        possibleMoves = []
        found = False
        while not found:
            for pos in self.player.getPosList():
                if pos[0] == coord1 + 1 and Utils.checkPos(board, (coord1 + 1, pos[1]),
                                                           self.player.getPlayerID()):
                    possibleMoves.append((coord1 + 1, pos[1]))

            if len(possibleMoves) == 0:
                if coord1 < board.getlineDimension() - 1:
                    coord1 += 1
                else:

                    coord1 = board.getlineDimension()
            else:
                pos = Utils.manhattanCalculation(self.source, possibleMoves)
                found = True
                return pos
