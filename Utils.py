"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA INFO
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QMessageBox

"""
Fichier contenant des fonctions utilitaires
"""


def checkPos(board, move, playerID):
    """
    Fonction qui vérifie qu'au moins un mouvement est faisable sur cette position en fct du joueur en appelant
    d'autres fonctions
    :param playerID:
    :param board : plateau du jeu
    :param move : mouvement choisi
    :return:
    """

    if board.getBoard()[move[0]][move[1]] == playerID and playerID == 1:
        return checkPosPlayer1(board, move)
    if board.getBoard()[move[0]][move[1]] == playerID and playerID == 2:
        return checkPosPlayer2(board, move)


def checkPosPlayer1(board, source):
    """
    Fonction qui vérifie que la position du joueur 1 permet d'effectuer un mouvement quelconque
    :param board : plateau du jeu
    :param source : position du pion pour lequel il faut trouver un mouvement
    :return : True dès qu'un mouvement potentiel a été détecté, False si n'a rien trouvé
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
    :param board : plateau du jeu
    :param source : position du pion pour lequel il faut trouver un mouvement
    :return : True dès qu'un mouvement potentiel a été détecté, False si n'a rien trouvé
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


def findMovePlayer1(board, source):
    """
        Fonction qui permet de trouver un mouvement faisable pour une certaine source donnée.
        :param board : plateau du jeu
        :param source : source du mouvement
        :return :
    """
    possibleMoves = []
    if board.getBoard()[source[0] - 1][source[1]] == 0:
        # alors on peut faire un mouvement vertical
        possibleMoves.append([source[0] - 1, source[1]])
    if source[1] > 0:
        if board.getBoard()[source[0] - 1][source[1] - 1] != 1:
            # alors on peut faire un mouvement diagonal gauche
            possibleMoves.append([source[0] - 1, source[1] - 1])
    if source[1] < board.getColumnDimension() - 1:

        if board.getBoard()[source[0] - 1][source[1] + 1] != 1:
            # alors on peut faire un mouvement diagonal droit
            possibleMoves.append([source[0] - 1, source[1] + 1])
    return possibleMoves


def findMovePlayer2(board, source):
    """
        Fonction qui permet de trouver un mouvement faisable pour une certaine source donnée.
        :param board : plateau du jeu
        :param source : source du mouvement
        :return :
    """
    possibleMoves = []
    if board.getBoard()[source[0] + 1][source[1]] == 0:
        # alors on peut faire un mouvement vertical
        possibleMoves.append([source[0] + 1, source[1]])
    if source[1] > 0:
        if board.getBoard()[source[0] + 1][source[1] - 1] != 2:
            # alors on peut faire un mouvement diagonal gauche
            possibleMoves.append([source[0] + 1, source[1] - 1])
    if source[1] < board.getColumnDimension() - 1:
        if board.getBoard()[source[0] + 1][source[1] + 1] != 2:
            # alors on peut faire un mouvement diagonal droit
            possibleMoves.append([source[0] + 1, source[1] + 1])
    return possibleMoves


def extractPosition(n, str_pos):
    """
    Fonction qui permet d'extraire une position, donc de traduire en coordonnées matricielles les coordonnées entrées
    par le joueur
    :param n : taille du plateau
    :param str_pos : position à traduire
    :return : les coordonnées matricielles de la position
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    literalCoord = str_pos[0]
    numericCoord = str_pos[1:]
    i = -(int(numericCoord) - n)
    j = alphabet.index(literalCoord)
    return i, j


def findPegs(board, player):
    """
    Méthode permettant de trouver les pions d'un certain joueur
    : param board : plateau à inspecter
    : param player : joueur à trouver
    : return : liste de pions du joueur trouvés
    """
    pegs = []
    for i in range(len(board.getBoard())):
        for j in range(len(board.getBoard()[0])):
            if board.getBoard()[i][j] == player.getPlayerID():
                pegs.append([i, j])
    return pegs


def findBoardSources(board, player):
    """
    Méthode permettant de trouver des sources de mouvements valides pour les pions d'un certain joueur trouvés dans le
    plateau
    : param board : plateau à inspecter
    : param player : joueur concerné
    : return : liste de sources valides
    """
    validSources = []
    pegs = findPegs(board, player)
    for sourcePos in pegs:
        if checkPos(board, sourcePos, player.getPlayerID()):
            validSources.append(sourcePos)
    return validSources


def findPossibleSources(board, player):
    """
    Méthode qui trouve un premier pion valide à proposer au joueur. On itère sur la liste des pions du joueur, et
    si le pion est jouable, on renvoie son emplacement, sinon, on en trouve un nouveau
    :param player :
    :param board : Plateau du jeu
    :return : la position du pion jouable trouvé
    """
    # on itère sur la liste des pions du joueur, si le mouvement est correct on renvoie le mouvement, sinon on
    # réessaye
    possibleSources = []
    for sourcePos in player.getPosList():
        if checkPos(board, sourcePos, player.getPlayerID()):
            possibleSources.append(sourcePos)
    return possibleSources


def findPossibleDestinations(source, board, player):
    """
    Méthode permettant de trouver les destinations possibles pour une certaine source donnée
    :param player:
    :param source : source du mouvement
    :param board :
    :return : la liste des destinations du mouvement possible
    """

    if player.getPlayerID() == 1:
        return findMovePlayer1(board, source)
    else:
        return findMovePlayer2(board, source)


def squareContour(item):
    """
    Méthode permettant de dessiner le contour des cases constituant le plateau de jeu.
    : param item : case à contourner
    """
    pen = QPen(QColor(252, 204, 116))
    pen.setWidth(0)
    item.setPen(pen)


def pegsContour(item):
    """
    Méthode permettant de dessiner le contour des pions du plateau de jeu.
    : param item : pion à contourner
    """
    pen = QPen(Qt.black)
    pen.setWidth(0)
    item.setPen(pen)


def selectedPegContour(i, item, movablePegs):
    """
    Méthode permettant de rendre sélectionnable un pion ainsi que de le surligner.
    Si les coordonnées du pion correspondent aux coordonnées matricielles dans la liste des pions jouables, alors on le
    rend sélectionnable et on le surligne en bleu.
    : param i : index du pion dans la liste
    : param item : pion (objet PyQt) à traiter
    : param movablePegs : liste contenant les pions jouables
    """
    if int(item.scenePos().y() // 80) == movablePegs[i][0] and int(item.scenePos().x() // 80) == \
            movablePegs[i][1] and type(item) == QGraphicsEllipseItem:
        item.setFlag(QGraphicsItem.ItemIsSelectable)
        pen = QPen(Qt.blue)
        pen.setWidth(3)
        item.setPen(pen)


def findMove(board1, board2, playerID):
    """
    Méthode permettant de retrouver le mouvement effectué en comparant le plateau d'avant et le plateau d'après.
    : param board1 : plateau d'avant
    : param board2 : plateau d'après
    : param playerID : joueur ayant effectué le coup
    : return : mouvement trouvé
    """
    move = []
    temp = []
    for i in range(len(board1)):
        if board1[i] != board2[i]:
            for j in range(len(board1[i])):
                if board1[i][j] != board2[i][j]:
                    temp.append([i, j])
    if board1[temp[0][0]][temp[0][1]] != playerID:
        move.append(temp[1])
        move.append(temp[0])
    else:
        move = temp
    return move


def initColorSquare(i, j):
    """
    Méthode permettant de colorer les cases du plateau alternativement en fonction de leur position.
    : param i : coordonnée x (donc coordonnée matricielle de ligne)
    : param j : coordonnée y (donc coordonnée matricielle de colonne)
    : return : couleur du pinceau trouvée
    """
    if i % 2 == 0:
        if j % 2 == 0:
            brush = QBrush(QColor(252, 204, 116))
        else:
            brush = QBrush(QColor(138, 120, 93))
    else:
        if j % 2 == 0:
            brush = QBrush(QColor(138, 120, 93))
        else:
            brush = QBrush(QColor(252, 204, 116))
    return brush


def displayMessageBox(windowTitle, text):
    """
    Méthode permettant d'afficher un messageBox en fonction du texte donné.
    : param windowTitle : titre de la fenêtre
    : param text : texte à afficher
    """
    messageBox = QMessageBox()
    messageBox.setWindowTitle(windowTitle)
    messageBox.setText(text)
    messageBox.exec_()
