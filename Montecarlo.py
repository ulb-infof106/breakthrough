# étape 1: construire l'arbre de la partie
import sys

import Utils
import Board
import Game


class Node:
    # représente un état de jeu
    def __init__(self, board, player, opponent):
        self.board = board
        self.children = []
        self.player = player
        self.opponent = opponent

    def setChildren(self):
        childrenBoards = self.findChildrenBoards()

        for board in childrenBoards:
            noeud = Node(board, self.opponent, self.player)
            self.children.append(noeud)

    def findChildrenBoards(self):
        childrenBoards = []
        possibleSourceMoves = Utils.findPossibleSources(self.board, self.player)
        for source in possibleSourceMoves:
            possibleDestinationMoves = Utils.findPossibleDestinations(source, self.board, self.player)
            for destination in possibleDestinationMoves:
                deletedPeg = self.simulateMove(source, destination)
                board = Board.Board(None, self.board.getBoard())
                childrenBoards.append(board)
                self.undoMove(deletedPeg, source, destination)
        return childrenBoards

    def simulateMove(self, source, dest):
        self.board.updateBoard(source, dest, self.player)
        deletedPeg = self.player.updatePosList(source, dest, self.opponent.getPosList())
        winPlayer1 = self.board.detectWinner(self.player, self.opponent)
        winPlayer2 = self.board.detectWinner(self.opponent, self.player)
        # game.winner = winPlayer2 + winPlayer1
        return deletedPeg

    def undoMove(self, deletedPeg, source, dest):

        if deletedPeg:
            self.opponent.getPosList().append(deletedPeg)
            self.board.updateBoard(dest, source, self.player, True)
        else:
            self.board.updateBoard(dest, source, self.player, False)
        self.player.updatePosList(dest, source, self.opponent.getPosList())
        # game.winner = game.getBoard().detectWinner(game.player1, game.player2)


class Tree:
    def __init__(self, game):
        self.root = Node(game.board, game.player1, game.player2)


boardGame = Board.Board(sys.argv[1])
startGame = Game.Game("Humain", "Humain", boardGame)
monteCarlo = Tree(startGame)
monteCarlo.root.setChildren()
for child in monteCarlo.root.children:
    print(child.board.getBoard())
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
#    aucune simulation n'a encore été faire --> aucun fils de la racine n'est visité.
#    On effectue une simulation sur tous les fils : 3 simulations on choisit des noeuds intermédiaires aléatoires et on
#    s'arrête à un noeud terminal
#    les résultats de ces 3 simulations sont propagés jusqu'à la racine
#    le noeud racine est alors complètemennt développé
