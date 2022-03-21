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

    def __init__(self, file):
        """
        Constructeur de la classe du plateau du jeu. Si un fichier a été donné en entrée, le plateau est
        initialisé selon son contenu, sinon, un plateau de base est crée.
        :param file: Fichier reçu en entrée.
        """
        self.board = []
        try:
            with open(file) as f:
                line = f.readlines()
            self.lineDimension = int(line[0].rstrip("\n").strip(" ")[0])
            self.columnDimension = int(line[0].rstrip("\n").strip(" ")[2])
            for i in range(self.lineDimension):
                self.board.append([0 for i in range(self.columnDimension)])

            self.placeOnBoard(line[1], 1)
            self.placeOnBoard(line[2], 2)
        except TypeError:
            self.setDefaultBoard()

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

    def printBoard(self):
        """
        Méthode qui se charge de  l'affichage du plateau: on affiche les contours ainsi que les coordonnées des lignes
        et colonnes, et on remplace les 2,1 et 0 par leurs symboles respectifs
        :return: aucun
        """
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
        print("\n")

    def displayProposedMove(self, move):
        """
        Méthode qui permet d'afficher le plateau avec le coup suggéré au joueur.
        On imprime la matrice normalement, sauf à l'endroit précisé par move où on imprime un #
        :param move: coup suggéré
        :return: aucun
        """
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        print(" " * 3 + self.columnDimension * " —")
        for line in range(self.lineDimension):
            print(str(-(line - self.lineDimension)) + " | ", end="")
            for column in range(self.columnDimension):
                if move and line == move[0] and column == move[1]:
                    print("#", end=" ")
                elif self.board[line][column] == 0:
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
        print("\n")

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
        :return:
        """
        if not backwards:
            self.board[sourcePos[0]][sourcePos[1]] = 0
            self.board[destinationpos[0]][destinationpos[1]] = player.getPlayerID()
        else:
            if player.getPlayerID() == 2:
                self.board[sourcePos[0]][sourcePos[1]] = 1
                self.board[destinationpos[0]][destinationpos[1]] = player.getPlayerID()
            else:
                self.board[sourcePos[0]][sourcePos[1]] = 2
                self.board[destinationpos[0]][destinationpos[1]] = player.getPlayerID()
