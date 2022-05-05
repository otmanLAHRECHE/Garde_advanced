from calendar import monthrange

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import app
from threads import ThreadGuard
from tools import create_garde_page, create_garde_inf_page


class ExportGardeUi(QtWidgets.QMainWindow):
    def __init__(self, service, month, year):
        super(ExportGardeUi, self).__init__()
        uic.loadUi("./user_interfaces/export.ui", self)

        self.month = month
        self.year = year
        self.service = service

        self.ttl = self.findChild(QtWidgets.QLabel, "label")
        self.progress = self.findChild(QtWidgets.QProgressBar, "progressBar")
        self.progress.setValue(0)
        self.status = self.findChild(QtWidgets.QLabel, "label_2")
        self.export = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.export.setEnabled(False)
        self.export.setIcon(QIcon("./asstes/images/download2.png"))
        self.preview = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.preview.setEnabled(False)
        self.preview.setIcon(QIcon("./asstes/images/eye.png"))
        self.export.clicked.connect(self.export_pdf)
        self.preview.clicked.connect(self.preview_pdf)
        self.status.setText("Preparation des données")
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
            self.ttl.setText("Imprimer planing de garde urgence mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "dentiste":
            self.ttl.setText("Imprimer planing de garde chirurgie dentaire mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "labo":
            self.ttl.setText("Imprimer planing de garde laboratoire mois " + str(m) + "/" + str(self.year) + ":")


        elif self.service == "radio":
            self.ttl.setText("Imprimer planing de garde radiologie mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "admin":
            self.ttl.setText("Imprimer planing de garde administration mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "dentiste_inf":
            self.ttl.setText("Imprimer planing de garde infirmiers dentaire mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "inf":
            self.ttl.setText("EPSP Djanet ( Infirmiers d'urgences )")
            self.ttl.setText("Imprimer planing de garde infirmiers d'urgences mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "surv":
            self.ttl.setText("EPSP Djanet ( Surveillants d'urgences )")
            self.ttl.setText("Imprimer planing de garde infirmiers surveillants mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "pharm":
            self.ttl.setText("Imprimer planing de garde pharmacie mois " + str(m) + "/" + str(self.year) + ":")

        self.thr = ThreadGuard(self.service, self.num_days, self.month, self.year)
        self.thr._signal.connect(self.signal_accept)
        self.thr._signal_result.connect(self.signal_accept)
        self.thr.start()

    def export_pdf(self):
        print(self.data)
        filePath, _ = QFileDialog.getSaveFileName(self, "Save garde", "",
                                                  "PDF(*.pdf);;All Files(*.*) ")

        # if file path is blank return back
        if filePath == "":
            message = "destination untrouvable"
            self.alert_(message)
        else:
            if not self.service == "inf" and not self.service == "surv":
                create_garde_page(self.service,  self.month, self.year, self.data, filePath)
                self.next_page = app.AppUi(self.service)
                self.next_page.show()
                self.close()
            else:
                create_garde_inf_page(self.service,  self.month, self.year, self.data,
                                      self.groupes, filePath)
                self.next_page = app.AppUi(self.service)
                self.next_page.show()
                self.close()

    def signal_accept(self, progress):
        if type(progress) == int:
            self.progress.setValue(progress)
        elif type(progress) == list:
            self.progress.setValue(100)
            self.data = progress
            self.status.setText("complete, click sur exporter")
            self.export.setEnabled(True)

    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()


    def preview_pdf(self):
        print("ok")