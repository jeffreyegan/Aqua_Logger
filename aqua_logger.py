import sys
import os
from PyQt5 import QtWidgets, uic
import sqlite3

qt_gui_file = "gui_main.ui"

app = QtWidgets.QApplication([])
win = uic.loadUi(qt_gui_file)
win.show()
sys.exit(app.exec())





'''Ui_MainWindow, QtBaseClass = uic.loadUi(qt_gui_file)


class AquaLogger(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.submit_parameters_button.clicked.connect(self.Update_Parameters)

    def Update_Parameters(self):
        return

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())'''
