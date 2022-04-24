
from PyQt5 import QtWidgets, uic, QtGui, Qt, QtCore
from calendar import monthrange

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, qApp, QMessageBox

from dialogs import CustomDialog, Saving_progress_dialog

import os

class GuardUi(QtWidgets.QMainWindow):
    def __init__(self, service, month, year):
        super(GuardUi, self).__init__()
        uic.loadUi("./user_interfaces/planing_garde.ui", self)

        self.want_to_close = False

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
