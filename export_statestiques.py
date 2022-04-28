import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog

import app
from threads import ThreadStateExport
from tools import create_statistique_page

basedir = os.path.dirname(__file__)


class ExportStatistiqueUi(QtWidgets.QMainWindow):
    def __init__(self, month, year):
        super(ExportStatistiqueUi, self).__init__()
        uic.loadUi("./user_interfaces/export.ui", self)




        self.month = month
        self.year = year

        self.setWindowTitle("Export Statistique")
        self.ttl = self.findChild(QtWidgets.QLabel, "label")
        self.progress = self.findChild(QtWidgets.QProgressBar, "progressBar")
        self.progress.setValue(0)
        self.status = self.findChild(QtWidgets.QLabel, "label_2")
        self.export = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.export.setIcon(QIcon("./asstes/images/download2.png"))
        self.export.setEnabled(False)
        self.export.clicked.connect(self.export_pdf)
        self.preview = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.preview.setEnabled(False)
        self.preview.setIcon(QIcon("./asstes/images/eye.png"))
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

        self.ttl.setText("Exporté statistique mois de  " + m + "/" + str(self.year))

        self.thr = ThreadStateExport(self.month, self.year)
        self.thr._signal.connect(self.signal_accept)
        self.thr._signal_result.connect(self.signal_accept)
        self.thr.start()

    def export_pdf(self):
        print(self.data)

        filePath, _ = QFileDialog.getSaveFileName(self, "Save garde", "",
                                                  "PDF(*.pdf);;All Files(*.*) ")


        if filePath == "":
            message = "destination untrouvable"
            self.alert_(message)
        else:
            create_statistique_page(self.month, self.year, self.data, filePath)
            self.next_page = app.AppUi("radio")
            self.next_page.show()
            print(self.thr.isFinished())
            self.close()


    def signal_accept(self, progress):
        if type(progress) == int:
            self.progress.setValue(progress)
        elif type(progress) == list:
            self.progress.setValue(100)
            self.data = progress
            print(self.data)
            self.status.setText("complete, click sur exporter")
            self.export.setEnabled(True)