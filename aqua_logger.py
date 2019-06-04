import sys, os
from PyQt5 import QtWidgets, QtCore, uic
import sqlite3
#from datetime import datetime
from aqua_logger_gui import Ui_MainWindow


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.update_time()  # Set datetime field in the GUI on startup
        self.connect_to_database()  # Connect to the SQLite db file
        self.ui.submit_parameters_button.clicked.connect(self.update_parameters)  # Submit Button

    def update_time(self):
        now = QtCore.QDateTime.currentDateTime()
        self.ui.p_datetime.setDateTime(now)

    def update_parameters(self):
        self.ui.p_ph.setValue(7.9)
        self.update_time()
        self.add_measurement()

    def connect_to_database(self):
        db_file = "aqua_data.db"
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def add_measurement(self):
        dt_string = self.ui.p_datetime.dateTime().toString(self.ui.p_datetime.displayFormat())  # mm/dd/yy hh:mm"
        q = ("INSERT INTO measurements (tank_id, measurement_time, method, temp_f, temp_c, pH, ammonia, nitrite, nitrate, copper, tds, gh, kh) " + 
        "VALUES (1, \""+dt_string+"\", \""+str(self.ui.p_method.currentText())+"\", "+str(self.ui.p_tempf.value())+", "+str((self.ui.p_tempf.value()-32.0)*5.0/9.0)+", "+str(self.ui.p_ph.value())+", "+str(self.ui.p_ammonia.value())+", "+str(self.ui.p_nitrite.value())+", "+str(self.ui.p_nitrate.value())+", "+str(self.ui.p_cu.value())+", "+str(self.ui.p_tds.value())+", "+str(self.ui.p_gh.value())+", "+str(self.ui.p_kh.value())+")")
        print(q)
        self.cur.execute(q)
        self.conn.commit()



app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())

