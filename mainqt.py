from PyQt5 import QtWidgets, QtGui, QtCore
import sys

from interfaz.interfaz import Ui_MainWindow
from archivos import leer_cfg, guardar_cfg, eliminar_cfg, editar_cfg, buscar_cfg
from cfg import ejecutar_cfg, string_to_cfg


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Interfaz grafica
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Tamaño de la pantalla
        self.setFixedSize(801, 452)

        # Placeholder multilinea
        placeholder = """S -> 'a' S | T
T -> 'b'"""
        self.ui.textEditCFG.setPlaceholderText(placeholder)

        # Atributos
        self.cfg = None
        self.cadena = None
        self.lista_cfg = None

        # Eventos
        self.ui.textEditCFG.textChanged.connect(self.actualizar_cfg)

        self.ui.lineEditCadena.textChanged.connect(self.validar_cadena)

        # self.ui.btnGraficarArbol.clicked.connect(self.graficar_arbol)

        self.ui.btnGuardarCFG.clicked.connect(self.guardar_cfg)

        # self.ui.listViewCFG.clicked.connect(self.seleccionar_cfg)
        self.ui.tableWidget.clicked.connect(self.seleccionar_cfg)

        # Funciones a realizar cuando se abre el programa
        self.cargar_cfgs()


    def actualizar_cfg(self):

        try:
            self.cfg = string_to_cfg(self.ui.textEditCFG.toPlainText())
            self.ui.lineEditCFGVF.setText("La grámatica es válida")
            self.ui.lineEditCFGVF.setStyleSheet('color: green; font: 10pt "MS Shell Dlg 2"')

        except Exception as ex:
            print(ex)
            self.ui.lineEditCFGVF.setText("La grámatica es inválida")
            self.ui.lineEditCFGVF.setStyleSheet('color: red; font: 10pt "MS Shell Dlg 2"')


    def validar_cadena(self):

        self.cadena = self.ui.lineEditCadena.text()

        resultado = ejecutar_cfg(self.cfg, self.cadena, graficar=False)

        if resultado:
            self.ui.lineEditCadenaVF.setText("La grámatica genera la cadena")
            self.ui.lineEditCadenaVF.setStyleSheet('color: green; font: 10pt "MS Shell Dlg 2"')

        else:
            self.ui.lineEditCadenaVF.setText("La grámatica no genera la cadena")
            self.ui.lineEditCadenaVF.setStyleSheet('color: red; font: 10pt "MS Shell Dlg 2"')


    def graficar_arbol(self):

        ejecutar_cfg(self.cfg, self.cadena, graficar=True)


    def guardar_cfg(self):

        text, ok = QtWidgets.QInputDialog().getText(self, "Guardar", "Descripción del CFG",
                                                    QtWidgets.QLineEdit.Normal)

        if ok:
            cfg = self.ui.textEditCFG.toPlainText()

            if text:
                guardar_cfg(cfg, text)
            else:
                guardar_cfg(cfg, cfg)

            self.cargar_cfgs()


    def seleccionar_cfg(self):

        index = self.ui.tableWidget.currentIndex().row()

        cfg = self.lista_cfg[index]['cfg']

        self.ui.textEditCFG.setText(cfg)


    def cargar_cfgs(self):

        self.lista_cfg = leer_cfg()

        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setRowCount(len(self.lista_cfg))

        self.ui.tableWidget.setColumnWidth(0, 280)

        self.ui.tableWidget.setHorizontalHeaderLabels(['Descripción'])

        self.ui.tableWidget.resizeRowsToContents()

        row = 0

        for cfg in self.lista_cfg:

            descripcion = QtWidgets.QTableWidgetItem(cfg['descripcion'])

            descripcion.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.ui.tableWidget.setItem(row, 0, descripcion)

            row += 1


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    application = MainWindow()
    application.show()

    sys.exit(app.exec())
