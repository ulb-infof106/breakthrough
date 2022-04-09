"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA INFO
"""
# note: explication des warnings à la fin de ce fichier
import time

from PyQt5.QtCore import Qt, QEventLoop, QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QDesktopWidget, QGroupBox, QFormLayout, \
    QLabel, QComboBox, QVBoxLayout, QSlider, QFileDialog, QGraphicsScene, QGraphicsView, \
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtGui import QBrush, QPen

import Board
import Game
import Utils


class App(QWidget):
    """
    Classe représentant l'application graphique PyQT5
    """
    # -------------------------------------------------partie d'initialisation d'attributs------------------------------
    MINIMAX = "Minimax"
    HUMAN = "Humain"
    WHITE = "white"
    BLACK = "black"
    SCALE = 80

    def __init__(self, app):

        super().__init__()
        """
        Tout d'abord, on initialise le paramétrage de la fenêtre (taille, etc).
        Ensuite, le mainLayout de la classe est divisée en deux boites; pour des raisons esthétiques : parametersBox et
        importBox, qui sont créées dès la création de l'application. Ensuite, on ajoute ces boits au mainLayout et 
        on montre le tout.
        """
        self.app = app
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
        self.playing = None
        self.pegClicked = False
        self.posClicked = False
        self.blackPegs = []
        self.whitePegs = []
        self.positions = []
        self.moveCounter = 0

    # ------------------------------- Partie de création d'éléments graphiques ----------------------------------------

    def centerWindow(self):
        """
        Méthode qui permet de centrer la fenêtre au milieu de l'écran de l'utilisateur
        """
        geometry = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(centerPoint)
        self.move(geometry.topLeft())

    def initUI(self):
        """
        Méthode permettant d'initialiser les paramètres de la fenêtre tel que le titre et la taille.
        """
        self.setWindowTitle(self.title)
        screen = self.app.primaryScreen()
        width = screen.size().width()
        height = screen.size().height()
        self.resize(int(width / 1.4), int(height / 1.4))
        self.centerWindow()

    def initComboPlayer(self):
        """
        Méthode qui permet de créer deux comboBoxs et y ajouter des éléments représentant les joueurs de la partie.
        """
        self.comboPlayer1 = QComboBox()
        self.comboPlayer1.addItem(self.MINIMAX)
        self.comboPlayer1.addItem(self.HUMAN)
        self.comboPlayer2 = QComboBox()
        self.comboPlayer2.addItem(self.MINIMAX)
        self.comboPlayer2.addItem(self.HUMAN)
        self.comboPlayer1.activated[str].connect(self.updatePlayers)
        self.comboPlayer2.activated[str].connect(self.updatePlayers)

    def initAISlider(self):
        """
        Méthode permettant de créer un slider afin de choisir le délai que l'IA respectera avant de jouer.
        """
        self.AISlider = QSlider(Qt.Horizontal)
        self.AISlider.setMaximum(20)
        self.AISlider.setMinimum(0)
        self.AISlider.setSingleStep(1)
        self.AISlider.valueChanged.connect(self.updateAIDelay)
        self.AIDelay = QLabel("0")

    def initTimerSlider(self):
        """
        Méthode permettant de créer un slider afin de choisir le temps en secondes que l'AI aura pour jouer un coup.
        """
        self.timer = QSlider(Qt.Horizontal)
        self.timer.setMaximum(10)
        self.timer.setMinimum(2)
        self.timer.setSingleStep(1)
        self.timer.valueChanged.connect(self.updateTimer)
        self.AITimer = QLabel("2")

    def initBoard(self):
        """
        Méthode permettant d'initialiser un tableau de jeu. Il s'agit d'un ensemble de rectangles, alternativement de
        couleurs différentes. Chaque rectangle représentera une case.
        """
        for i in range(self.board.getlineDimension()):
            for j in range(self.board.getColumnDimension()):
                rect = QGraphicsRectItem(0, 0, self.SCALE, self.SCALE)
                rect.setPos(self.SCALE * i, self.SCALE * j)
                brush = Utils.initColorSquare(i, j)
                rect.setBrush(brush)
                Utils.squareContour(rect)
                self.scene.addItem(rect)

    def initPegs(self):
        """
        Méthode permettant de placer les pions noirs et blancs sur le plateau, en fonction du fichier importé.
        """
        for i in range(self.board.getlineDimension()):
            for j in range(self.board.getColumnDimension()):
                if self.board.getBoard()[i][j] == 1:
                    self.placeWhitePegs(i, j)
                elif self.board.getBoard()[i][j] == 2:
                    self.placeBlackPegs(i, j)

    def setMainLayout(self):
        """
        Méthide permettant d'intégrer les différents layouts au layout principal et d'y configurer sa marge.
        """
        self.mainLayout.setContentsMargins(10, 10, 10, int(self.height() * 3 / 4))
        self.mainLayout.addWidget(self.parametersBox)
        self.mainLayout.addWidget(self.importBox)
        self.setLayout(self.mainLayout)

    def createImportBox(self):
        """
        Méthode permettant d'initialiser le layout dans lequel on place les éléments utiles à l'import de plateau.
        Ce layout est sous forme de boite.
        """
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
        """
        Méthode permettant d'initialiser le layout dans lequel on place les éléments utiles au paramétrage de la partie.
        Ce layout est sous forme de boite.
        """
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
        """
        Méthode permettant de créer un bouton stop qui servira à l'arrêt d'une partie en cours.
        """
        self.start.hide()
        self.preview.hide()
        self.stop = QPushButton("arrêter")
        self.stop.setMaximumSize(130, 130)
        self.stop.clicked.connect(self.stopGame)
        self.mainLayout.addWidget(self.stop)

    def updateAIDelay(self):
        """
        Méthode permettant de changer le délai que l'AI doit respecter avant de jouer en fonction de l'input utilisateur
        via le slider initialisé.
        """
        self.AIDelay.setText(str(self.AISlider.value() / 10))
        self.delay = self.AISlider.value()

    def updateTimer(self):
        """
        Méthode permettant de changer la durée que l'IA doit respecter pour jouer en fonction de l'input utilisateur
        via le slider initialisé.
        """
        self.timerValue = self.timer.value()
        self.AITimer.setText(str(self.timerValue))

    def updatePlayers(self):
        """
        Méthode permettant de changer le type de joueur en fonction de l'input utilisateur via les combo box
        initialisés. De plus, si aucune IA ne joue, ses paramètres relatifs sont cachés.
        """
        if not self.playing:
            if self.comboPlayer1.currentText() == self.HUMAN and self.comboPlayer2.currentText() == self.HUMAN:
                self.hideAIParameters()

            else:
                self.showAIParameters()
        else:
            Utils.displayMessageBox("Avertissement", "Les joueurs ne peuvent pas être changés en pleine partie. Vos "
                                                     "changements ne seront pas pris en compte.")

    def showAIParameters(self):
        """
        Méthode permettant d'afficher les paramètres relatifs à l'IA.
        """
        self.AIDelay.setText(str(self.AISlider.value() / 10))
        self.AISlider.show()
        self.timerValue = self.timer.value()
        self.AITimer.setText(str(self.timerValue))
        self.timer.show()

    def hideAIParameters(self):
        """
        Méthode permettant de cacher les paramètres relatifs à l'IA.
        """
        self.AISlider.hide()
        self.AIDelay.setText("L'IA ne jouera pas si les deux joueurs sont humains.")
        self.AISlider.setValue(-1)
        self.timer.hide()
        self.AITimer.setText("L'IA ne jouera pas si les deux joueurs sont humains.")
        self.timer.setValue(-1)

    def createScene(self):
        """
        Méthode permettant de créer la scène où sera montré l'aperçu du plateau de jeu.
        """
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
        """
        Méthode permettant de créer le plateau de jeu et de l'ajouter à la scène.
        """
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.initBoard()
        self.initPegs()
        self.view = QGraphicsView(self.scene)
        self.mainLayout.addWidget(self.view)

    def placeBlackPegs(self, i, j):
        """
        Méthode permettant de placer sur le plateau les pions noirs du jeu, en fonction du fichier reçu en import.
        : param i : indice x du pion (c'est-à-dire indice matriciel de ligne du pion)
        : param j : indice y du pion (c'est-à-dire indice matriciel de colonne du pion)
        """
        pegs = QGraphicsEllipseItem(0, 0, 50, 50)
        pegs.setPos(15 + j * self.SCALE, 15 + i * self.SCALE)
        brush = QBrush(Qt.black)
        pegs.setBrush(brush)
        Utils.pegsContour(pegs)
        self.scene.addItem(pegs)
        self.blackPegs.append(pegs)

    def placeWhitePegs(self, i, j):
        """
        Méthode permettant de placer sur le plateau les pions blancs du jeu, en fonction du fichier reçu en import.
        : param i : indice x du pion (c'est-à-dire indice matriciel de ligne du pion)
        : param j : indice y du pion (c'est-à-dire indice matriciel de colonne du pion)
        """
        pegs = QGraphicsEllipseItem(0, 0, 50, 50)
        pegs.setPos(15 + j * self.SCALE, 15 + i * self.SCALE)
        brush = QBrush(Qt.white)
        pegs.setBrush(brush)
        Utils.pegsContour(pegs)
        self.scene.addItem(pegs)
        self.whitePegs.append(pegs)

    def refreshScene(self):
        """
        Méthode permettant de rafraichir la scène, c'est-à-dire de charger dans la scène un nouveau plateau de jeu où
        aucune partie n'est en cours et de rendre une partie jouable sur ce plateau.
        """
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
        """
        Méthode permettant d'importer un fichier via un widget de dialogue. Si aucune scène n'est présente, on la crée,
        s'il y en a une, on la rafraichit.
        """
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
            if self.playing is not None:
                self.start.hide()

    # ------------------------------------- partie qui gère le mode de jeu humain vs humain ----------------------------

    def unlockBlackPegs(self, movablePegs):
        """
        Méthode permettant de rendre certains pions noirs sélectionnables et de montrer ces pions sélectionnables au
        joueur.
        : param movablePegs : liste de pions jouables
        """
        for i in range(len(movablePegs)):
            for item in self.blackPegs:
                Utils.selectedPegContour(i, item, movablePegs)

    def unlockWhitePegs(self, movablePegs):
        """
        Méthode permettant de rendre certains pions blancs sélectionnables et de montrer ces pions sélectionnables au
        joueur.
        : param movablePegs : liste de pions jouables
        """
        for i in range(len(movablePegs)):
            for item in self.whitePegs:
                Utils.selectedPegContour(i, item, movablePegs)

    def humanVSHuman(self, currentPlayer, nextPlayer):
        """
        Méthode permettant d'exécuter le mode de jeu où un humain joue contre un humain. Cette méthode est appelée en
        début de jeu si les 2 joueurs sont humains et lorsqu'un pion est déplacé, dans ces mêmes conditions.
        : param currentPlayer : joueur qui est en train de jouer
        : param nextPlayer : joueur suivant, qui jouera après le coup du joueur actuel
        """
        self.currentPlayer = currentPlayer
        self.nextPlayer = nextPlayer
        movablePegs = self.game.getMovablePegs(currentPlayer)
        if currentPlayer == self.WHITE:
            self.unlockWhitePegs(movablePegs)
        else:
            self.unlockBlackPegs(movablePegs)

    # ---------------------------------------------- Partie qui gère le mode de jeu AI VS AI ---------------------------

    def AIWait(self):
        """
        Méthode qui permet de faire attendre à l'IA le délai désiré avant de jouer un coup
        """
        loop = QEventLoop()
        QTimer.singleShot(self.delay * 100, loop.quit)
        loop.exec_()

    def AITimeout(self, playerID):
        """
        Méthode qui s'exécute si une IA a pris trop de temps pour jouer, et la disqualifie.
        : param playerID : l'id de joueur de l'IA
        """
        Utils.displayMessageBox("Timeout!", "L'IA a pris trop de temps pour jouer. Son adversaire a donc remporté la "
                                            "partie.")

        if playerID == 1:
            self.displayWinner(2)
        else:
            self.displayWinner(1)

    def checkTimeout(self, IA, moment, timeout):
        """
        Méthode qui permet de vérifier qu'une IA n'a pas rendu son mouvement après que le timer se soit écoulé.
        : param IA : AI qui vient de jouer le coup
        : param moment : moment auquel l'AI a trouvé son coup
        : param timeout : moment auquel l'AI a commencé à chercher son coup
        """
        if timeout > moment + self.timerValue:
            if IA is None:
                self.AITimeout(self.game.IA.playerID)
            else:
                self.AITimeout(IA.playerID)

    def IASelectMove(self, IA):
        """
        Méthode permettant à l'IA de sélectionner un mouvement et de contrôler si celle-ci l'a sélectionné dans le
        délai imparti.
        : param IA : AI qui vient de jouer le coup
        : return : le mouvement trouvé
        """
        moment = time.time()
        if IA is None:

            move = self.game.IA.selectMove()
        else:
            move = IA.selectMove()
        timeout = time.time()
        self.checkTimeout(IA, moment, timeout)
        return move

    def findPegToMove(self, move):
        """
        Méthode qui permet de trouver dans la scène quel item de PyQT correspond au pion bougé par le move.
        On commence par vérifier que le joueur ayant effectué le mouvement est l'IA. Ensuite, on itère sur ses pions,
        et lorsqu'on trouve les coordonnées scéniques du pion correspondant aux coordonnées matricielles de ce même pion
        bougé, on sauvegarde ce pion.
        : param move : mouvement du joueur
        : return : l'objet PyQt5 à bouger en fonction du mouvement du joueur (donc le pion à jouer)
        """
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
        """
        Méthode qui permet de bouger le pion dans la scène à l'endroit désiré. Tout d'abord, on itère sur les objets
        de la scène. Si cet objet est une case du plateau et que ses coordonnées scéniques correspondent aux coordonnées
        matricielles du mouvement, alors on bouge le pion à jouer sur cette case.
        : param move : mouvement du pion
        : param pegToMove : pion à jouer
        : return : la destination du pion qu'on vient de bouger
        """
        destinationX = None
        destinationY = None
        for item in self.scene.items():
            if int(item.scenePos().y() // self.SCALE) == move[1][0] and int(item.scenePos().x() // self.SCALE) == \
                    move[1][1] and type(item) == QGraphicsRectItem and pegToMove:
                destinationX = item.scenePos().x() + 15
                destinationY = item.scenePos().y() + 15
                pegToMove.setPos(destinationX, destinationY)
        return destinationX, destinationY

    def eatPegAI(self, destinationX, destinationY):
        """
        Méthode qui vérifie qu'il n'y avait pas un pion adverse à l'emplacement auquel l'IA vient de déplacer son pion.
        Tout d'abord, on commence par vérifier la couleur du joueur actuel pour ensuite itérer sur les pions du joueur
        adverse. Si on trouve un de ses pions à la position à laquelle on vient de bouger notre pion, on le supprime
        de la scène, car il vient d'être mangé.
        : param destinationX : position x du pion que l'on vient de jouer
        : param destinationY : position y du pion que l'on vient de jouer
        """
        if self.currentPlayer == self.WHITE:
            for peg in self.blackPegs:
                if peg.scenePos().x() == destinationX and peg.scenePos().y() == destinationY:
                    self.scene.removeItem(peg)
        else:
            for peg in self.whitePegs:
                if peg.scenePos().x() == destinationX and peg.scenePos().y() == destinationY:
                    self.scene.removeItem(peg)

    def IASetRoot(self, IA):
        """
        Méthode qui permet de définir la nouvelle racine de l'arbre de l'IA, qui est le coup que l'on vient de jouer.
        Si le paramètre IA vaut None, cela veut dire que l'on est dans un mode de jeu humain vs IA et que l'objet game
        n'a qu'une seule AI. Sinon, on est dans le cas AI VS AI et on doit mettre à jour la racine des deux IA de game.
        : param IA : Indicateur du mode de jeu
        """
        if IA is None:
            self.game.IA.setRoot(self.game.board, self.game)
        else:
            self.game.IA1.setRoot(self.game.board, self.game)
            self.game.IA2.setRoot(self.game.board, self.game)

    def IAMakeMove(self, IA=None):
        """
        Méthode permettant à l'IA de sélectionner un mouvement et de bouger le pion correspondant dans la scène. Si ce
        mouvement a provoqué une victoire, alors la partie s'arrête. IA vaudra None si le mode de jeu est Humain vs AI.
        : param IA : IA qui est en train de jouer dans le cas d'une partie AI vs AI.
        """
        move = self.IASelectMove(IA)
        if self.playing:
            if not move:
                self.stopGame()
            else:
                pegToMove = self.findPegToMove(move)
                destinationX, destinationY = self.movePeg(move, pegToMove)
                self.eatPegAI(destinationX, destinationY)
                self.game.makeMove(self.currentPlayer, move[0], move[1])
                self.IASetRoot(IA)
                self.moveCounter += 1

    def AIVSAI(self, currentPlayer, nextPlayer):
        """
        Méthode récursive qui permet de faire jouer 2 IA l'une contre l'autre. Chacune à leur tour, elles vont attendre
        le délai qu'elles doivent attendre avant de jouer et effectuer un coup.
        : param currentPlayer : IA qui est en train de jouer
        : param nextPlayer : IA à qui le tour viendra après currentPlayer
        """
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
        """
        Méthode qui permet de faire jouer le joueur noir qui est un humain ou une IA en cas de mode de jeu humain vs IA.
        Si le joueur humain joue, on récupère ses pions jouables et on les débloque afin qu'il puisse les sélectionner.
        Si l'IA joue, on lui fait attendre le délai défini et on lui fait jouer un coup.
        : param currentPlayer : joueur qui joue actuellement
        """
        if self.player2Type == self.HUMAN:
            movablePegs = self.game.getMovablePegs(currentPlayer)
            self.unlockBlackPegs(movablePegs)
        else:
            self.AIPlay()

    def AIPlay(self):
        """
        Méthode qui fait attendre à l'IA le délai qu'elle doit respecter avant de jouer et on lui fait jouer un coup.
        Si le coup n'a pas généré de gagnant, on appelle humainVSAI pour qu'on puisse débloquer les pions du joueur et
        le faire continuer à jouer.
        """
        self.AIWait()
        self.IAMakeMove()
        winner = self.checkWinner()
        if winner == 0:
            self.humanVSAI(self.nextPlayer, self.currentPlayer)

    def whiteProcessing(self, currentPlayer):
        """
        Méthode qui permet de faire jouer le joueur blanc qui est un humain ou une IA en cas de mode de jeu humain vs
        IA.
        Si le joueur humain joue, on récupère ses pions jouables et on les débloque afin qu'il puisse les sélectionner.
        : param currentPlayer : joueur qui joue actuellement
        """
        if self.player1Type == self.HUMAN:
            movablePegs = self.game.getMovablePegs(currentPlayer)
            self.unlockWhitePegs(movablePegs)
        else:
            self.AIPlay()

    def humanVSAI(self, currentPlayer, nextPlayer):
        """
        Méthode qui permet de faire jouer un humain contre une IA. Appelle les méthodes respectives des couleurs des
        joueurs.
        : param currentPlayer : joueur qui joue actuellement
        : param nextPlayer : joueur qui jouera au prochain tour
        """
        self.currentPlayer = currentPlayer
        self.nextPlayer = nextPlayer
        if self.currentPlayer == self.WHITE:
            self.whiteProcessing(currentPlayer)
        else:
            self.blackProcessing(currentPlayer)

    # -------------------------------------- Partie qui permet la sélection du mode de jeu -----------------------------

    def selectGameMode(self):
        """
        Méthode qui permet de sélectionner un mode de jeu en fonction des types de joueurs définis par les combo box
        au moment où l'utilisateur a cliqué sur démarrer la partie.
        """
        if self.player1Type == self.HUMAN and self.player2Type == self.HUMAN:
            self.humanVSHuman(self.WHITE, self.BLACK)
        elif self.player1Type == self.MINIMAX and self.player2Type == self.MINIMAX:
            self.AIVSAI(self.WHITE, self.BLACK)
        else:
            self.humanVSAI(self.WHITE, self.BLACK)

    # -------------------------------------- Bloc qui gère le déroulement d'une partie ---------------------------------

    def play(self):
        """
        Méthode qui permet de jouer une partie. La scène est rafraichie, les valeurs des widgets sont sauvegardées,
        un bouton stop est créé, une instance de game est créée et le mode de jeu est sélectionné.
        """
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
        """
        Méthode qui permet de débloquer certaines cases du plateau afin que le joueur puisse y déposer son pion.
        Tout d'abord, on parcourt la liste des destinations, puis on rend sélectionnable et on surligne les cases
        pour lesquelles les coordonnées scéniques correspondent aux coordonnées matricielles de la liste.
        : param destinations : liste des destinations valables pour un certain pion (donc cases à débloquer)
        """
        for i in range(len(destinations)):
            for item in self.scene.items():
                itemY = item.scenePos().y() // self.SCALE
                itemX = item.scenePos().x() // self.SCALE
                if int(itemY) == destinations[i][0] and int(itemX) == destinations[i][1] and type(item) == \
                        QGraphicsRectItem:
                    item.setFlag(QGraphicsItem.ItemIsSelectable)
                    pen = QPen(Qt.red)
                    pen.setWidth(3)
                    item.setPen(pen)

    def selectPeg(self):
        """
        Méthode qui permet de trouver la source d'un pion sélectionné et de débloquer les destinations qui lui sont
        valides.
        """
        self.pegClicked = True
        self.selectedPeg = self.scene.selectedItems()[0]
        source = [int(self.selectedPeg.scenePos().y() // self.SCALE), int(self.selectedPeg.scenePos().x() //
                                                                          self.SCALE)]
        destinations = self.game.getPossibleDestinations(self.currentPlayer, source)
        self.unlockDestinations(destinations)

    def pegHandler(self):
        """
        Méthode qui gère la sélection d'un pion. Si l'utilistateur clique sur un pion après avoir cliqué sur un pion, il
        faut bloquer toutes les destinations valides du pion précédent et débloquer toutes les destinations valides du
        pion actuel.
        """
        if self.pegClicked:
            self.lockPreviousDestinations()
            if self.player1Type == self.HUMAN and self.player2Type == self.HUMAN:
                self.humanVSHuman(self.currentPlayer, self.nextPlayer)
        self.selectPeg()

    def selectPos(self):
        """
        Méthode qui permet de trouver les coordonnées matricielles d'une source et d'une destination et d'en faire
        un mouvement. Si le mouvement est valide, on déplace le pion, sinon, on affiche un message d'erreur.
        """
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
        """
        Méthode qui permet de bloquer tous les pions du joueur qui vient de jouer son coup afin qu'il ne puisse plus
        jouer et attende son tour prochain.
        """
        for item in self.scene.items():
            if type(item) == QGraphicsEllipseItem:
                item.setFlag(QGraphicsItem.ItemIsSelectable, False)
                Utils.pegsContour(item)

    def lockPreviousDestinations(self):
        """
        Méthode qui permet de bloquer toutes les cases qui étaient valides pour un pion précédemment sélectionné et qui
        vient d'être joué.
        """
        for item in self.scene.items():
            if type(item) == QGraphicsRectItem:
                item.setFlag(QGraphicsItem.ItemIsSelectable, False)
                Utils.squareContour(item)

    def eatPegHuman(self):
        """
        Méthode qui permet de supprimer de la scène un pion qui vient d'être mangé par un joueur humain.
        """
        for item in self.scene.items():
            if type(item) == QGraphicsEllipseItem:
                if (item.scenePos().x() == self.selectedPos.scenePos().x() + 15 and item.scenePos().y() == self.
                        selectedPos.scenePos().y() + 15) and item != self.selectedPeg:
                    self.scene.removeItem(item)

    def squareHandler(self):
        """
        Méthode qui gère la sélection de cases.
        Si une IA est présente dans le jeu, sa nouvelle racine sera le mouvement qui vient d'être sélectionné.
        Si une case est cliquée après avoir cliqué sur un pion, il faut bloquer
        tous les autres pions sélectionnables et toutes les autres cases sélectionnables pour le pion.
        A la fin du traitement, on appelle le mode de jeu correspondant afin que la partie puisse se continuer.
        """
        self.selectPos()
        if self.player1Type == self.MINIMAX or self.player2Type == self.MINIMAX:
            self.game.IA.setRoot(self.game.board, self.game)
        winner = self.checkWinner()
        if winner == 0:
            self.lockPreviousPegs()
            self.lockPreviousDestinations()
            self.eatPegHuman()
            self.pegClicked = False
            if (self.player1Type == self.HUMAN and self.player2Type == self.MINIMAX) or \
                    (self.player1Type == self.MINIMAX and self.player2Type == self.HUMAN):
                self.humanVSAI(self.nextPlayer, self.currentPlayer)
            elif self.player1Type == self.HUMAN and self.player2Type == self.HUMAN:
                self.humanVSHuman(self.nextPlayer, self.currentPlayer)

    def selectionHandler(self):
        """
        Méthode qui permet de gérer la sélection d'items en fonction de leur nature. S'il s'agit d'une ellipse, on gère
        un pion, s'il s'agit d'un rectangle, on gère une case.
        """
        if len(self.scene.selectedItems()) > 0:
            if type(self.scene.selectedItems()[0]) == QGraphicsEllipseItem:
                self.pegHandler()
            else:
                self.squareHandler()

    def checkWinner(self):
        """
        Méthode qui permet d'obtenir le gagnant de la partie et de l'afficher.
        : return : le gagnant de la partie
        """
        winner = self.game.getWinner()
        if winner != 0:
            self.displayWinner(winner)
        return winner

    def stopGame(self):
        """
        Méthode qui permet d'arrêter une partie en cours. Le bouton stop est caché, le bouton start est affiché, et tous
        les pions et cases sélectionnables sont bloqués.
        """
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
        """
        Méthode qui permet d'afficher le gagnant de la partie et d'arrêter le jeu.
        : param winner : gagnant de la partie
        """
        if winner == 1:
            Utils.displayMessageBox("Gagné!", "Le joueur blanc a gagné!")
        else:
            Utils.displayMessageBox("Gagné!", "Le joueur noir a gagné!")
        self.stopGame()


"""
Explication des warnings et weak warnings:
    A. Warnings
        1.Sous Pycharm, la connexion de méthode à un widget PyQT5 provoque le warning 
"Cannot find reference 'connect' in 'function | function'". Selon mes recherches, il s'agit d'une erreur de Pycharm, 
ne s'affiche que sur cet IDE et n'entrave en rien la compréhension et l'exécution du code.
        2.Encore sous Pycharm, la récupération du string contenu dans un combobox PyQT5 provoque le warning
"Cannot find reference '[' in 'function | function | function'".Selon mes recherches, il s'agit d'une erreur de Pycharm, 
ne s'affiche que sur cet IDE et n'entrave en rien la compréhension et l'exécution du code.
    B. Weak warnings
        1. Instance attribute {attributeName} defined outside __init__: mon programme possède beaucoup de ce type de 
weak warnings: en effet, lors de la création d'un widget PyQT dans une classe, il faut qu'il soit défini en tant 
qu'attribut de classe si on veut que son affichage perdure, sinon, l'objet est détruit à la fin de l'appel de méthode 
par le garbage collector et il disparait. Donc, je définis le widget en tant qu'attribut de classe quand je le créé 
dans mon code. Il faudrait alors que je l'initialise dans ma méthode __init__(self) à None; cependant, comme j'ai une
petite quarantaine de widgets, il n'est vraiment pas propre de tous les initialiser dans __init__(self). Cependant,
ces weak warnings n'entravent en rien la lecture, la compréhension et l'exécution du code.
"""
