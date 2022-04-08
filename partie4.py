"""
Nom: De Keyser
Prénom: Maeva
Matricule: 000454537
Section: BA INFO
"""
import sys

from PyQt5.QtWidgets import QApplication

from GUI import App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App(app)
    sys.exit(app.exec_())
