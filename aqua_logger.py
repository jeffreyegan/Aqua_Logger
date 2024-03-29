#!/usr/bin/env python
__author__ = "Jeffrey Egan"
__copyright__ = "Copyright 2019, dragonaur.io"
__credits__ = ["Jeffrey Egan"]
__license__ = "Apache-2.0"
__version__ = "1.0.0"
__maintainer__ = "Rob Knight"
__email__ = "jeffrey.a.egan@gmail.com"
__status__ = "Released"

# Helpful command lines for configuration
# pyuic5 aqua_gui.ui -o aqua_logger_gui.py  # run this on updated *.ui files before executing this main script
# convert -strip input.png output.png  # run on images to address any PNG lib errors

#TODO bounds for parameters to tanks table and plot

# Standard Imports
import sys, os, math
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sqlite3
from aqua_logger_gui import Ui_MainWindow
import numpy as np
import pandas as pd

# Plotting Library Imports and Configuration
from matplotlib import pyplot as plt
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
import seaborn as sns
sns.set(style="darkgrid")
sns.axes_style({'text.color': '0.99'})
sns.set_context("notebook", font_scale=0.65, rc={"lines.linewidth": 1.0})
palette = sns.color_palette("mako_r", 6)

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
        self.fig = Figure(figsize=(581/self.fig_dpi,421/self.fig_dpi), dpi=self.fig_dpi, facecolor='#31363b', edgecolor='#31363b')
        self.ax1 = self.fig.add_subplot(111)
        #self.fig.subplots_adjust(left=0.1, right=0.2, top=0.2, bottom=0.1)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.ui.plot_widget)

        self.label = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("aqua_logger_logo_o.png")  # _o for opaque matching dark breath #31363b, w/o _o is transparent
        self.label.setPixmap(self.pixmap)
        self.label.setParent(self.ui.logo)

        self.ui.submit_parameters_button.clicked.connect(self.add_measurement)  # Submit Button
        self.ui.p_parameter.currentIndexChanged.connect(self.refresh_plot)  # Change Parameter
        self.ui.p_tank.currentIndexChanged.connect(self.refresh_plot)  # Change Tank
        self.refresh_plot()
        #self.about()

    def update_time(self):  # update the date time object field in the GUI to present time (local)
        now = QtCore.QDateTime.currentDateTime()
        self.ui.p_datetime.setDateTime(now)

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
        self.gh_kh_reagent = {  # dictionary to map the # of drops reagent to ppm
            "1.0": "17.9",
            "2.0": "35.8",
            "3.0": "53.7",
            "4.0": "71.6",
            "5.0": "89.5",
            "6.0": "107.4",
            "7.0": "125.3",
            "8": "143.2",
            "9.0": "161.1",
            "10.0": "179.0",
            "11.0": "196.9",
            "12.0": "214.8",
            "-1.0": "-1.0"
        }

    def refresh_plot(self):  # refreshes the GUI plot based on tank or parameter selection update by user
        self.ui.plot_widget.update()
        # tank id to plot data for
        q = "SELECT tank_id FROM tanks WHERE tank_name == \""+str(self.ui.p_tank.currentText())+"\""
        self.cur.execute(q)
        rows = self.cur.fetchall()
        self.tank_id = int(rows[0][0])

        # parameter data to plot
        q = "SELECT * FROM ( SELECT measurement_time, "+str(self.tank_params[self.ui.p_parameter.currentText()])+" FROM measurements WHERE (tank_id == "+str(self.tank_id)+" AND "+str(self.tank_params[self.ui.p_parameter.currentText()])+" NOT NULL) ORDER BY measurement_id DESC LIMIT 10) ORDER BY measurement_time ASC"
        plot_df = pd.read_sql_query(q, self.conn)
        if plot_df.empty:
            self.no_data()
        else:
            self.ax1.clear()
            sns.lineplot(x="measurement_time", y=str(self.tank_params[self.ui.p_parameter.currentText()]), data=plot_df, palette=palette, ax=self.ax1)
            self.ax1.set_title(str(self.ui.p_tank.currentText())+" - "+str(self.ui.p_parameter.currentText()), color="white")
            self.ax1.set_ylabel(self.param_units[self.ui.p_parameter.currentText()], color="white")
            self.ax1.set_xlabel("Date of Data Record", color="white")
            plot_df['time_label'] = plot_df['measurement_time'].apply(lambda x: str(x.split("/")[0])+"/"+str(x.split("/")[1]))
            xlabels = plot_df['time_label']
            ylabels = np.linspace(math.floor(min(plot_df[str(self.tank_params[self.ui.p_parameter.currentText()])])), math.ceil(max(plot_df[str(self.tank_params[self.ui.p_parameter.currentText()])])), 5)
            self.ax1.set_xticklabels(xlabels, rotation=0, color="white")
            self.ax1.tick_params(axis="y", colors="white")
            self.ax1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
            self.canvas.draw()
            self.ui.plot_widget.repaint()
        
    def add_measurement(self):  # add measurement data to the sqlite database file
        q = "SELECT tank_id FROM tanks WHERE tank_name == \""+str(self.ui.p_tank.currentText())+"\""
        self.cur.execute(q)
        rows = self.cur.fetchall()
        self.tank_id = int(rows[0][0])
        dt_string = self.ui.p_datetime.dateTime().toString(self.ui.p_datetime.displayFormat())  # mm/dd/yy hh:mm"

        if str(self.ui.p_method.currentText()) == "Strip":  # if reagent, 
            q = ("INSERT INTO measurements (tank_id, measurement_time, method, temp_f, temp_c, pH, ammonia, nitrite, nitrate, copper, tds, gh, kh) " + 
            "VALUES ("+str(self.tank_id)+", \""+dt_string+"\", \""+str(self.ui.p_method.currentText())+"\", "+str(self.ui.p_tempf.value())+", "+str((self.ui.p_tempf.value()-32.0)*5.0/9.0)+", "+str(self.ui.p_ph.value())+", "+str(self.ui.p_ammonia.value())+", "+str(self.ui.p_nitrite.value())+", "+str(self.ui.p_nitrate.value())+", "+str(self.ui.p_cu.value())+", "+str(self.ui.p_tds.value())+", "+str(self.ui.p_gh.value())+", "+str(self.ui.p_kh.value())+")")
        else:
            gh = self.gh_kh_reagent[str(self.ui.p_gh.value())]
            kh = self.gh_kh_reagent[str(self.ui.p_kh.value())]
            q = ("INSERT INTO measurements (tank_id, measurement_time, method, temp_f, temp_c, pH, ammonia, nitrite, nitrate, copper, tds, gh, kh) " + 
            "VALUES ("+str(self.tank_id)+", \""+dt_string+"\", \""+str(self.ui.p_method.currentText())+"\", "+str(self.ui.p_tempf.value())+", "+str((self.ui.p_tempf.value()-32.0)*5.0/9.0)+", "+str(self.ui.p_ph.value())+", "+str(self.ui.p_ammonia.value())+", "+str(self.ui.p_nitrite.value())+", "+str(self.ui.p_nitrate.value())+", "+str(self.ui.p_cu.value())+", "+str(self.ui.p_tds.value())+", "+str(gh)+", "+str(kh)+")")

        self.cur.execute(q)
        self.conn.commit()
        self.set_nulls()
        self.refresh_plot()
        self.update_time()
        self.confirm()

    def set_nulls(self):  # replace -1.0 values with NULLs
        for key, value in self.tank_params.items():
            q = "UPDATE measurements SET "+str(value)+" = NULL where "+str(value)+" = -1.0;"
            self.cur.execute(q)
            q = "UPDATE measurements SET temp_c = NULL where temp_f IS NULL;"
            self.cur.execute(q)
            self.conn.commit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", "Open Source Aquarium Water Paramter Tracking tool written by Jeffrey Egan. 2019")
    
    def confirm(self):
        QtWidgets.QMessageBox.about(self, "Success", "Aquarium water parameters successfully added to database!")

    def no_data(self):
        QtWidgets.QMessageBox.about(self, "Information", "Database has no valid records for this tank and water parameter combination. Add measurements to the database to enable plotting.")


app = QtWidgets.QApplication([])
application = aqua_logger()
application.show()
sys.exit(app.exec())
