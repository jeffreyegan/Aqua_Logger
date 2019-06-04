# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aqua_gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.p_tank = QtWidgets.QComboBox(self.centralwidget)
        self.p_tank.setGeometry(QtCore.QRect(420, 30, 171, 26))
        self.p_tank.setToolTip("")
        self.p_tank.setObjectName("p_tank")
        self.p_method = QtWidgets.QComboBox(self.centralwidget)
        self.p_method.setGeometry(QtCore.QRect(700, 40, 81, 26))
        self.p_method.setObjectName("p_method")
        self.p_method.addItem("")
        self.p_method.addItem("")
        self.p_datetime = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.p_datetime.setGeometry(QtCore.QRect(630, 0, 151, 27))
        self.p_datetime.setObjectName("p_datetime")
        self.submit_parameters_button = QtWidgets.QPushButton(self.centralwidget)
        self.submit_parameters_button.setGeometry(QtCore.QRect(640, 530, 141, 26))
        self.submit_parameters_button.setObjectName("submit_parameters_button")
        self.logo = QtWidgets.QGraphicsView(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 391, 91))
        self.logo.setObjectName("logo")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(630, 70, 81, 51))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(630, 120, 81, 51))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(630, 220, 81, 51))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(630, 170, 81, 51))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(630, 420, 81, 51))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(630, 320, 81, 51))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(630, 370, 81, 51))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(630, 270, 81, 51))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(630, 470, 81, 51))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(630, 30, 81, 51))
        self.label_10.setObjectName("label_10")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(600, 10, 20, 531))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(420, 0, 171, 31))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(420, 50, 171, 31))
        self.label_12.setObjectName("label_12")
        self.p_parameter = QtWidgets.QComboBox(self.centralwidget)
        self.p_parameter.setGeometry(QtCore.QRect(420, 80, 171, 26))
        self.p_parameter.setToolTip("")
        self.p_parameter.setObjectName("p_parameter")
        self.p_tempf = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p_tempf.setGeometry(QtCore.QRect(720, 80, 65, 31))
        self.p_tempf.setMinimum(-1.0)
        self.p_tempf.setMaximum(150.0)
        self.p_tempf.setProperty("value", -1.0)
        self.p_tempf.setObjectName("p_tempf")
        self.p_ph = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p_ph.setGeometry(QtCore.QRect(720, 130, 65, 31))
        self.p_ph.setDecimals(1)
        self.p_ph.setMinimum(-1.0)
        self.p_ph.setMaximum(14.0)
        self.p_ph.setProperty("value", -1.0)
        self.p_ph.setObjectName("p_ph")
        self.p_ammonia = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p_ammonia.setGeometry(QtCore.QRect(720, 180, 65, 31))
        self.p_ammonia.setMinimum(-1.0)
        self.p_ammonia.setMaximum(10.0)
        self.p_ammonia.setSingleStep(0.25)
        self.p_ammonia.setProperty("value", -1.0)
        self.p_ammonia.setObjectName("p_ammonia")
        self.p_nitrite = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p_nitrite.setGeometry(QtCore.QRect(720, 230, 65, 31))
        self.p_nitrite.setMinimum(-1.0)
        self.p_nitrite.setMaximum(10.0)
        self.p_nitrite.setSingleStep(0.1)
        self.p_nitrite.setProperty("value", -1.0)
        self.p_nitrite.setObjectName("p_nitrite")
        self.p_nitrate = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p_nitrate.setGeometry(QtCore.QRect(720, 280, 65, 31))
        self.p_nitrate.setMinimum(-1.0)
        self.p_nitrate.setMaximum(200.0)
        self.p_nitrate.setSingleStep(1.0)
        self.p_nitrate.setProperty("value", -1.0)
        self.p_nitrate.setObjectName("p_nitrate")
        self.p_cu = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p_cu.setGeometry(QtCore.QRect(720, 330, 65, 31))
        self.p_cu.setMinimum(-1.0)
        self.p_cu.setMaximum(5.0)
        self.p_cu.setSingleStep(0.25)
        self.p_cu.setProperty("value", -1.0)
        self.p_cu.setObjectName("p_cu")
        self.p_tds = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p_tds.setGeometry(QtCore.QRect(720, 380, 65, 31))
        self.p_tds.setMinimum(-1.0)
        self.p_tds.setMaximum(500.0)
        self.p_tds.setProperty("value", -1.0)
        self.p_tds.setObjectName("p_tds")
        self.p_gh = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p_gh.setGeometry(QtCore.QRect(720, 430, 65, 31))
        self.p_gh.setMinimum(-1.0)
        self.p_gh.setMaximum(300.0)
        self.p_gh.setProperty("value", -1.0)
        self.p_gh.setObjectName("p_gh")
        self.p_kh = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p_kh.setGeometry(QtCore.QRect(720, 480, 65, 31))
        self.p_kh.setMinimum(-1.0)
        self.p_kh.setMaximum(300.0)
        self.p_kh.setProperty("value", -1.0)
        self.p_kh.setObjectName("p_kh")
        self.plot_widget = QtWidgets.QWidget(self.centralwidget)
        self.plot_widget.setGeometry(QtCore.QRect(10, 120, 581, 421))
        self.plot_widget.setObjectName("plot_widget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Aqua Logger"))
        self.p_method.setItemText(0, _translate("MainWindow", "Reagent"))
        self.p_method.setItemText(1, _translate("MainWindow", "Strip"))
        self.submit_parameters_button.setText(_translate("MainWindow", " Submit Parameters"))
        self.label.setText(_translate("MainWindow", "Temperature\n"
"Fahrenheit"))
        self.label_2.setText(_translate("MainWindow", "Acidity\n"
"pH"))
        self.label_3.setText(_translate("MainWindow", "Nitrite\n"
"NO2- ppm"))
        self.label_4.setText(_translate("MainWindow", "Ammonia\n"
"NH3/NH4+"))
        self.label_5.setText(_translate("MainWindow", "General H.\n"
" GH ppm"))
        self.label_6.setText(_translate("MainWindow", "Copper\n"
"Cu+ ppm"))
        self.label_7.setText(_translate("MainWindow", "TDS ppm"))
        self.label_8.setText(_translate("MainWindow", "Nitrate\n"
"NO3- ppm"))
        self.label_9.setText(_translate("MainWindow", "Carbonate H.\n"
" KH ppm"))
        self.label_10.setText(_translate("MainWindow", "Method"))
        self.label_11.setText(_translate("MainWindow", "Aquarium Tank"))
        self.label_12.setText(_translate("MainWindow", "Parameter to Plot"))

