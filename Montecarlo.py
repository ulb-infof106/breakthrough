"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA INFO
"""
import math
import random
import time
from operator import attrgetter

import Utils
import Board


class GameState:
    """
    Structure représentant un état de jeu contenu dans un noeud
    """

    def __init__(self, board, player, opponent, winner=0):
        self.board = board
        self.player = player
        self.opponent = opponent
        self.winner = winner


class Node:
    """
    Classe représentant le noeud d'un arbre
    """

    def __init__(self, gameState, root=None):
        self.gameState = gameState
        self.children = []
        self.visited = False
        self.fullyDeveloped = False
        self.simulationRes = 0
        self.counter = 0
        self.UTC = 0

        if root:
            root.children.append(self)
        self.generateRoute()

    def findPossibleMovesAmount(self):
        """
        Méthode permettant de trouver le nombre de mouvements possibles à partir de l'état de jeu du noeud
        """
        counter = 0

        possibleSourceMoves = Utils.findBoardSources(self.gameState.board, self.gameState.player)
        for source in possibleSourceMoves:
            possibleDestinationMoves = Utils.findPossibleDestinations(source, self.gameState.board,
                                                                      self.gameState.player)
            counter += len(possibleDestinationMoves)
        return counter

    def createChild(self, board):
        """
        Méthode créant un enfant du noeud actuel : le joueur du noeud actuel deviendra l'adversaire du noeud fils
        et l'adversaire du noeud actuel deviendra le joueur du noeud fils. on crée un gameState pour le transmettre
        au noeud fils
        : param board : plateau qui sera dans le gamestate du noeud fils
        """
        winner = board.findWinner()
        gameState = GameState(board, self.gameState.opponent, self.gameState.player, winner)
        Node(gameState, self)

    def makeMove(self, source, dest):
        """
        Méthode permettant de mettre à jour le plateau du jeu en fonction d'une source et d'une destination
        : param source : source du mouvement
        : param dest : destination du mouvement
        : return : le pion mangé par ce mouvement
        """
        deletedPeg = self.gameState.board.updateBoard(source, dest, self.gameState.player)
        return deletedPeg

    def checkChildren(self, board):
        """
        Méthode qui permet de vérifier si un des fils du noeud actuel possède dans son gamestate le plateau recherché
        : param board : plateau à trouver dans les fils du noeud actuel
        : return : False si plateau trouvé, True sinon
        """
        if len(self.children) == 0:
            return True
        for child in self.children:
            if child.gameState.board.getBoard() == board.getBoard():
                return False
        return True

    def undoMove(self, deletedPeg, source, dest):
        """
        Méthode qui permet de "défaire" l'action d'une simulation en mettant à jour le tableau en fonction de si un
        pion a été mangé ou non
        : param deletedPeg : pion mangé
        : param source : source du mouvement précédemment effectué
        : param dest : destination du mouvement précédemment effectué
        """
        if deletedPeg != 0:
            self.gameState.board.updateBoard(dest, source, self.gameState.player, True)
        else:
            self.gameState.board.updateBoard(dest, source, self.gameState.player, False)

    def simulateMove(self, source, destination):
        """
        Méthode qui permet de simuler un mouvement et sauvegarder le plateau de jeu obtenu en ayant simulé ce coup
        pour le transmettre plus tard à un de ses fils
        : param destination : destination du mouvement
        : param source : source du mouvement
        : return : plateau pour lequel on créera un fils
        """
        res = None
        deletedPeg = self.makeMove(source, destination)
        board = Board.Board(None, self.gameState.board.getBoard())
        if self.checkChildren(board):
            res = board
        self.undoMove(deletedPeg, source, destination)
        return res

    def generateRoute(self):
        """
        Méthode qui permet de générer un chemin de racine à feuille. On s'arrête dès qu'on trouve un plateau pour
        lequel créer un fils.
        """
        board = None
        possibleSourceMoves = Utils.findBoardSources(self.gameState.board, self.gameState.player)
        for source in possibleSourceMoves:
            possibleDestinationMoves = Utils.findPossibleDestinations(source, self.gameState.board,
                                                                      self.gameState.player)
            for destination in possibleDestinationMoves:
                board = self.simulateMove(source, destination)
                if board:
                    break
            if board:
                break
        if board and self.gameState.winner == 0:
            self.createChild(board)

    def createTree(self, timer):
        """
        Méthode permettant de construire un arbre en un délai imparti
        : param timer : délai à partir duquel on limite le temps de création de l'arbre
        """
        counter = self.findPossibleMovesAmount()
        timeout = time.time() + timer * 0.75
        for i in range(counter):
            if time.time() >= timeout:
                break
            else:
                self.generateRoute()


class Tree:
    """
    Classe représentant l'arbre de Montecarlo, qui constitue l'IA
    """
    def __init__(self, player, game, timer):
        self.timer = timer
        self.playerID = player.getPlayerID()
        self.c = 1.4
        gameState = self.generateGameState(game)
        self.root = Node(gameState)
        self.root.createTree(self.timer)
        self.searchTree(self.root)

    def generateGameState(self, game, winner=0):
        """
        Méthode qui permet de générer un gameState pour le noeud actuel
        : param game : objet game représentant la partie
        : param winner : gagnant de la partie
        : return : le gameState généré
        """
        if self.playerID == 1:
            gameState = GameState(game.board, game.player1, game.player2, winner)
        else:
            gameState = GameState(game.board, game.player2, game.player1, winner)
        return gameState

    def generateChildGameState(self, game, winner):
        """
        Méthode qui permet de générer un gameState pour un noeud enfant
        : param game : objet game représentant la partie
        : param winner : gagnant de la partie
        : return : le gameState généré
        """
        if self.root.gameState.player.getPlayerID() == 1:
            gameState = GameState(game.board, game.player1, game.player2, winner)
        else:
            gameState = GameState(game.board, game.player2, game.player1, winner)
        return gameState

    def computeScore(self, node):
        """
        Méthode permettant de calculer le score qu'un noeud feuille aurait. Si le gagnant est l'ID de l'IA, le score
        est positif, sinon, le score est négatif.
        : param node : noeud duquel on calcule le score
        : return : le score obtenu pour ce noeud
        """
        if node.gameState.winner == self.playerID:
            node.simulationRes = 1000
        else:
            node.simulationRes = -1000
        return node.simulationRes

    def simulate(self, path, node):
        """
        Méthode récursive qui permet de se déplacer de plateau en plateau jusqu'à trouver un noeud feuille pour lequel
        on calcule le score obtenu
        : param path : liste des plateaux parcourus
        : param node : noeud à partir duquel on commence la simulation
        : return : le score obtenu
        """
        if node.gameState.winner > 0:
            node.counter += 1
            score = self.computeScore(node)
            return score
        else:
            child = random.choice(node.children)
            path.append(child)
            score = self.simulate(path, child)
            node.counter += 1
            node.simulationRes += score
            return score

    def simulation(self, node):
        """
        Méthode appelante de la méthode récursive simulate
        : param node : noeud sur lequel la simulation s'applique
        """
        path = []
        score = self.simulate(path, node)
        return score

    def computeUTC(self, node):
        """
        Méthode qui permet de calculer l'UTC d'un noeud.
        : param node : noeud pour lequel on calcule l'UTC
        """
        for child in node.children:
            div = math.log(node.counter) / child.counter
            child.UTC = (child.simulationRes / child.counter) + (self.c * math.sqrt(div))

    def choseChild(self, node):
        """
        Méthode permettant de choisir l'enfant sur lequel on effectuera la simulation prochaine, c'est-à-dire méthode
        qui choisit l'enfant qui a le meilleur UTC et qui n'est pas totalement développé
        : param Node : noeud pour lequel on cherche le successeur à la simulation
        : return : enfant sur lequel la simulation prochaine s'effectuera
        """
        res = None
        maximum = -1000
        if len(node.children) > 0:
            for child in node.children:
                if child.UTC >= maximum:
                    if not child.fullyDeveloped:
                        maximum = child.UTC
                        res = child
                    else:
                        res = self.choseChild(child)
        return res

    def searchTree(self, node):
        """
        Méthode récursive qui permet de parcourir les noeuds et d'effectuer une simulation sur les fils des noeuds, en
        fonction qu'ils soient visités ou totalement dévelopés. Après le for se déroule les étapes de la rétro
        propagation.
        : param node : noeud à partir duquel on effectue la recherche
        """
        for child in node.children:
            if not child.visited:
                node.counter += 1
                score = self.simulation(child)
                node.simulationRes += score
                child.visited = True
        node.fullyDeveloped = True
        self.computeUTC(node)
        child = self.choseChild(self.root)
        if len(child.children) > 0:
            self.searchTree(child)

    def createNewRoot(self, board, game):
        """
        Méthode permettant de créer une nouvelle racine s'il n'existe pas de noeud contenant le plateau correspondant
        à l'état de jeu actuel. On construit ensuite un nouveau sous-arbre à partir de cette racine, puis on lui fait
        subir un searchTree.
        : param board : plateau correspondant à l'état actuel du jeu
        : param game : instance de game correspondant à l'état de la partie
        """
        winner = board.findWinner()
        gameState = self.generateChildGameState(game, winner)
        if winner != 2:
            node = Node(gameState)
            self.root = node
            self.root.createTree(self.timer)
            if len(self.root.children) > 0:
                self.searchTree(self.root)

    def setRoot(self, board, game):
        """
        Méthode recherchant dans les fils de la racine s'il existe un fils ayant dans son gameState le plateau
        correspondant à l'état de jeu actuel. S'il en trouve un, ce dernier devient la nouvelle racine, sinon, une
        nouvelle racine est créée.
        : param board : plateau correspondant à l'état actuel du jeu
        : param game : instance de game correspondant à l'état de la partie
        """
        found = False
        for child in self.root.children:
            if child.gameState.board.getBoard() == board.getBoard():
                self.root = child
                self.root.createTree(self.timer)
                found = True
        if not found:
            self.createNewRoot(board, game)

    def selectMove(self):
        """
        Méthode permettant de choisir un mouvement, c'est-à-dire de choisir le mouvement menant à  l'état de jeu qui a
        été le plus visité lors des simulations et du searchTree.
        : return : mouvement trouvé
        """
        if len(self.root.children) > 0:
            child = max(self.root.children, key=attrgetter('counter'))
            if child.gameState.board.getBoard() == self.root.gameState.board.getBoard():
                self.root = child
                child = max(self.root.children, key=attrgetter('counter'))
            move = Utils.findMove(self.root.gameState.board.getBoard(), child.gameState.board.getBoard(), self.playerID)
            self.root = child
        else:
            move = None
        return move
