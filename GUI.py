import sys
import time

import Board
import Game
# todo: passer le code en renvue et nettoyage
# todo : changer les variables magiques
from PyQt5.QtCore import Qt, QEventLoop, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QGroupBox, QFormLayout, \
    QLabel, QComboBox, QVBoxLayout, QSlider, QFileDialog, QGraphicsScene, QGraphicsView, \
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtGui import QBrush, QPen
import Utils


class App(QWidget):
    """

    """
    # -------------------------------------------------partie d'initialisation d'attributs------------------------------
    MINIMAX = "Minimax"
    HUMAN = "Humain"
    WHITE = "white"
    BLACK = "black"
    SCALE = 80

    def __init__(self):

        super().__init__()
        self.initAttributes()
        self.mainLayout = QVBoxLayout()
        self.parametersBox = QGroupBox("Paramètres")
        self.importBox = QGroupBox("Import du plateau")
        self.title = "Breakthrough"
        self.initUI()
        self.createParametersBox()
        self.createImportBox()
        self.setMainLayout()
        self.show()

    def initAttributes(self):
        self.fileSelected = None
        self.stop = None
        self.board = None
        self.scene = None
        self.playing = False
        self.pegClicked = False
        self.posClicked = False
        self.blackPegs = []
        self.whitePegs = []
        self.positions = []
        self.moveCounter = 0

    # ------------------------------- Partie de création d'éléments graphiques ----------------------------------------

    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle(self.title)
        screen = app.primaryScreen()
        width = screen.size().width()
        height = screen.size().height()
        self.resize(int(width / 1.4), int(height / 1.4))
        self.centerWindow()

    def initComboPlayer(self):
        self.comboPlayer1 = QComboBox()
        self.comboPlayer1.addItem(self.MINIMAX)
        self.comboPlayer1.addItem(self.HUMAN)
        self.comboPlayer2 = QComboBox()
        self.comboPlayer2.addItem(self.MINIMAX)
        self.comboPlayer2.addItem(self.HUMAN)
        self.comboPlayer1.activated[str].connect(self.updatePlayers)
        self.comboPlayer2.activated[str].connect(self.updatePlayers)

    def initAISlider(self):
        self.AISlider = QSlider(Qt.Horizontal)
        self.AISlider.setMaximum(20)
        self.AISlider.setMinimum(0)
        self.AISlider.setSingleStep(1)
        self.AISlider.valueChanged.connect(self.updateAIDelay)
        self.AIDelay = QLabel("0")

    def initTimerSlider(self):
        self.timer = QSlider(Qt.Horizontal)
        self.timer.setMaximum(10)
        self.timer.setMinimum(2)
        self.timer.setSingleStep(1)
        self.timer.valueChanged.connect(self.updateTimer)
        self.AITimer = QLabel("2")

    def initBoard(self):
        for i in range(self.board.getlineDimension()):
            for j in range(self.board.getColumnDimension()):
                rect = QGraphicsRectItem(0, 0, self.SCALE, self.SCALE)
                rect.setPos(self.SCALE * i, self.SCALE * j)
                brush = Utils.initColorPeg(i, j)
                rect.setBrush(brush)
                Utils.squareContour(rect)
                self.scene.addItem(rect)

    def initPegs(self):
        for i in range(self.board.getlineDimension()):
            for j in range(self.board.getColumnDimension()):
                if self.board.getBoard()[i][j] == 1:
                    self.placeWhitePegs(i, j)
                elif self.board.getBoard()[i][j] == 2:
                    self.placeBlackPegs(i, j)

    def setMainLayout(self):
        self.mainLayout.setContentsMargins(10, 10, 10, int(self.height() * 3 / 4))
        self.mainLayout.addWidget(self.parametersBox)
        self.mainLayout.addWidget(self.importBox)
        self.setLayout(self.mainLayout)

    def createImportBox(self):
        layout = QFormLayout()
        layout.setVerticalSpacing(20)
        layout.setContentsMargins(50, 10, int(self.width() / 1.05), 10)

        self.fileSelected = QLabel("Aucun fichier sélectionné")
        importBoard = QPushButton('Importer', self)
        importBoard.clicked.connect(self.dialog)

        layout.addRow(self.fileSelected)
        layout.addRow(QLabel(""), importBoard)

        self.importBox.setLayout(layout)

    def createParametersBox(self):
        layout = QFormLayout()
        layout.setVerticalSpacing(20)
        layout.setContentsMargins(50, 10, 50, 10)

        self.initAISlider()
        self.initTimerSlider()
        self.initComboPlayer()

        layout.addRow(QLabel("Joueur 1:"), self.comboPlayer1)
        layout.addRow(QLabel("Joueur 2:"), self.comboPlayer2)
        layout.addRow(QLabel("Délai de l'IA (en secondes):"), self.AIDelay)
        layout.addWidget(self.AISlider)
        layout.addRow(QLabel("Durée du timer (en secondes): "), self.AITimer)
        layout.addWidget(self.timer)
        self.parametersBox.setLayout(layout)

    def createStopButton(self):
        self.start.hide()
        self.preview.hide()
        self.stop = QPushButton("arrêter")
        self.stop.setMaximumSize(130, 130)
        self.stop.clicked.connect(self.stopGame)
        self.mainLayout.addWidget(self.stop)

    def updateAIDelay(self):
        self.AIDelay.setText(str(self.AISlider.value() / 10))
        self.delay = self.AISlider.value()

    def updateTimer(self):
        self.timerValue = self.timer.value()
        self.AITimer.setText(str(self.timerValue))

    def updatePlayers(self):
        if not self.playing:
            if self.comboPlayer1.currentText() == self.HUMAN and self.comboPlayer2.currentText() == self.HUMAN:
                self.hideAIParameters()

            else:
                self.showAIParameters()
        else:
            Utils.displayMessageBox("Avertissement", "Les joueurs ne peuvent pas être changés en pleine partie. Vos "
                                                     "changements ne seront pas pris en compte.")

    def showAIParameters(self):
        self.AIDelay.setText(str(self.AISlider.value() / 10))
        self.AISlider.show()
        self.timerValue = self.timer.value()
        self.AITimer.setText(str(self.timerValue))
        self.timer.show()

    def hideAIParameters(self):
        self.AISlider.hide()
        self.AIDelay.setText("L'IA ne jouera pas si les deux joueurs sont humains.")
        self.AISlider.setValue(-1)
        self.timer.hide()
        self.AITimer.setText("L'IA ne jouera pas si les deux joueurs sont humains.")
        self.timer.setValue(-1)

    def createScene(self):
        self.preview = QLabel("Aperçu")
        self.mainLayout.addWidget(self.preview)
        self.scene = QGraphicsScene(0, 0, self.SCALE * self.board.getlineDimension(), self.SCALE * self.board.
                                    getColumnDimension())
        self.createBoard()
        self.start = QPushButton("Commencer")
        self.start.clicked.connect(self.play)
        self.start.setMaximumSize(130, 130)
        self.mainLayout.addWidget(self.start)

    def createBoard(self):
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.initBoard()
        self.initPegs()
        self.view = QGraphicsView(self.scene)
        self.mainLayout.addWidget(self.view)

    def placeBlackPegs(self, i, j):
        pegs = QGraphicsEllipseItem(0, 0, 50, 50)
        pegs.setPos(15 + j * self.SCALE, 15 + i * self.SCALE)
        brush = QBrush(Qt.black)
        pegs.setBrush(brush)
        Utils.pegsContour(pegs)
        self.scene.addItem(pegs)
        self.blackPegs.append(pegs)

    def placeWhitePegs(self, i, j):
        pegs = QGraphicsEllipseItem(0, 0, 50, 50)
        pegs.setPos(15 + j * self.SCALE, 15 + i * self.SCALE)
        brush = QBrush(Qt.white)
        pegs.setBrush(brush)
        Utils.pegsContour(pegs)
        self.scene.addItem(pegs)
        self.whitePegs.append(pegs)

    def refreshScene(self):
        if self.stop:
            self.stop.hide()
        self.start.show()
        self.preview.show()
        for item in self.scene.items():
            self.scene.removeItem(item)
        self.board = Board.Board(self.file)
        self.initBoard()
        self.initPegs()

    # ------------------------------- Partie du dialogue permettant d'importer un fichier ------------------------------

    def dialog(self):
        self.file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                       "", "Text Files (*.txt)")
        if check and self.file.endswith('.txt'):
            self.board = Board.Board(self.file)
            self.fileSelected.setText(self.file)
            if not self.scene:
                self.createScene()
            else:
                self.refreshScene()
        else:
            Utils.displayMessageBox("Erreur", "Veuillez sélectionner un fichier .txt")
            self.start.hide()

    # ------------------------------------- partie qui gère le mode de jeu humain vs humain ----------------------------

    def unlockBlackPegs(self, movablePegs):
        for i in range(len(movablePegs)):
            for item in self.blackPegs:
                Utils.selectedPegContour(i, item, movablePegs)

    def unlockWhitePegs(self, movablePegs):
        for i in range(len(movablePegs)):
            for item in self.whitePegs:
                Utils.selectedPegContour(i, item, movablePegs)

    def humanVSHuman(self, currentPlayer, nextPlayer):
        self.currentPlayer = currentPlayer
        self.nextPlayer = nextPlayer
        movablePegs = self.game.getMovablePegs(currentPlayer)
        if currentPlayer == self.WHITE:
            self.unlockWhitePegs(movablePegs)
        else:
            self.unlockBlackPegs(movablePegs)

    # ---------------------------------------------- Partie qui gère le mode de jeu AI VS AI ---------------------------

    def AIWait(self):
        loop = QEventLoop()
        QTimer.singleShot(self.delay * 100, loop.quit)
        loop.exec_()

    def AITimeout(self, playerID):
        Utils.displayMessageBox("Timeout!", "L'IA a pris trop de temps pour jouer. Son adversaire a donc remporté la "
                                            "partie.")

        if playerID == 1:
            self.displayWinner(2)
        else:
            self.displayWinner(1)

    def IASelectMove(self, IA):
        moment = time.time()
        if IA is None:

            move = self.game.IA.selectMove()
        else:
            move = IA.selectMove()
        timeout = time.time()
        if timeout > moment + self.timerValue:
            if IA is None:
                self.AITimeout(self.game.IA.playerID)
            else:
                self.AITimeout(IA.playerID)
        return move

    def findPegToMove(self, move):
        pegToMove = None
        if self.player2Type == self.MINIMAX and self.currentPlayer == self.BLACK:
            for peg in self.blackPegs:
                if int(peg.scenePos().y() // self.SCALE) == move[0][0] and int(peg.scenePos().x() //
                                                                               self.SCALE) == move[0][1]:
                    pegToMove = peg
        elif self.player1Type == self.MINIMAX and self.currentPlayer == self.WHITE:
            for peg in self.whitePegs:
                if int(peg.scenePos().y() // self.SCALE) == move[0][0] and int(peg.scenePos().x() //
                                                                               self.SCALE) == move[0][1]:
                    pegToMove = peg
        return pegToMove

    def movePeg(self, move, pegToMove):
        destinationX = None
        destinationY = None
        for item in self.scene.items():
            if int(item.scenePos().y() // self.SCALE) == move[1][0] and int(item.scenePos().x() // self.SCALE) == \
                    move[1][1] and type(item) == QGraphicsRectItem and pegToMove:
                destinationX = item.scenePos().x() + 15
                destinationY = item.scenePos().y() + 15
                pegToMove.setPos(destinationX, destinationY)
        return destinationX, destinationY

    def checkEatenPeg(self, destinationX, destinationY):
        if self.currentPlayer == self.WHITE:
            for peg in self.blackPegs:
                if peg.scenePos().x() == destinationX and peg.scenePos().y() == destinationY:
                    self.scene.removeItem(peg)
        else:
            for peg in self.whitePegs:
                if peg.scenePos().x() == destinationX and peg.scenePos().y() == destinationY:
                    self.scene.removeItem(peg)

    def IASetRoot(self, IA):
        if IA is None:
            self.game.IA.setRoot(self.game.board, self.game)
        else:
            self.game.IA1.setRoot(self.game.board, self.game)
            self.game.IA2.setRoot(self.game.board, self.game)

    def IAMakeMove(self, IA=None):
        move = self.IASelectMove(IA)
        if self.playing:
            if not move:
                self.stopGame()
            else:
                pegToMove = self.findPegToMove(move)
                destinationX, destinationY = self.movePeg(move, pegToMove)
                self.checkEatenPeg(destinationX, destinationY)
                self.game.makeMove(self.currentPlayer, move[0], move[1])
                self.IASetRoot(IA)
                self.moveCounter += 1
                if IA is None:
                    winner = self.checkWinner()
                    if winner == 0:
                        self.humanVSAI(self.nextPlayer, self.currentPlayer)

    def AIVSAI(self, currentPlayer, nextPlayer):
        self.currentPlayer = currentPlayer
        self.nextPlayer = nextPlayer
        if self.currentPlayer == self.WHITE:
            self.AIWait()
            self.IAMakeMove(self.game.IA1)
        else:
            self.AIWait()
            self.IAMakeMove(self.game.IA2)
        winner = self.game.getWinner()
        if winner != 0:
            self.displayWinner(winner)
        else:
            if self.playing:
                self.AIVSAI(nextPlayer, currentPlayer)

    # ------------------------------------ Partie qui gère le mode de jeu humain vs AI ---------------------------------

    def blackProcessing(self, currentPlayer):
        if self.player2Type == self.HUMAN:
            movablePegs = self.game.getMovablePegs(currentPlayer)
            self.unlockBlackPegs(movablePegs)
        else:
            self.AIWait()
            self.IAMakeMove()

    def whiteProcessing(self, currentPlayer):
        if self.player1Type == self.HUMAN:
            movablePegs = self.game.getMovablePegs(currentPlayer)
            self.unlockWhitePegs(movablePegs)
        else:
            self.AIWait()
            self.IAMakeMove()

    def humanVSAI(self, currentPlayer, nextPlayer):
        self.currentPlayer = currentPlayer
        self.nextPlayer = nextPlayer
        if self.currentPlayer == self.WHITE:
            self.whiteProcessing(currentPlayer)
        else:
            self.blackProcessing(currentPlayer)

    # -------------------------------------- Partie qui permet la sélection du mode de jeu -----------------------------

    def selectGameMode(self):
        if self.player1Type == self.HUMAN and self.player2Type == self.HUMAN:
            self.humanVSHuman(self.WHITE, self.BLACK)
        elif self.player1Type == self.MINIMAX and self.player2Type == self.MINIMAX:
            self.AIVSAI(self.WHITE, self.BLACK)
        else:
            self.humanVSAI(self.WHITE, self.BLACK)

    # -------------------------------------- Bloc qui gère le déroulement d'une partie ---------------------------------

    def play(self):
        self.refreshScene()
        self.moveCounter = 0
        self.playing = True
        self.delay = self.AISlider.value()
        self.timerValue = self.timer.value()
        self.createStopButton()
        self.player1Type = self.comboPlayer1.currentText()
        self.player2Type = self.comboPlayer2.currentText()
        self.game = Game.Game(self.player1Type, self.player2Type, self.board, self.timerValue)
        self.selectGameMode()
        self.scene.selectionChanged.connect(self.selectionHandler)

    def unlockDestinations(self, destinations):
        for i in range(len(destinations)):
            for item in self.scene.items():
                if int(item.scenePos().y() // self.SCALE) == destinations[i][0] and int(item.scenePos().x() //
                                                self.SCALE) == destinations[i][1] and type(item) == QGraphicsRectItem:
                    item.setFlag(QGraphicsItem.ItemIsSelectable)
                    pen = QPen(Qt.red)
                    pen.setWidth(3)
                    item.setPen(pen)

    def selectPeg(self):
        self.pegClicked = True
        self.selectedPeg = self.scene.selectedItems()[0]
        source = [int(self.selectedPeg.scenePos().y() // self.SCALE), int(self.selectedPeg.scenePos().x() //
                                                                          self.SCALE)]
        destinations = self.game.getPossibleDestinations(self.currentPlayer, source)
        self.unlockDestinations(destinations)

    def pegHandler(self):
        # si on clique sur un pion après avoir cliqué sur un pion, il faut bloquer tous les mouvements du pion précédent
        if self.pegClicked:
            self.lockPreviousDestinations()
            if self.player1Type == self.HUMAN and self.player2Type == self.HUMAN:
                self.humanVSHuman(self.currentPlayer, self.nextPlayer)
        self.selectPeg()

    def selectPos(self):
        if self.pegClicked:
            source = [int(self.selectedPeg.scenePos().y() // self.SCALE), int(self.selectedPeg.scenePos().x() //
                                                                              self.SCALE)]
            self.selectedPos = self.scene.selectedItems()[0]
            destination = [int(self.selectedPos.scenePos().y() // self.SCALE), int(self.selectedPos.scenePos().x() //
                                                                                   self.SCALE)]
            validMove = self.game.makeMove(self.currentPlayer, source, destination)
            if validMove:
                self.selectedPeg.setPos(self.selectedPos.scenePos().x() + 15,
                                        self.selectedPos.scenePos().y() + 15)
                self.moveCounter += 1
            else:
                Utils.displayMessageBox("Mouvement invalide", "Veuillez donner un mouvement valide")

    def lockPreviousPegs(self):
        for item in self.scene.items():
            if type(item) == QGraphicsEllipseItem:
                item.setFlag(QGraphicsItem.ItemIsSelectable, False)
                Utils.pegsContour(item)

    def lockPreviousDestinations(self):
        for item in self.scene.items():
            if type(item) == QGraphicsRectItem:
                item.setFlag(QGraphicsItem.ItemIsSelectable, False)
                Utils.squareContour(item)

    def eatPeg(self):
        for item in self.scene.items():
            if type(item) == QGraphicsEllipseItem:
                if (item.scenePos().x() == self.selectedPos.scenePos().x() + 15 and item.scenePos().y() == self.
                        selectedPos.scenePos().y() + 15) and item != self.selectedPeg:
                    self.scene.removeItem(item)

    def squareHandler(self):
        # si on clique sur une case après avoir cliqué sur un pion, il faut bloquer tous les autres pions et toutes les
        # autres cases disponibles pour ces pions précédents
        self.selectPos()
        if self.player1Type == self.MINIMAX or self.player2Type == self.MINIMAX:
            self.game.IA.setRoot(self.game.board, self.game)
        winner = self.checkWinner()
        if winner ==0:
            self.lockPreviousPegs()
            self.lockPreviousDestinations()
            self.eatPeg()
            self.pegClicked = False
            if (self.player1Type == self.HUMAN and self.player2Type == self.MINIMAX) or \
                    (self.player1Type == self.MINIMAX and self.player2Type == self.HUMAN):
                self.humanVSAI(self.nextPlayer, self.currentPlayer)
            elif self.player1Type == self.HUMAN and self.player2Type == self.HUMAN:
                self.humanVSHuman(self.nextPlayer, self.currentPlayer)

    def selectionHandler(self):
        if len(self.scene.selectedItems()) > 0:
            if type(self.scene.selectedItems()[0]) == QGraphicsEllipseItem:
                self.pegHandler()
            else:
                self.squareHandler()
                #self.checkWinner()

    def checkWinner(self):
        winner = self.game.getWinner()
        if winner != 0:
            self.displayWinner(winner)
        return winner

    def stopGame(self):
        self.playing = False
        self.stop.hide()
        self.start.show()
        for item in self.scene.items():
            item.setFlag(QGraphicsItem.ItemIsSelectable, False)
            if type(item) == QGraphicsRectItem:
                Utils.squareContour(item)
            else:
                Utils.pegsContour(item)

    def displayWinner(self, winner):
        if winner == 1:
            Utils.displayMessageBox("Gagné!", "Le joueur blanc a gagné!")
        else:
            Utils.displayMessageBox("Gagné!", "Le joueur noir a gagné!")
        self.stopGame()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
