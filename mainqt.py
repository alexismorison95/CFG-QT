from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import os

from interfaz.interfaz import Ui_MainWindow
from ayuda import Ayuda

from archivos import leer, guardar, editar, eliminar
from cfg import ejecutar_cfg, string_to_cfg


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Interfaz grafica
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Iconos
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap('./interfaz/chime_in.png')))
        self.ui.actionComo_usar.setIcon(QtGui.QIcon('./interfaz/question1.png'))
        self.ui.actionAcerca_de.setIcon(QtGui.QIcon('./interfaz/info1.png'))

        # Tamaño de la pantalla
        self.setFixedSize(871, 452)

        # Atributos
        self.cfg = None
        self.cadena = None
        self.lista_cfg = None
        self.cfg_seleccionado = None
        self.editar_cfg = False

        # Placeholder multilinea
        placeholder = """S -> 'a' S | T
T -> 'b'"""
        self.ui.textEditCFG.setPlaceholderText(placeholder)

        # Eventos
        self.ui.textEditCFG.textChanged.connect(self.actualizar_cfg)

        self.ui.lineEditCadena.textChanged.connect(self.validar_cadena)

        self.ui.btnGraficar.clicked.connect(self.graficar_arbol)

        self.ui.btnGuardarCFG.clicked.connect(self.guardar_cfg)

        self.ui.tableWidget.clicked.connect(self.seleccionar_cfg)

        self.ui.btnEliminarCFG.clicked.connect(self.eliminar_cfg)

        self.ui.btnNuevoCFG.clicked.connect(self.nuevo_cfg)

        self.ui.btnArchivos.clicked.connect(self.abrir_archivos)

        self.ui.actionComo_usar.triggered.connect(self.abrir_ayuda)

        # Funciones a realizar cuando se abre el programa
        self.cargar_cfgs()

        self.ui.textEditCFG.setFocus()


    def abrir_ayuda(self):

        ayuda = Ayuda()
        ayuda.setModal(False)
        ayuda.exec()


    def abrir_archivos(self):

        actual_path = os.path.abspath(os.getcwd())

        os.startfile(actual_path + "/res")


    def nuevo_cfg(self):

        self.ui.textEditCFG.setText("")
        self.ui.lineEditCFGVF.setText("")

        self.editar_cfg = False
        self.cfg = None


    def eliminar_cfg(self):

        if self.editar_cfg:

            index = self.ui.tableWidget.currentIndex().row()

            eliminar(self.lista_cfg, index)

            self.ui.textEditCFG.setText("")
            self.ui.lineEditCFGVF.setText("")

            self.editar_cfg = False
            self.cfg = None

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

        if self.cfg:
            self.cadena = self.ui.lineEditCadena.text()

            resultado = ejecutar_cfg(self.cfg, self.cadena, graficar=False)

            if resultado:
                self.ui.lineEditCadenaVF.setText("La grámatica genera la cadena")
                self.ui.lineEditCadenaVF.setStyleSheet('color: green; font: 10pt "MS Shell Dlg 2"')

            else:
                self.ui.lineEditCadenaVF.setText("La grámatica no genera la cadena")
                self.ui.lineEditCadenaVF.setStyleSheet('color: red; font: 10pt "MS Shell Dlg 2"')

        else:
            self.ui.lineEditCadenaVF.setText("")


    def graficar_arbol(self):

        ejecutar_cfg(self.cfg, self.cadena, graficar=True)


    def guardar_cfg(self):

        text, ok = QtWidgets.QInputDialog().getText(
            self,
            "Guardar",
            "Descripción del CFG",
            QtWidgets.QLineEdit.Normal
        )

        if ok:

            if self.editar_cfg:

                index = self.ui.tableWidget.currentIndex().row()

                obj = self.cfg_seleccionado
                obj['cfg'] = self.ui.textEditCFG.toPlainText()
                obj['descripcion'] = text

                editar(self.lista_cfg, obj, index)

            else:
                cfg = self.ui.textEditCFG.toPlainText()

                if text:
                    guardar(cfg, text)
                else:
                    guardar(cfg, cfg)

            self.cargar_cfgs()


    def seleccionar_cfg(self):

        index = self.ui.tableWidget.currentIndex().row()

        cfg = self.lista_cfg[index]['cfg']

        self.cfg_seleccionado = self.lista_cfg[index]

        self.editar_cfg = True

        self.ui.textEditCFG.setText(cfg)


    def cargar_cfgs(self):

        self.lista_cfg = leer()

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
