import PyQt5
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

import app
import export_statestiques
from dialogs import Threading_loading, CustomDialog, Saving_progress_dialog
from threads import Thread_state_load, Thread_save_state


class RadioStatistiquesUi(QtWidgets.QMainWindow):
    def __init__(self, month, year):
        super(RadioStatistiquesUi, self).__init__()
        uic.loadUi("./user_interfaces/radiologie_statistiques.ui", self)

        self.month = month
        self.year = year

        self.want_to_close = False

        self.title = self.findChild(QtWidgets.QLabel, "label")
        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.save = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.save.setIcon(QIcon("./asstes/images/save.png"))
        self.export = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.export.setIcon(QIcon("./asstes/images/download.png"))

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

        self.title.setText("Radio statistiques mois de " + str(m) + "/" + str(self.year) + ":")

        self.load_state()
        self.save.clicked.connect(self.save_)
        self.export.clicked.connect(self.export_)

    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        message = "Votre radio statistiques na pas sauvgarder, es-tu sûr de quiter"
        dialog = CustomDialog(message)
        if dialog.exec():
            self.next_page = app.AppUi("radio")
            self.next_page.show()
            self.close()
        else:
            a0.ignore()

    def load_state(self):
        self.dialog = Threading_loading()
        self.dialog.ttl.setText("إنتظر من فضلك")
        self.dialog.progress.setValue(0)
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()

        self.thr1 = Thread_state_load(self.month, self.year)
        self.thr1._signal.connect(self.signal_accepted_load)
        self.thr1._signal_status.connect(self.signal_accepted_load)
        self.thr1._signal_finish.connect(self.signal_accepted_load)
        self.thr1.start()

    def signal_accepted_load(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:

            po = progress[0]
            self.table.setRowHeight(0, 50)
            self.table.setItem(0, 0, QTableWidgetItem(str(po[0])))
            self.table.setItem(0, 1, QTableWidgetItem(str(po[1])))
            self.table.setItem(0, 2, QTableWidgetItem(str(po[2])))
            total = int(po[0]) + int(po[1]) + int(po[2])
            self.table.setItem(0, 3, QTableWidgetItem(str(total)))


            os = progress[1]
            self.table.setRowHeight(1, 50)
            self.table.setItem(1, 0, QTableWidgetItem(str(os[0])))
            self.table.setItem(1, 1, QTableWidgetItem(str(os[1])))
            self.table.setItem(1, 2, QTableWidgetItem(str(os[2])))
            total = int(os[0]) + int(os[1]) + int(os[2])
            self.table.setItem(1, 3, QTableWidgetItem(str(total)))

            abd = progress[2]
            self.table.setRowHeight(2, 50)
            self.table.setItem(2, 0, QTableWidgetItem(str(abd[0])))
            self.table.setItem(2, 1, QTableWidgetItem(str(abd[1])))
            self.table.setItem(2, 2, QTableWidgetItem(str(abd[2])))
            total = int(abd[0]) + int(abd[1]) + int(abd[2])
            self.table.setItem(2, 3, QTableWidgetItem(str(total)))

            uiv = progress[3]
            self.table.setRowHeight(3, 50)
            self.table.setItem(3, 0, QTableWidgetItem(str(uiv[0])))
            self.table.setItem(3, 1, QTableWidgetItem(str(uiv[1])))
            self.table.setItem(3, 2, QTableWidgetItem(str(uiv[2])))
            total = int(uiv[0]) + int(uiv[1]) + int(uiv[2])
            self.table.setItem(3, 3, QTableWidgetItem(str(total)))

            chol = progress[4]
            self.table.setRowHeight(4, 50)
            self.table.setItem(4, 0, QTableWidgetItem(str(chol[0])))
            self.table.setItem(4, 1, QTableWidgetItem(str(chol[1])))
            self.table.setItem(4, 2, QTableWidgetItem(str(chol[2])))
            total = int(chol[0]) + int(chol[1]) + int(chol[2])
            self.table.setItem(4, 3, QTableWidgetItem(str(total)))

            est = progress[5]
            self.table.setRowHeight(5, 50)
            self.table.setItem(5, 0, QTableWidgetItem(str(est[0])))
            self.table.setItem(5, 1, QTableWidgetItem(str(est[1])))
            self.table.setItem(5, 2, QTableWidgetItem(str(est[2])))
            total = int(est[0]) + int(est[1]) + int(est[2])
            self.table.setItem(5, 3, QTableWidgetItem(str(total)))

            echo = progress[6]
            self.table.setRowHeight(6, 50)
            self.table.setItem(6, 0, QTableWidgetItem(str(echo[0])))
            self.table.setItem(6, 1, QTableWidgetItem(str(echo[1])))
            self.table.setItem(6, 2, QTableWidgetItem(str(echo[2])))
            total = int(echo[0]) + int(echo[1]) + int(echo[2])
            self.table.setItem(6, 3, QTableWidgetItem(str(total)))

            fibr = progress[7]
            self.table.setRowHeight(7, 50)
            self.table.setItem(7, 0, QTableWidgetItem(str(fibr[0])))
            self.table.setItem(7, 1, QTableWidgetItem(str(fibr[1])))
            self.table.setItem(7, 2, QTableWidgetItem(str(fibr[2])))
            total = int(fibr[0]) + int(fibr[1]) + int(fibr[2])
            self.table.setItem(7, 3, QTableWidgetItem(str(total)))

            ecg = progress[8]
            self.table.setRowHeight(8, 50)
            self.table.setItem(8, 0, QTableWidgetItem(str(ecg[0])))
            self.table.setItem(8, 1, QTableWidgetItem(str(ecg[1])))
            self.table.setItem(8, 2, QTableWidgetItem(str(ecg[2])))
            total = int(ecg[0]) + int(ecg[1]) + int(ecg[2])
            self.table.setItem(8, 3, QTableWidgetItem(str(total)))

            self.table.setRowHeight(9, 50)
            t1 = po[0] + os[0] +abd[0] + uiv[0] + chol[0] + est[0] + echo[0] + fibr[0] + ecg[0]
            t2 = po[1] + os[1] +abd[1] + uiv[1] + chol[1] + est[1] + echo[1] + fibr[1] + ecg[1]
            t3 = po[2] + os[2] +abd[2] + uiv[2] + chol[2] + est[2] + echo[2] + fibr[2] + ecg[2]
            self.table.setItem(9, 0, QTableWidgetItem(str(t1)))
            self.table.setItem(9, 1, QTableWidgetItem(str(t2)))
            self.table.setItem(9, 2, QTableWidgetItem(str(t3)))
            total = t1 + t2 +t3
            self.table.setItem(9, 3, QTableWidgetItem(str(total)))





        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.ttl.setText("complete")
            self.dialog.close()


    def save_(self):
        alert = False
        for row in range(self.table.rowCount()):
            if type(self.table.item(row, 2)) == PyQt5.QtWidgets.QTableWidgetItem :
                if not str(self.table.item(row, 0).text()).isnumeric() or not str(self.table.item(row, 1).text()).isnumeric() or not str(self.table.item(row, 2).text()).isnumeric():
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

            self.thr = Thread_save_state(self.month, self.year, self.table)
            self.thr._signal.connect(self.signal_accepted_save)
            self.thr._signal_status.connect(self.signal_accepted_save)
            self.thr.start()



    def export_(self):
        self.want_to_close = True
        self.next_page = export_statestiques.ExportStatistiqueUi(self.month, self.year)
        self.next_page.show()



    def signal_accepted_save(self, progress):
        if type(progress) == int :
            self.dialog.progress.setValue(progress)
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            self.dialog.close()
            t1 = 0
            t2 = 0
            t3 = 0
            for row in range(self.table.rowCount()):
                self.table.setItem(row, 3, QTableWidgetItem(str(int(self.table.item(row, 0).text()) + int(self.table.item(row, 1).text()) + int(self.table.item(row, 2).text()))))
                t1 = t1 + int(self.table.item(row, 0).text())
                t2 = t2 + int(self.table.item(row, 1).text())
                t3 = t3 + int(self.table.item(row, 2).text())

                if row == 9:
                    self.table.setItem(row, 0, QTableWidgetItem(str(t1)))
                    self.table.setItem(row, 0, QTableWidgetItem(str(t2)))
                    self.table.setItem(row, 0, QTableWidgetItem(str(t3)))
                    self.table.setItem(row, 0, QTableWidgetItem(str(t1 + t2 + t3)))


            self.alert_("data saved")