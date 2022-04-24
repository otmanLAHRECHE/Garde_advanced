import datetime
import sqlite3

from PyQt5 import QtWidgets, uic, QtGui, Qt, QtCore
from calendar import monthrange

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, qApp, QMessageBox

import app
from dialogs import CustomDialog, Saving_progress_dialog, Threading_loading

import os

from threads import Thread_load_guards, Thread_create_guard
from widgets import Chose_worker


class GuardUi(QtWidgets.QMainWindow):
    def __init__(self, service, month, year):
        super(GuardUi, self).__init__()
        uic.loadUi("./user_interfaces/planing_garde.ui", self)

        self.want_to_close = False
        self.days_of_week = "Dimanche" + "  " + "Lundi" + "  " + "Mardi" + "  " + "Mercredi" + "  " + "Jeudi"

        self.ttl = self.findChild(QtWidgets.QLabel, "label")
        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.save = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.save.setIcon(QIcon("./asstes/images/save.png"))
        self.exportPd = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.exportPd.setIcon(QIcon("./asstes/images/download.png"))
        self.auto = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.auto.setIcon(QIcon("./asstes/images/auto.png"))
        self.table.setColumnWidth(2, 220)
        self.table.setColumnWidth(3, 220)

        self.month = month
        self.year = year
        self.service = service
        self.num_days = monthrange(self.year, self.month)[1]

        if self.month == 1:
            m = "janvier"
        elif self.month == 2:
            m = "février"
        elif self.month == 3:
            m = "mars"
        elif self.month == 4:
            m = "avril"
        elif self.month == 5:
            m = "mai"
        elif self.month == 6:
            m = "juin"
        elif self.month == 7:
            m = "juillet"
        elif self.month == 8:
            m = "août"
        elif self.month == 9:
            m = "septembre"
        elif self.month == 10:
            m = "octobre"
        elif self.month == 11:
            m = "novembre"
        elif self.month == 12:
            m = "décembre"

        if self.service == "urgence":
            self.ttl.setText("Planing de garde urgence mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "dentiste":
            self.ttl.setText("Planing de garde chirurgie dentaire mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "labo":
            self.ttl.setText("Planing de garde laboratoire mois " + str(m) + "/" + str(self.year) + ":")


        elif self.service == "radio":
            self.ttl.setText("Planing de garde radiologie mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "admin":
            self.ttl.setText("Planing de garde administration mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "dentiste_inf":
            self.ttl.setText("Planing de garde infirmiers dentaire mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "inf":
            self.ttl.setText("EPSP Djanet ( Infirmiers d'urgences )")
            self.ttl.setText("Planing de garde infirmiers d'urgences mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "pharm":
            self.ttl.setText("Planing de garde pharmacie mois " + str(m) + "/" + str(self.year) + ":")


        self.load_med()
        self.load_guards()
        self.exportPd.clicked.connect(self.export)

        self.save.clicked.connect(self.save_)
        self.auto.clicked.connect(self.auto_)

    def load_guards(self):
        self.dialog = Threading_loading()
        self.dialog.ttl.setText("إنتظر من فضلك")
        self.dialog.progress.setValue(0)
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()

        self.thr2 = Thread_load_guards(self.service, self.num_days, self.month, self.year)
        self.thr2._signal.connect(self.signal_accepted_load)
        self.thr2._signal_status.connect(self.signal_accepted_load)
        self.thr2._signal_finish.connect(self.signal_accepted_load)
        self.thr2.start()

    def load_med(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        sql_q = 'SELECT full_name FROM health_worker where service=?'
        cur.execute(sql_q, (self.service,))
        self.medcins = cur.fetchall()
        connection.close()

    def save_(self):
        self.want_to_close = True
        self.dialog = Threading_loading()
        self.dialog.ttl.setText("إنتظر من فضلك")
        self.dialog.progress.setValue(0)
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()

        self.thr = Thread_create_guard(self.service, self.num_days, self.month, self.year, self.table)
        self.thr._signal.connect(self.signal_accepted)
        self.thr._signal_status.connect(self.signal_accepted)
        self.thr.start()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        message = "Votre liste de garde na pas sauvgarder, es-tu sûr de quiter"
        dialog = CustomDialog(message)
        if not self.want_to_close:
            if dialog.exec():
                self.next_page = app.AppUi()
                self.next_page.show()
                self.close()
            else:
                a0.ignore()
        else:
            self.next_page = app.AppUi()
            self.next_page.show()
            self.close()

    def signal_accepted(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            self.dialog.close()

    def signal_accepted_load(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:
            row = progress[0]
            results_light = progress[1]
            results_night = progress[2]

            day = row + 1
            x = datetime.datetime(self.year, self.month, day)
            m = ""
            if x.strftime("%A") == "Saturday":
                m = "Samedi"
            elif x.strftime("%A") == "Sunday":
                m = "Dimanche"
            elif x.strftime("%A") == "Monday":
                m = "Lundi"
            elif x.strftime("%A") == "Tuesday":
                m = "Mardi"
            elif x.strftime("%A") == "Wednesday":
                m = "Mercredi"
            elif x.strftime("%A") == "Thursday":
                m = "Jeudi"
            elif x.strftime("%A") == "Friday":
                m = "Vendredi"

            self.table.setRowHeight(row, 50)
            self.table.setItem(row, 0, QTableWidgetItem(m))
            self.table.setItem(row, 1, QTableWidgetItem(str(day) + "/" + str(self.month) + "/" + str(self.year)))
            chose_light = Chose_worker(self.medcins)
            chose_night = Chose_worker(self.medcins)

            if self.service == "inf" or  self.service == "admin" or self.service == "pharm" or self.service == "dentiste_inf":
                if m in self.days_of_week:
                    if results_light:
                        rl = results_light[0]
                        chose_light.chose.setCurrentText(str(rl[0]))
                    else:
                        chose_light.chose.setEnabled(False)

                if results_night:
                    rn = results_night[0]
                    chose_night.chose.setCurrentText(str(rn[0]))
            else:
                if results_light:
                    print(results_light)
                    rl = results_light[0]
                    chose_light.chose.setCurrentText(str(rl[0]))
                if results_night:
                    print(results_night)
                    rn = results_night[0]
                    chose_night.chose.setCurrentText(str(rn[0]))


            self.table.setCellWidget(row, 2, chose_light)
            self.table.setCellWidget(row, 3, chose_night)

        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            self.dialog.close()
