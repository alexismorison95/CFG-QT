from PyQt5 import QtWidgets

from interfaz.ayuda import Ui_Dialog


class Ayuda(QtWidgets.QDialog):

    def __init__(self):
        super(Ayuda, self).__init__()

        # Interfaz grafica
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

