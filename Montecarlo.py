import math
import random
import time
from operator import attrgetter

import Utils
import Board

# todo: fin de correction de l'AI
class GameState:
    # structure qui représente un état de jeu inclus dans un node
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
        self.generateRoute()

    def createTree(self):
        counter = self.findPossibleMovesAmount()
        timeout = time.time() + 1.5
        for i in range(counter):
            if time.time() >= timeout:
                break
            else:
                self.generateRoute()

    def findPossibleMovesAmount(self):
        counter = 0
        possibleSourceMoves = Utils.findBoardSources(self.gameState.board, self.gameState.player)
        for source in possibleSourceMoves:
            possibleDestinationMoves = Utils.findPossibleDestinations(source, self.gameState.board,
                                                                      self.gameState.player)
            counter += len(possibleDestinationMoves)
        return counter

    def createChild(self, board):
        winner = board.findWinner()
        gameState = GameState(board, self.gameState.opponent, self.gameState.player, winner)
        Node(gameState, self)

    def generateRoute(self):
        board = None
        possibleSourceMoves = Utils.findBoardSources(self.gameState.board, self.gameState.player)
        for source in possibleSourceMoves:
            possibleDestinationMoves = Utils.findPossibleDestinations(source, self.gameState.board,
                                                                      self.gameState.player)
            for destination in possibleDestinationMoves:
                board = self.simulateMove(destination, source)
                if board:
                    break
            if board:
                break
        if board and self.gameState.winner == 0:
            self.createChild(board)

    def simulateMove(self, destination, source):
        res = None
        deletedPeg = self.makeMove(source, destination)
        board = Board.Board(None, self.gameState.board.getBoard())
        if self.checkChildren(board):
            res = board
        self.undoMove(deletedPeg, source, destination)
        return res

    def checkChildren(self, board):
        if len(self.children) == 0:
            return True
        for child in self.children:
            if child.gameState.board.getBoard() == board.getBoard():
                return False
        return True

    def makeMove(self, source, dest):
        deletedPeg = self.gameState.board.updateBoard(source, dest, self.gameState.player)
        return deletedPeg

    def undoMove(self, deletedPeg, source, dest):

        if deletedPeg != 0:
            self.gameState.board.updateBoard(dest, source, self.gameState.player, True)
        else:
            self.gameState.board.updateBoard(dest, source, self.gameState.player, False)


class Tree:
    def __init__(self, player, game):
        self.playerID = player.getPlayerID()
        self.c = 1.4
        gameState = self.generateGameState(game)
        self.root = Node(gameState)
        self.root.createTree()
        self.searchTree(self.root)

    def generateGameState(self, game, winner=0):
        if self.playerID == 1:
            gameState = GameState(game.board, game.player1, game.player2, winner)
        else:
            gameState = GameState(game.board, game.player2, game.player1, winner)
        return gameState

    def setRoot(self, board, game):
        found = False
        for child in self.root.children:
            if child.gameState.board.getBoard() == board.getBoard():
                self.root = child
                self.root.createTree()
                found = True
        if not found:
            self.createNewRoot(board, game)

    def createNewRoot(self, board, game):
        winner = board.findWinner()
        gameState = self.generateGameState(game, winner)
        if winner != 2:
            node = Node(gameState)
            self.root = node
            self.root.createTree()
            if len(self.root.children) > 0:
                self.searchTree(self.root)

    def selectMove(self):
        if len(self.root.children) > 0:
            child = max(self.root.children, key=attrgetter('counter'))
            if child.gameState.board.getBoard() == self.root.gameState.board.getBoard():
                self.root = child
                child = max(self.root.children, key=attrgetter('counter'))
            move = Utils.findMove(self.root.gameState.board.getBoard(), child.gameState.board.getBoard())
            self.root = child
        else:
            move = None
        print(move)
        return move

    def searchTree(self, node):
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

    def simulation(self, node):
        path = []
        score = self.simulate(path, node)
        return score

    def simulate(self, path, node):
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

    def computeScore(self, node):
        if node.gameState.winner == self.playerID:
            node.simulationRes = 1000
        else:
            node.simulationRes = -1000
        return node.simulationRes

    def computeUTC(self, node):
        for child in node.children:
            div = math.log(node.counter) / child.counter
            child.UTC = (child.simulationRes / child.counter) + (self.c * math.sqrt(div))

    def choseChild(self, node):
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
