"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA3 INFO
"""

import Utils


class Board:
    """
    Classe qui représente le plateau du jeu
    """

    def __init__(self, file, board=None):
        """
        Constructeur de la classe du plateau du jeu. Si un fichier a été donné en entrée, le plateau est
        initialisé selon son contenu, sinon, un plateau de base est crée.
        :param file: Fichier reçu en entrée.
        """
        self.board = []

        try:
            self.createFileBoard(file)
        except TypeError:
            if board:
                self.createGivenBoard(board)
            else:
                self.setDefaultBoard()

    def createGivenBoard(self, board):
        self.lineDimension = len(board)
        self.columnDimension = len(board[0])
        self.copyBoard(board)

    def createFileBoard(self, file):
        with open(file) as f:
            line = f.readlines()
        self.lineDimension = int(line[0].rstrip("\n").strip(" ")[0])
        self.columnDimension = int(line[0].rstrip("\n").strip(" ")[2])
        for i in range(self.lineDimension):
            self.board.append([0 for i in range(self.columnDimension)])
        self.placeOnBoard(line[1], 1)
        self.placeOnBoard(line[2], 2)

    def copyBoard(self, board):
        for i in range(len(board)):
            self.board.append([])
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    self.board[i].append(0)
                elif board[i][j] == 1:
                    self.board[i].append(1)
                elif board[i][j] == 2:
                    self.board[i].append(2)

    def getlineDimension(self):

        """
        getter qui permet de fournir la dimention en lignes du plateau
        :return: la dimension en ligne
        """
        return self.lineDimension

    def getColumnDimension(self):

        """
        getter qui permet de fournir la dimention en colonnes du plateau
        :return: la dimension en colonne
        """
        return self.columnDimension

    def getBoard(self):
        return self.board

    def setDefaultBoard(self):
        self.lineDimension = self.columnDimension = 7
        for i in range(self.lineDimension):
            if i == 0 or i == 1:
                self.board.append([2 for i in range(self.columnDimension)])
            elif i == self.lineDimension - 1 or i == self.lineDimension - 2:
                self.board.append([1 for i in range(self.columnDimension)])
            else:
                self.board.append([0 for i in range(self.columnDimension)])

    def placeOnBoard(self, line, player):

        """
        Méthode qui permet de placer les pions blancs et noirs sur le plateau
        :param line:ligne reçue en paramètre, permettant de connaitre les emplacements des pions, puisqu'il s'agit de la
        ligne reçue depuis le fichier analysé.
        :param player: joueur concerné
        :return: aucun
        """
        pegs = line.replace(",", " ").split()
        for i in pegs:
            lineCoord, columnCoord = Utils.extractPosition(self.lineDimension, i)
            self.board[lineCoord][columnCoord] = player

    """def printBoard(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        print(" " * 3 + self.columnDimension * " —")
        for line in range(self.lineDimension):
            print(str(-(line - self.lineDimension)) + " | ", end="")
            for column in range(self.columnDimension):
                if self.board[line][column] == 0:
                    print(".", end=" ")
                elif self.board[line][column] == 1:
                    print("W", end=" ")
                elif self.board[line][column] == 2:
                    print("B", end=" ")
            print("|")
        print(" " * 3 + self.columnDimension * " —")
        print(" " * 3, end="")
        for i in range(self.columnDimension):
            print(" " + alphabet[i], end="")
        print("\n")"""

    def detectWinner(self, player, nextPlayer):
        """
        Méthode qui détermine si un joueur a gagné: si un joueur se trouve sur la première ligne du côté adverse, on
        retourne son ID correspondant. Si la liste de pions du joueur est vide, son adversaire a gagné, et on
        retourne son ID correspondant.
        :return: 1 si joueur 1 a gagné, 2 si joueur 2 a gagné, None si aucun gagnant
        """
        if len(nextPlayer.getPosList()) == 0:
            return player.getPlayerID()
        if len(player.getPosList()) == 0:
            return nextPlayer.getPlayerID()
        pos = player.getPosList()

        for peg in pos:
            if player.getPlayerID() == 1 and peg[0] == 0:
                # conditions pour qu'un pion blanc se trouve sur la première rangée noire et le blanc a gagné
                return player.getPlayerID()
            elif player.getPlayerID() == 2 and peg[0] == self.lineDimension - 1:
                # conditions pour qu'un pion noir se trouve que la première rangée blanche et le noir a gagné
                return player.getPlayerID()
        return 0

    def updateBoard(self, sourcePos, destinationpos, player, backwards=False):

        """
        Méthode qui met à jour le plateau lors d'un mouvement du joueur

        :param backwards: Indice qui permet de savoir si on annule un mouvement ou si on en fait un. Si on annule le
        mouvement, il faut rajouter le pion mangé dans la liste des pions du joueur.
        :param sourcePos: position source du mouvement
        :param destinationpos: position de destination du mouvement
        :param player: joueur actuel
        :return: pion mangé
        """
        eatenPeg = 0
        if not backwards:
            eatenPeg = self.forwardUpdate(destinationpos, eatenPeg, player, sourcePos)
        else:
            self.backwardsUpdate(destinationpos, player, sourcePos)
        return eatenPeg

    def backwardsUpdate(self, destinationpos, player, sourcePos):
        if player.getPlayerID() == 2:
            self.board[sourcePos[0]][sourcePos[1]] = 1
            self.board[destinationpos[0]][destinationpos[1]] = player.getPlayerID()
        else:
            self.board[sourcePos[0]][sourcePos[1]] = 2
            self.board[destinationpos[0]][destinationpos[1]] = player.getPlayerID()

    def forwardUpdate(self, destinationpos, eatenPeg, player, sourcePos):
        if self.board[destinationpos[0]][destinationpos[1]] != 0:
            eatenPeg = self.board[destinationpos[0]][destinationpos[1]]
        self.board[sourcePos[0]][sourcePos[1]] = 0
        self.board[destinationpos[0]][destinationpos[1]] = player.getPlayerID()
        return eatenPeg

    def findWinner(self):
        counter1, counter2 = self.findCounter()
        if counter1 == 0:
            return 2
        elif counter2 == 0:
            return 1
        elif 1 in self.board[0]:
            return 1
        elif 2 in self.board[self.lineDimension - 1]:
            return 2
        return 0

    def findCounter(self):
        counter1 = 0
        counter2 = 0
        for i in range(self.lineDimension):
            if 2 in self.board[i]:
                counter2 += 1
            if 1 in self.board[i]:
                counter1 += 1
        return counter1, counter2
