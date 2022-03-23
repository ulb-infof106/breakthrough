import sys

import Board
import Game
# todo : AI VS AI
# todo : AI vs humain
# todo: si humain gagne, fin détectée après que l'ai ait joué
from PyQt5.QtCore import Qt, QEventLoop, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QGroupBox, QFormLayout, \
    QLabel, QComboBox, QVBoxLayout, QSlider, QFileDialog, QGraphicsScene, QGraphicsView, \
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtGui import QBrush, QPen, QColor
import Utils


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.scene = None
        self.playing = False
        self.pegClicked = False
        self.posClicked = False
        self.blackPegs = []
        self.whitePegs = []
        self.positions = []
        self.mainLayout = QVBoxLayout()
        self.parametersBox = QGroupBox("Paramètres")
        self.importBox = QGroupBox("Import du plateau")
        self.title = "Breakthrough"
        self.initUI()
        self.createParametersBox()
        self.createImportBox()
        self.setMainLayout()
        self.show()

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
        self.resize(int(width / 1.5), int(height / 1.5))
        self.centerWindow()

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

        self.initSlider()
        self.initComboPlayer()

        layout.addRow(QLabel("Joueur 1:"), self.comboPlayer1)
        layout.addRow(QLabel("Joueur 2:"), self.comboPlayer2)
        layout.addRow(QLabel("Délai de l'IA (en secondes):"), self.AILevel)
        layout.addWidget(self.AISlider)

        self.parametersBox.setLayout(layout)

    def initComboPlayer(self):
        self.comboPlayer1 = QComboBox()
        self.comboPlayer1.addItem("Minimax")
        self.comboPlayer1.addItem("Humain")
        self.comboPlayer2 = QComboBox()
        self.comboPlayer2.addItem("Minimax")
        self.comboPlayer2.addItem("Humain")
        self.comboPlayer1.activated[str].connect(self.updatePlayers)
        self.comboPlayer2.activated[str].connect(self.updatePlayers)

    def initSlider(self):
        self.AISlider = QSlider(Qt.Horizontal)
        self.AISlider.setMaximum(20)
        self.AISlider.setMinimum(0)
        self.AISlider.setSingleStep(1)
        self.AISlider.valueChanged.connect(self.updateAILevel)
        self.AILevel = QLabel("0")

    def updateAILevel(self):
        self.AILevel.setText(str(self.AISlider.value() / 10))
        self.delay = self.AISlider.value()

    def updatePlayers(self):
        if not self.playing:
            if self.comboPlayer1.currentText() == "Humain" and self.comboPlayer2.currentText() == "Humain":
                self.AISlider.hide()
                self.AILevel.setText("L'IA ne jouera pas si les deux joueurs sont humains.")
                self.AISlider.setValue(-1)

            else:
                self.AILevel.setText(str(self.AISlider.value() / 10))
                self.AISlider.show()
        else:
            warning = QMessageBox()
            warning.setWindowTitle("Avertissement")
            warning.setText("Les joueurs ne peuvent pas être changés en pleine partie. Vos changements ne seront pas "
                            "pris en compte.")
            warning.exec_()


    def createScene(self):
        self.preview = QLabel("Aperçu")
        self.mainLayout.addWidget(self.preview)
        self.scene = QGraphicsScene(0, 0, 80 * self.board.getlineDimension(), 80 * self.board.getColumnDimension())
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

    def initPegs(self):
        for i in range(self.board.getlineDimension()):
            for j in range(self.board.getColumnDimension()):
                if self.board.getBoard()[i][j] == 1:
                    self.placeWhitePegs(i, j)
                elif self.board.getBoard()[i][j] == 2:
                    self.placeBlackPegs(i, j)

    def placeBlackPegs(self, i, j):
        pegs = QGraphicsEllipseItem(0, 0, 50, 50)
        pegs.setPos(15 + j * 80, 15 + i * 80)
        brush = QBrush(Qt.black)
        pegs.setBrush(brush)
        Utils.pegsContour(pegs)
        self.scene.addItem(pegs)
        self.blackPegs.append(pegs)

    def placeWhitePegs(self, i, j):
        pegs = QGraphicsEllipseItem(0, 0, 50, 50)
        pegs.setPos(15 + j * 80, 15 + i * 80)
        brush = QBrush(Qt.white)
        pegs.setBrush(brush)
        Utils.pegsContour(pegs)
        self.scene.addItem(pegs)
        self.whitePegs.append(pegs)

    def initBoard(self):

        for i in range(self.board.getlineDimension()):
            for j in range(self.board.getColumnDimension()):
                rect = QGraphicsRectItem(0, 0, 80, 80)
                rect.setPos(80 * i, 80 * j)
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
                rect.setBrush(brush)
                Utils.squareContour(rect)
                self.scene.addItem(rect)

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
            self.errorMessage()

    def errorMessage(self):
        error = QMessageBox()
        error.setWindowTitle("Erreur")
        error.setText("Veuillez sélectionner un fichier .txt")
        error.exec_()

    def play(self):
        self.refreshScene()
        self.playing = True
        self.delay = self.AISlider.value()
        self.createStopButton()
        self.player1Type = self.comboPlayer1.currentText()
        self.player2Type = self.comboPlayer2.currentText()
        self.game = Game.Game(self.player1Type, self.player2Type, self.board)
        self.selectGameMode()
        self.scene.selectionChanged.connect(self.selectionHandler)

    def selectGameMode(self):
        if self.player1Type == "Humain" and self.player2Type == "Humain":
            self.humanVSHuman("white", "black")
        elif self.player1Type == "Humain" and self.player2Type == "Minimax":
            self.humanVSAI("white", "black")

    def humanVSAI(self, currentPlayer, nextPlayer):
        self.currentPlayer = currentPlayer
        self.nextPlayer = nextPlayer
        if self.currentPlayer == "white":
            movablePegs = self.game.getMovablePegs(currentPlayer)
            self.unlockWhitePegs(movablePegs)
        else:
            self.AIWait()
            self.IAMakeMove()

    def AIWait(self):
        loop = QEventLoop()
        QTimer.singleShot(self.delay*100, loop.quit)
        loop.exec_()

    def IAMakeMove(self):
        move = self.game.IA.play(self.game)
        pegToMove = self.findPegToMove(move)
        destinationX, destinationY = self.movePeg(move, pegToMove)
        self.checkEatenPeg(destinationX, destinationY)

    def checkEatenPeg(self, destinationX, destinationY):
        for peg in self.whitePegs:
            if peg.scenePos().x() == destinationX and peg.scenePos().y() == destinationY:
                self.scene.removeItem(peg)

    def movePeg(self, move, pegToMove):
        destinationX = None
        destinationY = None
        for item in self.scene.items():
            if int(item.scenePos().y() // 80) == move[1][0] and int(item.scenePos().x() // 80) == \
                    move[1][1] and type(item) == QGraphicsRectItem and pegToMove:
                destinationX = item.scenePos().x() + 15
                destinationY = item.scenePos().y() + 15
                pegToMove.setPos(destinationX, destinationY)
        return destinationX, destinationY

    def findPegToMove(self, move):
        pegToMove = None
        for peg in self.blackPegs:
            if int(peg.scenePos().y() // 80) == move[0][0] and int(peg.scenePos().x() // 80) == move[0][1]:
                pegToMove = peg
        return pegToMove

    def refreshScene(self):
        self.preview.show()
        for item in self.scene.items():
            self.scene.removeItem(item)
        self.board = Board.Board(self.file)
        self.initBoard()
        self.initPegs()

    def selectionHandler(self):
        #if not self.pegClicked:
        #
        if len(self.scene.selectedItems()) > 0:
            if type(self.scene.selectedItems()[0]) == QGraphicsEllipseItem:
                self.pegHandler()
            else:
                self.squareHandler()
                self.checkWinner()

    def squareHandler(self):
        # si on clique sur une case après avoir cliqué sur un pion, il faut bloquer tous les autres pions et toutes les
        # autres cases disponibles pour ces pions précédents
        self.selectPos()
        self.lockPreviousPegs()
        self.lockPreviousDestinations()
        self.eatPeg()
        self.pegClicked = False
        if self.player1Type == "Humain" and self.player2Type == "Minimax":
            self.humanVSAI(self.nextPlayer, self.currentPlayer)

    def pegHandler(self):
        # si on clique sur un pion après avoir cliqué sur un pion, il faut bloquer tous les mouvements du pion précédent
        if self.pegClicked:
            self.lockPreviousDestinations()
            if self.player1Type == "Humain" and self.player2Type == "Humain":
                self.humanVSHuman(self.currentPlayer, self.nextPlayer)
        self.selectPeg()

    def checkWinner(self):
        winner = self.game.getWinner()
        if winner == 0:
            self.humanVSHuman(self.nextPlayer, self.currentPlayer)
        else:
            if winner == 1:
                win = QMessageBox()
                win.setWindowTitle("Gagné!")
                win.setText("Le joueur blanc a gagné!")
                win.exec_()
            else:
                win = QMessageBox()
                win.setWindowTitle("Gagné!")
                win.setText("Le joueur noir a gagné!")
                win.exec_()

            self.stopGame()

    def lockPreviousPegs(self):
        for item in self.scene.items():
            if type(item) == QGraphicsEllipseItem:
                item.setFlag(QGraphicsItem.ItemIsSelectable, False)
                Utils.pegsContour(item)

    def selectPos(self):
        if self.pegClicked:
            source = [int(self.selectedPeg.scenePos().y() // 80), int(self.selectedPeg.scenePos().x() // 80)]
            self.selectedPos = self.scene.selectedItems()[0]
            destination = [int(self.selectedPos.scenePos().y() // 80), int(self.selectedPos.scenePos().x() // 80)]
            validMove = self.game.makeMove(self.currentPlayer, source, destination)
            if validMove:
                self.selectedPeg.setPos(self.selectedPos.scenePos().x() + 15,
                                        self.selectedPos.scenePos().y() + 15)
            else:
                invalidMove = QMessageBox()
                invalidMove.setWindowTitle("Mouvement invalide")
                invalidMove.setText("Veuillez donner un mouvement valide")
                invalidMove.exec_()

    def selectPeg(self):
        self.pegClicked = True
        self.selectedPeg = self.scene.selectedItems()[0]
        source = [int(self.selectedPeg.scenePos().y() // 80), int(self.selectedPeg.scenePos().x() // 80)]
        destinations = self.game.getPossibleDestinations(self.currentPlayer, source)
        self.unlockDestinations(destinations)

    def humanVSHuman(self, currentPlayer, nextPlayer):
        self.currentPlayer = currentPlayer
        self.nextPlayer = nextPlayer
        movablePegs = self.game.getMovablePegs(currentPlayer)
        if currentPlayer == "white":
            self.unlockWhitePegs(movablePegs)
        else:
            self.unlockBlackPegs(movablePegs)

    def lockPreviousDestinations(self):
        for item in self.scene.items():
            if type(item) == QGraphicsRectItem:
                item.setFlag(QGraphicsItem.ItemIsSelectable, False)
                Utils.squareContour(item)

    def unlockDestinations(self, destinations):
        for i in range(len(destinations)):
            for item in self.scene.items():
                if int(item.scenePos().y() // 80) == destinations[i][0] and int(item.scenePos().x() // 80) == \
                        destinations[i][1] and type(item) == QGraphicsRectItem:
                    item.setFlag(QGraphicsItem.ItemIsSelectable)
                    pen = QPen(Qt.red)
                    pen.setWidth(3)
                    item.setPen(pen)

    def unlockBlackPegs(self, movablePegs):
        for i in range(len(movablePegs)):
            for item in self.blackPegs:
                Utils.selectedPegContour(i, item, movablePegs)

    def unlockWhitePegs(self, movablePegs):
        for i in range(len(movablePegs)):
            for item in self.whitePegs:
                Utils.selectedPegContour(i, item, movablePegs)

    def createStopButton(self):
        self.start.hide()
        self.preview.hide()
        self.stop = QPushButton("arrêter")
        self.stop.setMaximumSize(130, 130)
        self.stop.clicked.connect(self.stopGame)
        self.mainLayout.addWidget(self.stop)

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

    def eatPeg(self):
        for item in self.scene.items():
            if type(item) == QGraphicsEllipseItem:
                if (item.scenePos().x() == self.selectedPos.scenePos().x() + 15 and item.scenePos().y() == self.
                        selectedPos.scenePos().y() + 15) and item != self.selectedPeg:
                    self.scene.removeItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
