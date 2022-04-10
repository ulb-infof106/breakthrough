"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA INFO
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
        self.columnDimension = None
        self.lineDimension = None
        self.board = []

        try:
            self.createFileBoard(file)
        except TypeError:
            if board:
                self.createGivenBoard(board)
            else:
                self.setDefaultBoard()
    
    def copyBoard(self, board):
        """
        Méthode qui permet de copier un plateau.
        : param board : plateau à copier
        """
        for i in range(len(board)):
            self.board.append([])
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    self.board[i].append(0)
                elif board[i][j] == 1:
                    self.board[i].append(1)
                elif board[i][j] == 2:
                    self.board[i].append(2)

    def createGivenBoard(self, board):
        """
        Méthode qui permet de créer un objet board sans référence à l'aide d'une matrice fournie 
        : param board : plateau de jeu à intégrer à l'objet
        """
        self.lineDimension = len(board)
        self.columnDimension = len(board[0])
        self.copyBoard(board)

    def createFileBoard(self, file):
        """
        Méthode qui permet de créer un plateau en fonction d'un fichier reçu 
        : param file : fichier reçu, contenant les dimensions du plateau
        """
        try:
            with open(file) as f:
                line = f.readlines()
            self.lineDimension = int(line[0].rstrip("\n").strip(" ")[0])
            self.columnDimension = int(line[0].rstrip("\n").strip(" ")[2])
            for i in range(self.lineDimension):
                self.board.append([0 for i in range(self.columnDimension)])
            self.placeOnBoard(line[1], 1)
            self.placeOnBoard(line[2], 2)
        except ValueError:
            self.setDefaultBoard()

    def getlineDimension(self):
        """
        getter qui permet de fournir la dimention en lignes du plateau
        :return: la dimension en ligne
        """
        return self.lineDimension

    def getColumnDimension(self):

        """
        Getter qui permet de fournir la dimention en colonnes du plateau
        : return : la dimension en colonne
        """
        return self.columnDimension

    def getBoard(self):
        """
        Getter permettant de fournir la matrice correspondant au plateau
        : return : la matrice correspondant au plateau
        """
        return self.board

    def setDefaultBoard(self):
        """
        Méthode permettant d'initialiser un plateau par défaut, sans base de fichier
        """
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
        """
        Méthode qui permet de mettre à jour le plateau "à l'envers": il s'agit de l'annulation d'un coup, spécifiquement
        si un pion adverse a été mangé.
        : param destinationpos : destination de l'annulation du coup
        : param player : joueur concerné
        : param sourcePos : source de l'annulation du coup
        """
        if player.getPlayerID() == 2:
            self.board[sourcePos[0]][sourcePos[1]] = 1
            self.board[destinationpos[0]][destinationpos[1]] = player.getPlayerID()
        else:
            self.board[sourcePos[0]][sourcePos[1]] = 2
            self.board[destinationpos[0]][destinationpos[1]] = player.getPlayerID()

    def forwardUpdate(self, destinationpos, eatenPeg, player, sourcePos):
        """
        Méthode qui permet de mettre à jour le plateau de façon régulière et de mémoriser si un pion a été mangé
        : param destinationpos : destination du mouvement
        : param eatenPeg : pion mangé
        : param player : joueur concerné
        : param sourcePos : source du mouvement
        : return : pion mangé
        """
        if self.board[destinationpos[0]][destinationpos[1]] != 0:
            eatenPeg = self.board[destinationpos[0]][destinationpos[1]]
        self.board[sourcePos[0]][sourcePos[1]] = 0
        self.board[destinationpos[0]][destinationpos[1]] = player.getPlayerID()
        return eatenPeg

    def findCounter(self):
        """
        Méthode permettant de trouver le nombre de pions noirs et de pions blanc le plateau possède
        : return : le nombre de pions blancs et le nombre de pions noirs
        """
        counterWhite = 0
        counterBlack = 0
        for i in range(self.lineDimension):
            if 2 in self.board[i]:
                counterBlack += 1
            if 1 in self.board[i]:
                counterWhite += 1
        return counterWhite, counterBlack

    def findWinner(self):
        """
        Méthode qui permet de trouver un gagnant en fonction du nombre de pions:
        Si aucun pion blanc n'est trouvé, le joueur noir a gagné et vice-versa.
        Si un pion noir est trouvé sur la dernière ligne, le joueur noir a gagné.
        Si un pion blanc est trouvé sur la première ligne, le joueur blanc a gagné.
        : return : le playerID du gagnant
        """
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

