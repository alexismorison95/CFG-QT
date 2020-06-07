from PyQt5 import QtWidgets, QtGui
import sys
import json

from interfaz.interfaz import Ui_MainWindow
from funciones import ejecutar_cfg, string_to_cfg, leer_json_cfg, guardar_json_cfg


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Interfaz grafica
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Tamaño de la pantalla
        self.setFixedSize(720, 401)

        # Placeholder multilinea
        placeholder = """S -> 'a' S | T
T -> 'b'"""
        self.ui.textEditCFG.setPlaceholderText(placeholder)

        # Atributos
        self.cfg = None
        self.cadena = None

        # Eventos
        self.ui.textEditCFG.textChanged.connect(self.actualizar_cfg)

        self.ui.lineEditCadena.textChanged.connect(self.validar_cadena)

        self.ui.btnGraficarArbol.clicked.connect(self.graficar_arbol)

        self.ui.btnGuardarCFG.clicked.connect(self.guardar_cfg)

        self.ui.listViewCFG.clicked.connect(self.seleccionar_cfg)

        # Funciones a realizar cuando se abre el programa
        self.cargar_cfgs()

    def actualizar_cfg(self):

        try:
            self.cfg = string_to_cfg(self.ui.textEditCFG.toPlainText())
            self.ui.labelInfoCFG.setText("Gramatica correcta")

        except Exception as ex:
            print(ex)
            self.ui.labelInfoCFG.setText("Gramatica incorrecta")

    def validar_cadena(self):

        self.cadena = self.ui.lineEditCadena.text()

        resultado = ejecutar_cfg(self.cfg, self.cadena, graficar=False)

        if resultado:
            self.ui.labelCadenaVF.setText("La gramatica genera la cadena")
        else:
            self.ui.labelCadenaVF.setText("La gramatica no genera la cadena")

    def graficar_arbol(self):

        ejecutar_cfg(self.cfg, self.cadena, graficar=True)

    def guardar_cfg(self):

        cfg = self.ui.textEditCFG.toPlainText()

        guardar_json_cfg(cfg)

        self.cargar_cfgs()

    def seleccionar_cfg(self):

        print(self.ui.listViewCFG.currentIndex().data())

        self.ui.textEditCFG.setText(self.ui.listViewCFG.currentIndex().data())

    def cargar_cfgs(self):

        model = QtGui.QStandardItemModel()
        self.ui.listViewCFG.setModel(model)

        lista = leer_json_cfg()

        for cfg in lista:

            item = QtGui.QStandardItem(cfg)
            model.appendRow(item)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    application = MainWindow()
    application.show()

    sys.exit(app.exec())
