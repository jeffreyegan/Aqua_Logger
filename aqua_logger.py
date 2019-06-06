import sys, os
from PyQt5 import QtWidgets, QtCore, uic
import sqlite3
#from datetime import datetime
from aqua_logger_gui import Ui_MainWindow
import numpy as np
import pandas as pd
import random, time



from matplotlib import pyplot as plt
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import seaborn as sns
sns.set(style="darkgrid")
sns.axes_style({'text.color': '0.99'})
sns.set_context("notebook", font_scale=0.65, rc={"lines.linewidth": 1.0})
palette = sns.color_palette("mako_r", 6)


# pyuic5 aqua_gui.ui -o aqua_logger_gui.py  # run this on updated *.ui files before executing this main script

#TODO icon, plot, nulls, logo, bounds for parameters to tanks table and plot

class aqua_logger(QtWidgets.QMainWindow):
    def __init__(self):
        super(aqua_logger, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.update_time()
        self.connect_to_database()
        self.list_tanks()
        self.list_parameters()

        self.fig_dpi = 120  # figure resolution in dots per inch
        self.fig = Figure(figsize=(581/self.fig_dpi,421/self.fig_dpi), dpi=self.fig_dpi, facecolor='#505050', edgecolor='#505050')
        self.ax1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.ui.plot_widget)

        self.refresh_plot()
        self.ui.submit_parameters_button.clicked.connect(self.update_parameters)  # Submit Button
        self.ui.p_parameter.currentIndexChanged.connect(self.refresh_plot)  # Change Parameter
        self.ui.p_tank.currentIndexChanged.connect(self.refresh_plot)  # Change Tank
        #self.about()

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
        self.param_units = {  # dictionary of units for selected parameter - used in y-axis of plots
            "Temp - F": "Degrees Fahrenheit",
            "Temp - C": "Degrees Celcius",
            "Acidity - pH": "pH",
            "Ammonia": "Ammonia ppm",
            "Nitrite": "Nitrite ppm",
            "Nitrate": "Nitrate ppm",
            "Copper": "Copper ppm",
            "Total Disolved Solids": "TDS ppm",
            "General Hardness": "GH ppm",
            "Carbonate Hardness": "KH ppm"
        }
        for key in self.tank_params:  # for key in dict, additem to drop down
            self.ui.p_parameter.addItem(key)
        self.ui.p_tank.setCurrentIndex(0)

    def refresh_plot(self):
        self.ui.plot_widget.update()
        # tank id to plot data for
        q = "SELECT tank_id FROM tanks WHERE tank_name == \""+str(self.ui.p_tank.currentText())+"\""
        self.cur.execute(q)
        rows = self.cur.fetchall()
        self.tank_id = int(rows[0][0])

        # parameter data to plot
        print(str(self.tank_params[self.ui.p_parameter.currentText()]))
        q = "SELECT * FROM ( SELECT measurement_time, "+str(self.tank_params[self.ui.p_parameter.currentText()])+" FROM measurements WHERE tank_id == "+str(self.tank_id)+" ORDER BY measurement_id DESC LIMIT 10) ORDER BY measurement_time ASC"
        #TODO eventually needs some time bounding on the query or no recent data will be seen
        plot_df = pd.read_sql_query(q, self.conn)

        self.ax1.clear()
        sns.lineplot(x="measurement_time", y=str(self.tank_params[self.ui.p_parameter.currentText()]), data=plot_df, palette=palette, ax=self.ax1)
        self.ax1.set_title(str(self.ui.p_tank.currentText())+" - "+str(self.ui.p_parameter.currentText()))
        self.ax1.set_ylabel(self.param_units[self.ui.p_parameter.currentText()])
        plot_df['time_label'] = plot_df['measurement_time'].apply(lambda x: str(x.split("/")[0])+"/"+str(x.split("/")[1]))
        xlabels = plot_df['time_label']
        self.ax1.set_xticklabels(xlabels, rotation=0)

        self.canvas.draw()
        self.ui.plot_widget.repaint()
        
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
        self.refresh_plot()

        self.update_time()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", "Open Source Aquarium Water Paramter Tracking tool written by Jeffrey Egan. 2019")


app = QtWidgets.QApplication([])
application = aqua_logger()
application.show()
sys.exit(app.exec())

