"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA3 INFO
"""

import Utils


class IA:
    """
    Classe représentant l'intelligence artificielle contre qui le joueur joue
    """
    def __init__(self, player, game):
        self.depth = 3
        self.player = player
        self.value = 100000
        if self.player.getPlayerID() == 1:
            self.opponent = game.player2
        else:
            self.opponent = game.player1

    def getPlayer(self):
        """
        Getter renvoyant le joueur que représente l'IA
        :return: le joueur que représente l'IA
        """
        return self.player

    def play(self, game):
        """
        Méthode qui permet de faire jouer l'IA, qui appelle la méthode Minimax et qui met à jour la liste des pions de
        l'IA ainsi que le plateau du jeu
        :param game: l'état du jeu
        :return: aucun
        """
        move, score = self.Minimax(game, self.depth, True)
        #game.getBoard().printBoard()
        game.getBoard().updateBoard(move[0], move[1], self.player)
        self.player.updatePosList(move[0], move[1], self.opponent.getPosList())
        return move

    def Minimax(self, game, depth, maximize):
        """
        Méthode Minimax. Permet de trouver le meilleur coup par l'IA par backtracking.
        :param game: l'état du jeu
        :param depth: la profondeur , c'est à dire le nombre d'appels récursifs autorisés
        :param maximize: indice permettant de définir si on cherche à maximiser le score (si l'AI joue), ou si on
        cherche à le minimiser (si l'adversaire joue)
        :return: le score et son mouvement correspondant
        """
        best_actions = []
        if depth == 0 or game.winner:
            score = self.getScore(game, depth)
            return None, score
        best_score = Utils.findBestScore(maximize)
        possibleSourceMoves = self.findPossibleSourceMoves(game.getBoard(), maximize)
        for source in possibleSourceMoves:
            possibleDestinationMove = self.findPossibleDestinationMoves(source, game.getBoard(), maximize)

            for dest in possibleDestinationMove:
                deletedPeg = self.simulateMove(source, dest, game, maximize)
                move, score = self.Minimax(game, depth - 1, not maximize)
                self.undoMove(deletedPeg, maximize, source, dest, game)

                if Utils.isBetter(score, best_score, maximize):
                    best_score = score
                    best_actions = [[source, dest]]

                elif score == best_score:
                    best_actions.append([source, dest])
        return Utils.chooseMove(best_actions), best_score

    def getScore(self, game, depth):
        """
        Méthode qui permet de trouver le score du coup en fonction d'une valeur initialisée à la construction de la
        classe
        :param game: l'état du jeu
        :param depth: le nombre de récursions effectuées
        :return: le score
        """
        if game.getWinner() == self.player.getPlayerID():
            score = self.value + depth
        elif game.getWinner() == self.opponent.getPlayerID():
            score = -self.value - depth
        else:
            score = 0
        return score

    def findPossibleSourceMoves(self, board, maximize):
        """
        Méthode qui permet de trouver les pions jouables du joueur en fonction de maximize.  Si maximize faut True,
        on prend en considération les pions de l'Ai, sinon on considère à la place les pions de l'adversaire.
        :param board: plateau du jeu
        :param maximize:
        :return: les sources possibles des mouvements
        """
        possibleMoves = []
        if maximize:
            for sourcePos in self.player.getPosList():
                if Utils.checkPos(board, sourcePos, self.player.getPlayerID()):
                    possibleMoves.append(sourcePos)
        else:
            for sourcePos in self.opponent.getPosList():
                if Utils.checkPos(board, sourcePos, self.opponent.getPlayerID()):
                    possibleMoves.append(sourcePos)
        return possibleMoves

    def simulateMove(self, source, dest, game, maximize):
        """
        Méthode permettant de simuler un coup en mettant à jour le plateau du jeu ainsi que la liste des pions du
        joueur en fonction de maximize. Ensuite, il met à jour le gagnant du jeu s'il y en a un.
        :param source: source du coup
        :param dest: destination du coup
        :param game: état du jeu
        :param maximize:
        :return: le pion supprimé par le mouvement
        """
        if maximize:
            game.getBoard().updateBoard(source, dest, self.player)
            deletedPeg = self.player.updatePosList(source, dest, self.opponent.getPosList())

        else:
            game.getBoard().updateBoard(source, dest, self.opponent)
            deletedPeg = self.opponent.updatePosList(source, dest, self.player.getPosList())
        winPlayer1 = game.getBoard().detectWinner(game.player1, game.player2)
        winPlayer2 = game.getBoard().detectWinner(game.player2, game.player1)
        game.winner = winPlayer2 + winPlayer1
        return deletedPeg

    def undoMove(self, deletedPeg, maximize, source, dest, game):
        """
        méthode permettant de défaire un coup joué précédemment, en fonction de maximize. Si maximize vaut True, on
        considère les pions de l'AI, sinon, on considère ceux de l'adversaire. Si un pion a été supprimé précédemment,
        on le re rajoute à la liste des pions du joueur correspondant ainsi qu'au plateau du jeu.
        :param deletedPeg: pion supprimé précédemment
        :param maximize:
        :param source: source du coup
        :param dest: destination du coup
        :param game: état du jeu
        :return: aucun
        """
        if maximize:
            if deletedPeg:
                self.opponent.getPosList().append(deletedPeg)
                game.getBoard().updateBoard(dest, source, self.player, True)
            else:
                game.getBoard().updateBoard(dest, source, self.player, False)
            self.player.updatePosList(dest, source, self.opponent.getPosList())

        else:
            if deletedPeg:
                self.player.getPosList().append(deletedPeg)
                game.getBoard().updateBoard(dest, source, self.opponent, True)
            else:
                game.getBoard().updateBoard(dest, source, self.opponent, False)
            self.opponent.updatePosList(dest, source, self.player.getPosList())

        game.winner = game.getBoard().detectWinner(game.player1, game.player2)

    def findPossibleDestinationMoves(self, source, board, maximize):
        """
        Méthode permettant de trouver les destinations possibles pour une certaine source donnée en fonction de
        maximize.
        :param source: source du mouvement
        :param board:
        :param maximize:
        :return: la liste des destinations du mouvement possible
        """
        if maximize:
            if self.player.getPlayerID() == 1:
                return Utils.findMovePlayer1(board, source)
            elif self.player.getPlayerID() == 2:
                return Utils.findMovePlayer2(board, source)
        else:
            if self.opponent.getPlayerID() == 1:
                return Utils.findMovePlayer1(board, source)
            elif self.opponent.getPlayerID() == 2:
                return Utils.findMovePlayer2(board, source)
