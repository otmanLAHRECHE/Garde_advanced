import PyQt5
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

import app
import export_recap
from database_operations import load_workers
from dialogs import CustomDialog, Threading_loading
from threads import Thread_save_recap, Thread_recap_load


class RecapUi(QtWidgets.QMainWindow):
    def __init__(self, service, month, year):
        super(RecapUi, self).__init__()
        uic.loadUi("./user_interfaces/recap.ui", self)

        self.month = month
        self.year = year
        self.service = service

        self.want_to_close = False

        self.setWindowTitle("RECAP Service " + self.service)

        self.title = self.findChild(QtWidgets.QLabel, "label")
        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.table.hideColumn(0)
        self.chef = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.save = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.save.setIcon(QIcon("./asstes/images/save.png"))
        self.export = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.export.setIcon(QIcon("asstes/images/download.png"))
        self.export.setEnabled(False)
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
            self.title.setText("RECAP Service de urgence mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "dentiste":
            self.title.setText("RECAP Service de chirurgie dentaire mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "labo":
            self.title.setText("RECAP Service de laboratoire mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "radio":
            self.title.setText("RECAP Service de radiologie mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "admin":
            self.title.setText("RECAP Service de administration mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "dentiste_inf":
            self.title.setText("RECAP Service de infirmiers dentaire mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "inf":
            self.title.setText("RECAP Service de infirmiers d'urgences mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "surv":
            self.title.setText("RECAP Service de infirmiers surveillants mois " + str(m) + "/" + str(self.year) + ":")

        elif self.service == "pharm":
            self.title.setText("RECAP Service de pharmacie mois " + str(m) + "/" + str(self.year) + ":")

        self.load_recap()

        self.save.clicked.connect(self.save_)
        self.export.clicked.connect(self.export_)
        self.add_barka.clicked.connect(self.add_)

    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        message = "Es-tu sûr de quiter"
        dialog = CustomDialog(message)
        if dialog.exec():
            self.next_page = app.AppUi(self.service)
            self.next_page.show()
            self.close()
        else:
            a0.ignore()


    def load_recap(self):
        self.dialog = Threading_loading()
        self.dialog.ttl.setText("إنتظر من فضلك")
        self.dialog.progress.setValue(0)
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()

        self.thr1 = Thread_recap_load(self.month, self.year, self.service)
        self.thr1._signal.connect(self.signal_accepted_load)
        self.thr1._signal_status.connect(self.signal_accepted_load)
        self.thr1._signal_finish.connect(self.signal_accepted_load)
        self.thr1._signal_users.connect(self.signal_accepted_load_users)
        self.thr1.start()

    def signal_accepted_load(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:

            agents_name = progress[0]
            jo = progress[1]
            jw = progress[2]
            jf = progress[3]
            pr = progress[4]

            self.table.setRowHeight(pr, 50)
            self.table.setItem(pr, 1, QTableWidgetItem(agents_name))
            self.table.setItem(pr, 2, QTableWidgetItem(str(jo)))
            self.table.setItem(pr, 3, QTableWidgetItem(str(jw)))
            self.table.setItem(pr, 4, QTableWidgetItem(str(jf)))
            total = jo + jw + jf
            self.table.setItem(pr, 5, QTableWidgetItem(str(total)))

        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.ttl.setText("complete")
            self.dialog.close()

    def signal_accepted_load_users(self, progress):
        self.chef.addItem("")
        for worker in progress:
            self.chef.addItem(worker[0])

    def save_(self):
        alert = False
        for row in range(self.table.rowCount()):
            if type(self.table.item(row, 2)) == PyQt5.QtWidgets.QTableWidgetItem:
                if not str(self.table.item(row, 2).text()).isnumeric() or not str(self.table.item(row, 3).text()).isnumeric() or not str(self.table.item(row, 4).text()).isnumeric():
                    alert = True

        if alert:
            self.alert_("Entrer des valeurs valide")
        else:
            self.want_to_close = True
            self.dialog = Threading_loading()
            self.dialog.ttl.setText("إنتظر من فضلك")
            self.dialog.progress.setValue(0)
            self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.dialog.show()

            self.thr = Thread_save_recap(self.month, self.year, self.table, self.service)
            self.thr._signal.connect(self.signal_accepted_save)
            self.thr._signal_status.connect(self.signal_accepted_save)
            self.thr.start()

    def export_(self):

        self.want_to_close = True
        print(self.chef.currentText())

        self.next_page = export_recap.ExportRecapUi(self.month, self.year, self.service, self.chef.currentText())
        self.next_page.show()

    def signal_accepted_save(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.ttl.setText("complete")
            self.dialog.close()

            for row in range(self.table.rowCount()):
                if type(self.table.item(row, 2)) == PyQt5.QtWidgets.QTableWidgetItem:
                    self.table.setItem(row, 5, QTableWidgetItem(
                        str(int(self.table.item(row, 2).text()) + int(self.table.item(row, 3).text()) + int(
                            self.table.item(row, 4).text()))))

            self.export.setEnabled(True)
            self.alert_("data saved")

    def add_(self):
        for row in range(self.table.rowCount()):
            if not type(self.table.item(row, 2)) == PyQt5.QtWidgets.QTableWidgetItem:
                index = row
                break
        print(index)

        self.table.setRowHeight(index, 50)
        self.table.setItem(index, 1, QTableWidgetItem(self.add_barka_combo.currentText()))
        self.table.setItem(index, 2, QTableWidgetItem(str(0)))
        self.table.setItem(index, 3, QTableWidgetItem(str(0)))
        self.table.setItem(index, 4, QTableWidgetItem(str(0)))
        total = 0 + 0 + 0
        self.table.setItem(index, 5, QTableWidgetItem(str(0)))

