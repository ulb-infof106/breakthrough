import sys
import Board
import Game

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QGroupBox, QFormLayout, \
    QLineEdit, QLabel, QComboBox, QSpinBox, QVBoxLayout, QSlider, QFileDialog, QGraphicsScene, QGraphicsView, \
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtGui import QIcon, QBrush, QPen, QColor
from PyQt5.QtCore import pyqtSlot


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.playing = False
        self.pegClicked = False
        self.posClicked = False
        self.blackPegs = []
        self.whitePegs = []
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

    def updatePlayers(self):
        if self.comboPlayer1.currentText() == "Humain" and self.comboPlayer2.currentText() == "Humain":
            self.AISlider.hide()
            self.AILevel.setText("L'IA ne jouera pas si les deux joueurs sont humains.")
            self.AISlider.setValue(-1)

        else:
            self.AILevel.setText(str(self.AISlider.value() / 10))
            self.AISlider.show()

    def createScene(self):
        self.scene = QGraphicsScene(0, 0, 80 * self.board.getlineDimension(), 80 * self.board.getColumnDimension())
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.initBoard()
        self.initPegs()
        self.view = QGraphicsView(self.scene)
        preview = QLabel("Aperçu")
        self.start = QPushButton("Commencer")
        self.start.clicked.connect(self.play)
        self.start.setMaximumSize(130, 130)
        self.mainLayout.addWidget(preview)
        self.mainLayout.addWidget(self.view)
        self.mainLayout.addWidget(self.start)
        # self.view.show()

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
        pen = QPen(Qt.black)
        pen.setWidth(1)
        pegs.setPen(pen)
        self.scene.addItem(pegs)
        self.blackPegs.append(pegs)

    def placeWhitePegs(self, i, j):
        pegs = QGraphicsEllipseItem(0, 0, 50, 50)
        pegs.setPos(15 + j * 80, 15 + i * 80)
        brush = QBrush(Qt.white)
        pegs.setBrush(brush)
        pen = QPen(Qt.black)
        pen.setWidth(1)
        pegs.setPen(pen)
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
                pen = QPen(QColor(252, 204, 116))
                pen.setWidth(0)
                rect.setPen(pen)

                self.scene.addItem(rect)

    def dialog(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "Text Files (*.txt)")
        if check:
            self.board = Board.Board(file)
            self.fileSelected.setText(file)
            self.createScene()

    def play(self):
        self.playing = True
        """for item in self.scene.items():
            if type(item) == QGraphicsRectItem:
                item.setFlag(QGraphicsItem.ItemIsSelectable)"""
        self.createStopButton()
        AIDelay = self.AISlider.value()
        player1Type = self.comboPlayer1.currentText()
        player2Type = self.comboPlayer2.currentText()
        self.game = Game.Game(player1Type, player2Type, AIDelay, self.board)
        self.humainVSHumain("white", "black")
        self.scene.selectionChanged.connect(self.selectPeg)

    def selectPeg(self):
        if len(self.scene.selectedItems()) > 0:
            if type(self.scene.selectedItems()[0]) == QGraphicsEllipseItem:
                self.selectedPeg = self.scene.selectedItems()[0]
                self.game.getPossibleMoves(self.currentPlayer,[int(self.selectedPeg.scenePos().y() // 80), int(self.selectedPeg.scenePos().x() // 80)])

    def humainVSHumain(self, currentPlayer, nextPlayer):
        self.currentPlayer = currentPlayer
        movablePegs = self.game.getMovablePegs(currentPlayer)
        if currentPlayer == "white":
            self.unlockWhitePegs(movablePegs)
        else:
            self.unlockBlackPegs(movablePegs)

    def unlockBlackPegs(self, movablePegs):
        for i in range(len(movablePegs)):
            for item in self.blackPegs:

                if int(item.scenePos().y() // 80) == movablePegs[i][0] and int(item.scenePos().x() // 80) == \
                        movablePegs[i][1] and type(item) == QGraphicsEllipseItem:
                    item.setFlag(QGraphicsItem.ItemIsSelectable)
                    pen = QPen(Qt.blue)
                    pen.setWidth(3)
                    item.setPen(pen)

    def unlockWhitePegs(self, movablePegs):
        for i in range(len(movablePegs)):
            for item in self.whitePegs:

                if int(item.scenePos().y() // 80) == movablePegs[i][0] and int(item.scenePos().x() // 80) == \
                        movablePegs[i][1] and type(item) == QGraphicsEllipseItem:
                    item.setFlag(QGraphicsItem.ItemIsSelectable)
                    pen = QPen(Qt.blue)
                    pen.setWidth(3)
                    item.setPen(pen)

    def createStopButton(self):
        self.start.hide()
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

    def movePegs(self):
        if len(self.scene.selectedItems()) > 0:
            if type(self.scene.selectedItems()[0]) == QGraphicsEllipseItem:
                self.selectedPeg = self.scene.selectedItems()[0]
                self.pegClicked = True
            else:
                if self.pegClicked == True:
                    self.selectedPos = self.scene.selectedItems()[0]
                    self.posClicked = True
            if self.posClicked and self.pegClicked:
                print("pion:")
                print(self.selectedPeg.scenePos().x() // 80)
                print(self.selectedPeg.scenePos().y() // 80)
                self.eatPeg()
                self.selectedPeg.setPos(self.selectedPos.scenePos().x() + 15, self.selectedPos.scenePos().y() + 15)
                print("case :")
                print(self.selectedPos.scenePos().x() // 80)
                print(self.selectedPos.scenePos().y() // 80)
                self.posClicked = False
                self.pegClicked = False

    def eatPeg(self):
        for item in self.scene.items():
            if type(item) == QGraphicsEllipseItem:
                if item.scenePos().x() == self.selectedPos.scenePos().x() + 15 and item.scenePos().y() == self. \
                        selectedPos.scenePos().y() + 15:
                    self.scene.removeItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
