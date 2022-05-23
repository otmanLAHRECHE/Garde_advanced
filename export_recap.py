from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog

import app
from dialogs import CustomDialog
from threads import ThreadRecapExport
from tools import create_recap_page


class ExportRecapUi(QtWidgets.QMainWindow):
    def __init__(self, month, year, service, chef):
        super(ExportRecapUi, self).__init__()
        uic.loadUi("./user_interfaces/export.ui", self)

        self.chef = chef


        self.month = month
        self.year = year
        self.service = service

        self.setWindowTitle("Export RECAP service: " + self.service)
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
        self.status.setText("Preparation des données")

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
            self.ttl.setText("Imprimer RECAP urgence mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "dentiste":
            self.ttl.setText("Imprimer RECAP chirurgie dentaire mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "labo":
            self.ttl.setText("Imprimer RECAP laboratoire mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "radio":
            self.ttl.setText("Imprimer RECAP radiologie mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "admin":
            self.ttl.setText("Imprimer RECAP administration mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "dentiste_inf":
            self.ttl.setText("Imprimer RECAP infirmiers dentaire mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "pharm":
            self.ttl.setText("Imprimer RECAP pharmacie mois " + str(m) + "/" + str(self.year) + ":")

        self.thr = ThreadRecapExport(self.month, self.year, self.service)
        self.thr._signal.connect(self.signal_accept)
        self.thr._signal_result.connect(self.signal_accept)
        self.thr.start()


    def export_pdf(self):

        filePath, _ = QFileDialog.getSaveFileName(self, "Save garde", "",
                                                  "PDF(*.pdf);;All Files(*.*) ")


        if filePath == "":
            message = "destination untrouvable"
            self.alert_(message)
        else:
            if self.service == "urgence":
                s = "URGENCES"
                r = "medecins d'urgence"
            elif self.service == "dentiste":
                s = "DENTISTES"
                r = "medecins dentiste"
            elif self.service == "dentiste_inf":
                s = "DENTISTES"
                r = "infirmiers dentiste"
            elif self.service == "labo":
                s = "LABORATOIRE"
                r = "service laboratoire"
            elif self.service == "radio":
                s = "RADIOLOGIE"
                r = "service radiologie"
            elif self.service == "pharm":
                s = "PHARMACIE"
                r = "pharmaciens"
            elif self.service == "admin":
                s = "ADMINISTRATION"
                r = "administration"



            create_recap_page(s, r, self.month, self.year, self.data, self.chef, filePath)
            self.close()


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        message = "Es-tu sûr de quiter"
        dialog = CustomDialog(message)

        if dialog.exec():
            self.next_page = app.AppUi(self.service)
            self.next_page.show()
            self.close()
        else:
            a0.ignore()


    def signal_accept(self, progress):
        if type(progress) == int:
            self.progress.setValue(progress)
        elif type(progress) == list:
            self.progress.setValue(100)
            self.data = progress
            self.status.setText("complete, click sur exporter")
            self.export.setEnabled(True)