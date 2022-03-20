import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QGroupBox, QFormLayout, \
    QLineEdit, QLabel, QComboBox, QSpinBox, QVBoxLayout, QSlider, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.parametersBox = QGroupBox("Paramètres")
        self.boardBox = QGroupBox("Import du plateau")
        self.title = "Breakthrough"
        self.initUI()
        self.createParametersBox()
        self.createBoardBox()
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
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(10, 10, 10, int(self.height()*3/4))
        mainLayout.addWidget(self.parametersBox)
        mainLayout.addWidget(self.boardBox)
        self.setLayout(mainLayout)

    def createBoardBox(self):
        layout = QFormLayout()
        layout.setVerticalSpacing(20)
        layout.setContentsMargins(50, 10, int(self.width()/1.05), 10)

        self.fileSelected = QLabel("Aucun fichier sélectionné")
        importBoard = QPushButton('Importer', self)
        importBoard.clicked.connect(self.dialog)

        layout.addRow(self.fileSelected)
        layout.addRow(QLabel(""), importBoard)

        self.boardBox.setLayout(layout)

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
        self.AILevel.setText(str(self.AISlider.value()/10))

    def updatePlayers(self):
        if self.comboPlayer1.currentText() == "Humain" and self.comboPlayer2.currentText() == "Humain":
            self.AISlider.hide()
            self.AILevel.setText("L'IA ne jouera pas si les deux joueurs sont humains.")

        else:
            self.AILevel.setText(str(self.AISlider.value()/10))
            self.AISlider.show()

    def dialog(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "Text Files (*.txt)")
        if check:
            print(file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
