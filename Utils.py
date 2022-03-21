"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA3 INFO
"""
import random

"""
Fichier contenant des fonctions utilitaires
"""


def checkPos(board, move, playerID):
    """
    Fonction qui vérifie qu'au moins un mouvement est faisable sur cette position en fct du joueur en appelant
    d'autres fonctions
    :param playerID:
    :param board: plateau du jeu
    :param move: mouvement choisi
    :return:
    """
    if board.getBoard()[move[0]][move[1]] == playerID and playerID == 1:
        return checkPosPlayer1(board, move)
    if board.getBoard()[move[0]][move[1]] == playerID and playerID == 2:
        return checkPosPlayer2(board, move)


def checkPosPlayer1(board, source):
    """
    Fonction qui vérifie que la position du joueur 1 permet d'effectuer un mouvement quelconque
    :param board: plateau du jeu
    :param source: position du pion pour lequel il faut trouver un mouvement
    :return: True dès qu'un mouvement potentiel a été détecté, False si n'a rien trouvé
    """
    if board.getBoard()[source[0] - 1][source[1]] == 0:
        # alors on peut faire un mouvement vertical
        return True
    try:
        target = board.getBoard()[source[0] - 1][source[1] - 1]
        if target != 1:
            return True
    except IndexError:
        return False
    try:
        target = board.getBoard()[source[0] - 1][source[1] + 1]
        if target != 1:
            return True
    except IndexError:
        return False
    return False


def checkPosPlayer2(board, source):
    """
    Fonction qui vérifie que la position du joueur 2 permet d'effectuer un mouvement quelconque
    :param board: plateau du jeu
    :param source: position du pion pour lequel il faut trouver un mouvement
    :return: True dès qu'un mouvement potentiel a été détecté, False si n'a rien trouvé
    """

    if board.getBoard()[source[0] + 1][source[1]] == 0:
        # alors on peut faire un mouvement vertical
        return True
    try:
        target = board.getBoard()[source[0] + 1][source[1] - 1]
        if target != 2:
            return True
    except IndexError:
        return False
    try:
        target = board.getBoard()[source[0] + 1][source[1] + 1]
        if target != 2:
            return True
    except IndexError:
        return False
    return False


def manhattanCalculation(currentPos, possiblePegs):
    """
    Fonction qui permet de calculer la distance manhattan entre 2 positions
    :param currentPos: position initiale du pion
    :param possiblePegs: pions qu'on peut potentiellement sélectionner
    :return: le pion sélectionnable qui a la plus petite distance manhattan avec le pion initial
    """
    res = -1
    pos = -1
    for i in range(len(possiblePegs)):
        manhattan = abs(currentPos[0] - possiblePegs[i][0]) + abs(currentPos[1] - possiblePegs[i][1])
        if res == -1 or manhattan < res:
            res = manhattan
            pos += 1
    return possiblePegs[pos]


def findMovePlayer2(board, source):
    """
    Fonction qui permet de trouver un mouvement faisable pour une certaine source donnée.
    :param board: plateau du jeu
    :param source: source du mouvement
    :return:
    """
    possibleMoves = []
    if board.getBoard()[source[0] + 1][source[1]] == 0:
        # alors on peut faire un mouvement vertical
        possibleMoves.append([source[0] + 1, source[1]])
    try:
        target = board.getBoard()[source[0] + 1][source[1] - 1]
        if target != 2:
            possibleMoves.append([source[0] + 1, source[1] - 1])
    except IndexError:
        pass
    try:
        target = board.getBoard()[source[0] + 1][source[1] + 1]
        if target != 2:
            possibleMoves.append([source[0] + 1, source[1] + 1])
    except IndexError:
        pass
    return possibleMoves


def chooseMove(best_actions):
    """
    Méthode qui permet de choisir un mouvement parmi tous ceux possibles, en fonction du score
    :param best_actions:
    :return: le mouvement trouvé s'il existe, None sinon
    """
    if len(best_actions) == 0:
        return None
    if type(best_actions[0]) == int:
        return best_actions
    try:
        move = best_actions[random.randint(0, len(best_actions) - 1)]
        return move
    except IndexError:
        return


def findMovePlayer1(board, source):
    """
    Fonction qui permet de trouver un mouvement faisable pour une certaine source donnée.
    :param board: plateau du jeu
    :param source: source du mouvement
    :return: la liste des destinations de mouvement possibles
    """
    possibleMoves = []
    if board.getBoard()[source[0] - 1][source[1]] == 0:
        # alors on peut faire un mouvement vertical
        possibleMoves.append([source[0] - 1, source[1]])
    try:
        target = board.getBoard()[source[0] - 1][source[1] - 1]
        if target != 1:
            possibleMoves.append([source[0] - 1, source[1] - 1])
    except IndexError:
        pass
    try:
        target = board.getBoard()[source[0] - 1][source[1] + 1]
        if target != 1:
            possibleMoves.append([source[0] - 1, source[1] + 1])
    except IndexError:
        pass
    return possibleMoves


def findBestScore(maximize):
    """
    Méthode qui permet d'initialiser le meilleur score en fonction de maximize
    :param maximize:
    :return: le meilleur score
    """
    if maximize:
        best_score = float('-inf')
    else:
        best_score = float('inf')
    return best_score


def isBetter(score, best_score, maximize):
    """
    Méthode qui permet de déterminer si le score trouvé est meilleur que le meilleur score
    :param score: score trouvé
    :param best_score: meilleur score précédent
    :param maximize:
    :return: True si score est meilleur que best_score, False sinon.
    """
    if maximize:
        if score > best_score:
            return True
    else:
        if score < best_score:
            return True
    return False


def convertPosToInt(str_pos, board):
    """
    Fonction qui permet d'extraire une position,donc de traduire en coordonnées matricielles les coordonnées entrées
    par le joueur
    :param board:
    :param str_pos: position à traduire
    :return: les coordonnées matricielles de la position
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    literalCoord = str_pos[0]
    numericCoord = str_pos[1:]
    i = -(int(numericCoord) - board.getlineDimension())
    j = alphabet.index(literalCoord)
    return [i, j]

def extractPosition(n, str_pos):
    """
    Fonction qui permet d'extraire une position,donc de traduire en coordonnées matricielles les coordonnées entrées
    par le joueur
    :param n: taille du plateau
    :param str_pos: position à traduire
    :return: les coordonnées matricielles de la position
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    literalCoord = str_pos[0]
    numericCoord = str_pos[1:]
    i = -(int(numericCoord) - n)
    j = alphabet.index(literalCoord)
    return i, j


def inputUser(board):
    """
    Méthode qui prend l'input du joueur. Ce dernier fournira l'emplacement en langage plateau où il voudra poser
    son pion. S'il donne une mauvaise coordonnée, on lui redemande un input jusqu'à ce qu'il soit correct.
    :param board:
    :return:
    """
    validMove = False
    move = input("Veuillez sélectionner une case où placer votre pion: ")
    while not validMove:
        try:

            moveInt = convertPosToInt(move, board)
            try:
                target = board.getBoard()[moveInt[0]][moveInt[1]]
                return moveInt
            except IndexError:
                print("Veuillez entrer des coordonnées qui se trouvent dans le plateau")
                move = input("Veuillez sélectionner une case où placer votre pion: ")
        except ValueError:
            print("Veuillez respecter les règles d'encodage")
            move = input("Veuillez sélectionner une case où placer votre pion: ")
