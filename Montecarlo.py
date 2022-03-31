 # question : si plusieurs noeuds ont la même valeur UTC, itérer sur tous les noeuds de même valeur?
import math
import random
import sys

import Utils
import Board
import Game


class GameState:
    # représente un état de jeu inclus dans un node
    def __init__(self, board, player, opponent, winner=0):
        self.board = board
        self.player = player
        self.opponent = opponent
        self.winner = winner

class Node:
    # représente un état de jeu
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
        if self.gameState.winner == 0:
            self.setChildren()

    def setChildren(self):
        childrenBoards = self.findChildrenBoards()
        if len(childrenBoards) != 0:
            for board in childrenBoards:
                winner = board.findWinner()
                gameState = GameState(board, self.gameState.opponent, self.gameState.player, winner)
                Node(gameState, self)

    def findChildrenBoards(self):
        childrenBoards = []
        possibleSourceMoves = Utils.findBoardSources(self.gameState.board, self.gameState.player)
        for source in possibleSourceMoves:
            possibleDestinationMoves = Utils.findPossibleDestinations(source, self.gameState.board, self.gameState.player)
            for destination in possibleDestinationMoves:
                self.simulateMove(childrenBoards, destination, source)
        return childrenBoards

    def simulateMove(self, childrenBoards, destination, source):
        deletedPeg = self.makeMove(source, destination)
        board = Board.Board(None, self.gameState.board.getBoard())
        childrenBoards.append(board)
        self.undoMove(deletedPeg, source, destination)

    def makeMove(self, source, dest):
        deletedPeg = self.gameState.board.updateBoard(source, dest, self.gameState.player)
        return deletedPeg

    def undoMove(self, deletedPeg, source, dest):

        if deletedPeg != 0:
            self.gameState.board.updateBoard(dest, source, self.gameState.player, True)
        else:
            self.gameState.board.updateBoard(dest, source, self.gameState.player, False)


class Tree:
    def __init__(self, game):
        self.playerID = 1
        self.c = 1.4
        # get playerID with game later
        gameState = GameState(game.board, game.player1, game.player2)

        self.root = Node(gameState)
        for child in self.root.children:
            if not child.visited:
                self.root.counter += 1
                self.simulation(child)
                child.visited = True
        self.root.fullyDeveloped = True
        self.computeUTC(self.root)
        child = self.choseChild(self.root)
        # appel récursif: la simulation recommence sur child

    def simulation(self, node):
        path = []
        self.simulate(path, node)

    def simulate(self, path, node):
        if node.gameState.winner > 0:
            score = self.computeScore(node)
            return score
        else:
            child = random.choice(node.children)
            path.append(child)
            score = self.simulate(path, child)
            node.counter += 1
            node.simulationRes += score
            return score

    def computeScore(self, node):
        if node.gameState.winner == self.playerID:
            node.simulationRes = 1000
        else:
            node.simulationRes = -1000
        return node.simulationRes

    def computeUTC(self, node):
        for child in node.children:
            div = math.log(node.counter)/child.counter
            child.UTC = (child.simulationRes / child.counter) + (self.c * math.sqrt(div))

    def choseChild(self, node):
        res = None
        max = -1000
        if len(node.children) > 0:
            for child in node.children:
                if child.UTC >= max:
                    if not child.fullyDeveloped:
                        max = child.UTC
                        res = child
                    else:
                        res = self.choseChild(child)
        return res

    def printLeafs(self, root):
        for child in root.children:
            if child.gameState.winner != 0:
                child.gameState.board.printBoard()
            else:
                self.printLeafs(child)

    def printTree(self, root):
        for child in root.children:
            print(child.simulationRes)
            self.printTree(child)


boardGame = Board.Board(sys.argv[1])
startGame = Game.Game("Humain", "Humain", boardGame)
monteCarlo = Tree(startGame)

# informations sur les noeuds:
# - après rétropropagation, le noeud d'où la simulation a démarré est marqué comme visité
# - 2 statistiques pour un noeud v:
#   -somme des résultats des simulations rétropropagés à travers le noeud v (Q(v))
#   -compteur du nombre de fois que le noeud v s’est retrouvé sur la traversée inverse d’une rétropropagation (N(v))
# En d’autres termes, Q(v) reflète à quel point le noeud v est prometteur tandis que N(v) reflète à quel point le noeud
# v a été exploré. grand Q(v) représente coup intéressant à exploiter. petit N(v) intéressant car coup peu exploré
# ces statistiques sont mises à jour lors de la rétropropagation
# - ces statistiques permettent de calculer l'UTC dont la formule est:
# Q(vi)/ N(vi) + c*sqrt(ln(N(v))/N(vi)) où vi est un des noeuds internes visités, v le noeud source(ou actuel) et c =1.4
# - quand un noeud est totalement développé, on choisit le fils ayant le meilleur UTC pour commencer la prochaine
# simulation
# - si ce fils est lui même complètement développé, on choisit le meilleur utc parmi ses fils et ainsi de suite

# informations sur l'arbre:
# - arbre m-aire
# - rollout policy function qui prend en paramètre un état du jeu (noeud) et retourne le prochain coup à jouer.
# - une simulation commence toujours au noeud qui n’a pas encore été visité précédemment
# - quand une simulation se termine, le résultat est rétropropagé jusqu'à la racine
# - la rétropropagation met à jour les statistiques des noeuds intermédiaires par lesquels elle passe
# - fin de recherche: le meilleur coup est celui qui a été visité le + (donc max(N(vi)))

# définitions importantes:
# - noeud visité: au moins une simulation a déjà commencé en ce noeud
# - noeud totalement développé: tous les enfants du noeud ont été visités
# - noeud actuel : état du jeu actuel
# - noeud terminal : noeud où la partie se termine
# - traversée : chemin  (aléatoire) d’un noeud actuel vers un autre noeud qui n’est pas encore totallement développé
# - recherche :ensemble de traversées dans l’arbre de jeu
# - simulation: séquence de coups qui commence au noeud actuel et qui se termine à un noeud terminal
# - un résultat peut être attribué à la simulation
# - rétropropagation: traversée inverse qui commence du noeud terminal et qui remonte
# jusqu’au noeud racine de l’arbre de jeu courant en passant par tous les noeuds intermédiaires

# premier traitement:
#    aucune simulation n'a encore été faite --> aucun fils de la racine n'est visité.
#    On effectue une simulation sur tous les fils : 3 simulations on choisit des noeuds intermédiaires aléatoires et on
#    s'arrête à un noeud terminal
#    les résultats de ces 3 simulations sont propagés jusqu'à la racine
#    le noeud racine est alors complètemennt développé
