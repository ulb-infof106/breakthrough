"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA3 INFO
"""

import Player
import Move
import IA
import Utils


class Game:
    """
    Classe qui représente l'état de la partie
    """

    def __init__(self, player1, player2, board):
        """
        Constructeur de la classe représentant l'état de la partie. On commence par initialiser un plateau via un
        fichier, et on crée des instances de 2 joueurs, puis celle de l'IA qui correspondra à un joueur.
        """
        self.winner = 0
        self.board = board
        self.player1 = Player.Player(1, self.board)
        self.player2 = Player.Player(2, self.board)
        self.chooseGameMode(player1, player2)

    def chooseGameMode(self, player1, player2):
        if player1 == "Humain":
            if player2 != "Humain":
                self.IA = IA.IA(self.player2, self)
        else:
            if player2 == "Humain":
                self.IA = IA.IA(self.player1, self)
            else:
                self.IA1 = IA.IA(self.player1, self)
                self.IA2 = IA.IA(self.player2, self)

    def getBoard(self):
        """
        Getter qui renvoie le plateau du jeu
        : return : Le plateau du jeu
        """
        return self.board

    def checkForwardMove(self, player, sourcePos, destinationPos):
        """
        Méthode qui vérifie que le mouvement "tout droit" du joueur est correct
        : param player : joueur actuel
        : param destinationPos : position de destination
        : param sourcePos : position source
        : return : true si mouvement correct, false sinon
        """

        if (sourcePos[1] == destinationPos[1] and self.board.getBoard()[destinationPos[0]][destinationPos[1]] != 0) or \
                abs(sourcePos[0] - destinationPos[0]) != 1:
            # si le joueur essaye de poser son pion à un emplacement pas libre tout en avançant ou essaye de se déplacer
            # de plus de 2 cases
            return False
        if (player.getPlayerID() == 1 and destinationPos[0] > sourcePos[0]) or (
                player.getPlayerID() == 2 and destinationPos[0] < sourcePos[0]):
            # si le joueur essaye de reculer
            return False
        return True

    def checkDiagonalMove(self, player, sourcePos, destinationPos):
        """
        Méthode qui vérifie que le mouvement en diagonale du joueur est correct
        : param player : joueur actuel
        : param destinationPos : position de destination
        : param sourcePos : position source
        : return : true si mouvement correct, false sinon
        """
        if player.getPlayerID() == 2 and destinationPos[1] != sourcePos[1] and (not destinationPos[0] > sourcePos[0]):
            # si le joueur essaye de se déplacer latéralement ou vers les diagonales arrière
            return False
        if player.getPlayerID() == 1 and destinationPos[1] != sourcePos[1] and (not destinationPos[0] < sourcePos[0]):
            return False
        if player.getPlayerID() == 2 and destinationPos[1] != sourcePos[1] and destinationPos[0] > sourcePos[0] and \
                self.board.getBoard()[destinationPos[0]][destinationPos[1]] == 2:
            # si le joueur essaye de faire un mouvement diagonal où il y a déjà un de ses pions
            return False
        if player.getPlayerID() == 1 and destinationPos[1] != sourcePos[1] and destinationPos[0] < sourcePos[0] and \
                self.board.getBoard()[destinationPos[0]][destinationPos[1]] == 1:
            return False
        if abs(destinationPos[1] - sourcePos[1]) > 1:
            # si le joueur essaye de faire un mouvement diagonal trop éloigné
            return False
        return True

    def detectWin(self):
        """
        Méthode qui permet de détecter si le coup venant d'être joué fait gagner un des joueurs.
        : return : aucun
        """
        wonPlayer1 = self.board.detectWinner(self.player1, self.player2)
        wonPlayer2 = self.board.detectWinner(self.player2, self.player1)
        self.winner = wonPlayer1 + wonPlayer2

    def getMovablePegs(self, currentPlayer):
        if currentPlayer == "white":
            return Utils.findPossibleSources(self.board, self.player1)
        else:
            return Utils.findPossibleSources(self.board, self.player2)

    def getPossibleDestinations(self, currentPlayer, pos):
        # on envoie une pos et on veut obtenir tous les mouvements possibles pour cette pos
        if currentPlayer == "white":
            return Utils.findPossibleDestinations(pos, self.board, self.player1)
        else:
            return Utils.findPossibleDestinations(pos, self.board, self.player2)

    def makeMove(self, currentPlayer, source, destination):
        currentPlayer, nextPlayer = self.getPlayers(currentPlayer)
        move = Move.Move(currentPlayer, source, destination)
        if self.checkDiagonalMove(currentPlayer, move.getSource(), move.getDestination()) and self.checkForwardMove(
                currentPlayer, move.getSource(), move.getDestination()):
            currentPlayer.updatePosList(move.getSource(), move.getDestination(), nextPlayer.getPosList())
            self.board.updateBoard(move.getSource(), move.getDestination(), currentPlayer)
            return True
        return False

    def getWinner(self):
        self.detectWin()
        return self.winner

    def getPlayers(self, currentPlayer):
        if currentPlayer == "white":
            return self.player1, self.player2
        else:
            return self.player2, self.player1
