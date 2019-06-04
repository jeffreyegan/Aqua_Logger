import sys, os
from PyQt5 import QtWidgets, QtCore, uic
import sqlite3
#from datetime import datetime
from aqua_logger_gui import Ui_MainWindow


# pyuic5 aqua_gui.ui -o aqua_logger_gui.py  # run this on updated *.ui files before executing this main script

#TODO icon, plot, nulls, logo

class aqua_logger(QtWidgets.QMainWindow):
    def __init__(self):
        super(aqua_logger, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.update_time()
        self.connect_to_database()
        self.list_tanks()
        self.list_parameters()
        self.ui.submit_parameters_button.clicked.connect(self.update_parameters)  # Submit Button

    def update_time(self):  # update the date time object field in the GUI to present time (local)
        now = QtCore.QDateTime.currentDateTime()
        self.ui.p_datetime.setDateTime(now)

    def update_parameters(self):  # methods to call when update parameters button is pushed by user
        self.ui.p_ph.setValue(7.9)
        self.update_time()
        self.add_measurement()

    def connect_to_database(self):  # connect to the sqlite database file
        db_file = "aqua_data.db"
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def list_tanks(self):  # populate list of tanks available in drop down list from database
        q = "SELECT tank_name FROM tanks"
        self.cur.execute(q)
        rows = self.cur.fetchall()
        for row_idx in range(len(rows)):
            self.ui.p_tank.addItem(rows[row_idx][0])
        self.ui.p_tank.setCurrentIndex(0)

    def list_parameters(self):  # populate list of parameters in database available for plotting
        self.tank_params = {  # dictionary of text to sql column names
            "Temp - F": "temp_f",
            "Temp - C": "temp_c",
            "Acidity - pH": "pH",
            "Ammonia": "ammonia",
            "Nitrite": "nitrite",
            "Nitrate": "nitrate",
            "Copper": "copper",
            "Total Disolved Solids": "tds",
            "General Hardness": "gh",
            "Carbonate Hardness": "kh"
        }

        for key in self.tank_params:  # for key in dict, additem to drop down
            self.ui.p_parameter.addItem(key)
        self.ui.p_tank.setCurrentIndex(0)

    def plot_data(self):
        q = "SELECT tank_id FROM tanks WHERE tank_name == \""+str(self.ui.p_tank.currentText())+"\""
        self.cur.execute(q)
        rows = self.cur.fetchall()
        self.tank_id = int(rows[0][0])

        q = "SELECT "+str(self.tank_params[self.ui.p_parameter.currentText()])+" FROM measurements WHERE tank_id == "+str(self.tank_id)
        #TODO eventually needs some time bounding on the query or no recent data will be seen
        self.cur.execute(q)
        rows = self.cur.fetchall()
        
        

        # call current tank and param to make a plot

        # on update, replot


    def add_measurement(self):  # add measurement data to the sqlite database file
        q = "SELECT tank_id FROM tanks WHERE tank_name == \""+str(self.ui.p_tank.currentText())+"\""
        self.cur.execute(q)
        rows = self.cur.fetchall()
        self.tank_id = int(rows[0][0])

        dt_string = self.ui.p_datetime.dateTime().toString(self.ui.p_datetime.displayFormat())  # mm/dd/yy hh:mm"
        q = ("INSERT INTO measurements (tank_id, measurement_time, method, temp_f, temp_c, pH, ammonia, nitrite, nitrate, copper, tds, gh, kh) " + 
        "VALUES ("+str(self.tank_id)+", \""+dt_string+"\", \""+str(self.ui.p_method.currentText())+"\", "+str(self.ui.p_tempf.value())+", "+str((self.ui.p_tempf.value()-32.0)*5.0/9.0)+", "+str(self.ui.p_ph.value())+", "+str(self.ui.p_ammonia.value())+", "+str(self.ui.p_nitrite.value())+", "+str(self.ui.p_nitrate.value())+", "+str(self.ui.p_cu.value())+", "+str(self.ui.p_tds.value())+", "+str(self.ui.p_gh.value())+", "+str(self.ui.p_kh.value())+")")
        print(q)
        #TODO still need to handle nulls better, instead of 0 s
        self.cur.execute(q)
        self.conn.commit()
        self.plot_data()

        self.update_time()



app = QtWidgets.QApplication([])
application = aqua_logger()
application.show()
sys.exit(app.exec())

