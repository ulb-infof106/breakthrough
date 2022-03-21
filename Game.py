"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA3 INFO
"""

import sys
import Board
import Player
import Move
import IA


class Game:
    """
    Classe qui représente l'état de la partie
    """

    def __init__(self, player1, player2, delay, board):
        """
        Constructeur de la classe représentant l'état de la partie. On commence par initialiser un plateau via un
        fichier, et on crée des insiances de 2 joueurs, puis celle de l'IA qui correspondra à un joueur.
        """
        self.winner = 0
        self.board = board
        self.player1 = Player.Player(1, self.board)
        self.player2 = Player.Player(2, self.board)
        self.chooseGameMode(player1, player2, delay)

    def chooseGameMode(self, player1, player2, delay):
        if player1 == "Humain":
            if player2 != "Humain":
                self.IA = IA.IA(self.player2, self)
                self.delay = delay
                # self.humainVSAi(self.player1, self.player2)
        else:
            if player2 == "Humain":
                self.IA = IA.IA(self.player1, self)
                self.delay = delay
                # lancer AI vs humain
                pass
            else:
                self.IA1 = IA.IA(self.player1, self)
                self.IA2 = IA.IA(self.player2, self)
                self.delay = delay
                # lancer AI vs AI
                pass

    def getBoard(self):
        """
        getter qui renvoie le plateau du jeu
        :return: Le plateau du jeu
        """
        return self.board

    def getWinner(self):
        """
        Getter qui renvoie le gagnant du jeu
        :return: Le gagnant de la partie
        """
        return self.winner

    def checkForwardMove(self, player, sourcePos, destinationPos):
        """
        Méthode qui vérifie que le mouvement "tout droit" du joueur est correct
        :param player: joueur actuel
        :param destinationPos: position de destination
        :param sourcePos: position source
        :return: true si mouvement correct, false sinon
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
        :param player: joueur actuel
        :param destinationPos: position de destination
        :param sourcePos: position source
        :return: true si mouvement correct, false sinon
        """
        if player.getPlayerID() == 2 and destinationPos[1] != sourcePos[1] and (not destinationPos[0] > sourcePos[0]):
            # si le joueur essaye de se déplacer latéralement ou vers les diagonales arrières
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
        :return: aucun
        """
        wonPlayer1 = self.board.detectWinner(self.player1, self.player2)
        wonPlayer2 = self.board.detectWinner(self.player2, self.player1)
        self.winner = wonPlayer1 + wonPlayer2
        if self.winner == 1:
            print("Le joueur blanc a gagné")
            self.board.printBoard()
        elif self.winner == 2:
            print("Le joueur noir a gagné")
            self.board.printBoard()

    def humainVSAi(self, currentPlayer, nextPlayer):
        """
        Joueur 1 est humain, joueur 2 est AI
        Méthode récursive qui permet de jouer la partie. On commence par demander un mouvement au joueur, puis on le
        vérifie. S'il est correct, on met à jour la liste de ses pions , le plateau du jeu et on fait jouer l'AI.
        Ensuite, on détecte si un des joueurs a gagné la partie. Si non, la méthode est rappelée.
        :return:
        """
        move = Move.Move(currentPlayer, self.board)
        if self.checkDiagonalMove(currentPlayer, move.getSource(), move.getDestination()) and self.checkForwardMove(
                currentPlayer, move.getSource(), move.getDestination()):
            currentPlayer.updatePosList(move.getSource(), move.getDestination(), nextPlayer.getPosList())
            self.board.updateBoard(move.getSource(), move.getDestination(), currentPlayer)

            self.detectWin()
            if self.winner == 0:
                try:
                    self.IA.play(self)
                    self.humainVSAi(currentPlayer, nextPlayer)
                except AttributeError:  # si ai == None, on va obtenur une attribute error
                    self.humainVSAi(nextPlayer, currentPlayer)

        else:
            print("Veuillez entrer une coordonnée valide:")
            self.humainVSAi(currentPlayer, nextPlayer)

    def getMovablePegs(self, currentPlayer):
        if currentPlayer == "white":
            move = Move.Move(self.player1, self.board)
            return move.possibleSources
        else:
            move = Move.Move(self.player2, self.board)
            return move.possibleSources

    def getPossibleMoves(self, currentPlayer, pos):
        #on envoie une pos et on veut obtenir tous les mouvements possibles pour cette pos
        pass