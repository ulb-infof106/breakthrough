"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA INFO
"""

import Player
import Move
import Montecarlo
import Utils


class Game:
    """
    Classe qui représente l'état de la partie
    """

    def __init__(self, player1, player2, board, timer):
        """
        Constructeur de la classe représentant l'état de la partie. On commence par initialiser un plateau via un
        fichier, et on crée des instances de 2 joueurs, puis celle de l'IA qui correspondra à un joueur.
        """
        self.winner = 0
        self.board = board
        self.player1 = Player.Player(1, self.board)
        self.player2 = Player.Player(2, self.board)
        self.chooseGameMode(player1, player2, timer)

    def chooseGameMode(self, player1, player2, timer):
        if player1 == "Humain":
            if player2 == "Minimax":
                self.IA = Montecarlo.Tree(self.player2, self, timer)
        else:
            if player2 == "Humain":
                self.IA = Montecarlo.Tree(self.player1, self, timer)
            else:
                self.IA1 = Montecarlo.Tree(self.player1, self, timer)
                self.IA2 = Montecarlo.Tree(self.player2, self, timer)

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
        """
        wonPlayer1 = self.board.detectWinner(self.player1, self.player2)
        wonPlayer2 = self.board.detectWinner(self.player2, self.player1)
        self.winner = wonPlayer1 + wonPlayer2

    def getMovablePegs(self, currentPlayer):
        """
        Méthode qui permet de trouver les sources de mouvements possibles pour un certain joueur en fonction de sa
        couleur.
        : param currentPlayer : couleur du joueur actuel
        : return : liste des sources de mouvements possibles
        """
        if currentPlayer == "white":
            return Utils.findPossibleSources(self.board, self.player1)
        else:
            return Utils.findPossibleSources(self.board, self.player2)

    def getPossibleDestinations(self, currentPlayer, pos):
        """
        Méthode qui permet de trouver les destinations de mouvements possibles pour un certain joueur en fonction de sa
        couleur et d'une source donnée.
        : param currentPlayer : couleur du joueur actuel
        : param pos : source de mouvement donnée
        : return : liste des destinations de mouvements possibles
        """
        if currentPlayer == "white":
            return Utils.findPossibleDestinations(pos, self.board, self.player1)
        else:
            return Utils.findPossibleDestinations(pos, self.board, self.player2)

    def getPlayers(self, currentPlayer):
        """
        Méthode permettant de récupérer les joueurs de la partie en fonction de la couleur du joueur actuel
        : param currentPlayer : couleur du joueur actuel
        : return : 2 objets de la classe player
        """
        if currentPlayer == "white":
            return self.player1, self.player2
        else:
            return self.player2, self.player1

    def makeMove(self, currentPlayer, source, destination):
        """
        Méthode qui permet de créer un objet mouvement en fonction d'un joueur et d'une source et destination de
        mouvement. Si ce mouvement est correct, on met à jour le plateau de jeu en fonction.
        : param currentPlayer : joueur qui joue actuellement
        : param source : source du mouvement
        : param destination : destination du mouvement
        : return : True si le mouvement est correct, False sinon
        """
        currentPlayer, nextPlayer = self.getPlayers(currentPlayer)
        move = Move.Move(currentPlayer, source, destination)
        if self.checkDiagonalMove(currentPlayer, move.getSource(), move.getDestination()) and self.checkForwardMove(
                currentPlayer, move.getSource(), move.getDestination()):
            currentPlayer.updatePosList(move.getSource(), move.getDestination(), nextPlayer.getPosList())
            self.board.updateBoard(move.getSource(), move.getDestination(), currentPlayer)
            return True
        return False

    def getWinner(self):
        """
        Getter retournant le gagnant de la partie
        """
        self.detectWin()
        return self.winner
