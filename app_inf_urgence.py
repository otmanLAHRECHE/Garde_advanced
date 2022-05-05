import sqlite3

from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import QSize, QPropertyAnimation, QDate
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMessageBox, QTableWidgetItem, qApp, QCompleter

import planing_garde
from custom_widgets import Check
from database_operations import delete_worker, delete_group_inf, delete_group_surv
from dialogs import Add_new_inf, Threading_loading, Add_new_month
from threads import ThreadAddWorker, ThreadAddGroupe, ThreadLoadWorkers, ThreadLoadInf, ThreadAddGroupeSurv, \
    ThreadUpdateGroupe, ThreadUpdateGroupeSurv, ThreadAddGardeMonth, ThreadDeleteGardeMonth, ThreadLoadGardeMonth

WINDOW_SIZE = 0

class AppInfUi(QtWidgets.QMainWindow):
    def __init__(self, service):
        super(AppInfUi, self).__init__()
        uic.loadUi("./user_interfaces/app_model_inf.ui", self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(115, 20)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 150))

        self.centralwidget.setGraphicsEffect(self.shadow)
        self.main_header = self.findChild(QtWidgets.QFrame, "main_header")
        self.left_side_menu = self.findChild(QtWidgets.QFrame, "left_side_menu")

        self.left_menu_toggle_btn = self.findChild(QtWidgets.QPushButton, "left_menu_toggle_btn")
        self.left_menu_toggle_btn.setIcon(QIcon("./icons/cil-menu.png"))
        self.left_menu_toggle_btn.setIconSize(QSize(24, 24))
        self.minimizeButton = self.findChild(QtWidgets.QPushButton, "minimizeButton")
        self.minimizeButton.setIcon(QIcon("./icons/minus.png"))
        self.minimizeButton.setIconSize(QSize(24, 24))
        self.closeButton = self.findChild(QtWidgets.QPushButton, "closeButton")
        self.closeButton.setIcon(QIcon("./icons/x.png"))
        self.closeButton.setIconSize(QSize(24, 24))
        self.pushButton_4 = self.findChild(QtWidgets.QPushButton, "pushButton_4")
        self.pushButton_4.setIcon(QIcon("./icons/users.png"))
        self.pushButton_2.setMinimumSize(QSize(100, 0))
        self.pushButton_4.setIconSize(QSize(32, 32))
        self.pushButton_3 = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.pushButton_3.setIcon(QIcon("./icons/calendar.png"))
        self.pushButton_3.setIconSize(QSize(32, 32))
        self.pushButton_2 = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.pushButton_2.setIcon(QIcon("./icons/settings.png"))
        self.pushButton_2.setIconSize(QSize(32, 32))
        self.fragment = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        self.pushButton_4.setStyleSheet("""
                        background-color: rgb(0, 92, 157);
                        background-repeat: none;
                        padding-left: 50px;
                        background-position: center left;
                        """)
        self.fragment.setCurrentIndex(0)

        self.minimizeButton.clicked.connect(self.showMinimized)
        self.closeButton.clicked.connect(self.close)

        self.pushButton_4.clicked.connect(self.h)
        self.pushButton_3.clicked.connect(self.sort)
        self.pushButton_2.clicked.connect(self.sett)

        def moveWindow(e):
            if self.isMaximized() == False:
                self.move(self.pos() + e.globalPos() - self.clickPosition)
                self.clickPosition = e.globalPos()
                e.accept()

        self.main_header.mouseMoveEvent = moveWindow

        self.left_menu_toggle_btn.clicked.connect(lambda: self.slideLeftMenu())

        ##################################################################################changes:

        self.service = service

        self.table_workers_surv = self.findChild(QtWidgets.QTableWidget, "tableWidget_4")
        self.table_workers_inf = self.findChild(QtWidgets.QTableWidget, "tableWidget_6")
        self.table_gardes = self.findChild(QtWidgets.QTableWidget, "tableWidget_5")


        self.table_gardes.hideColumn(0)
        self.table_gardes.setColumnWidth(1, 40)
        self.table_gardes.setColumnWidth(2, 200)
        self.table_gardes.setColumnWidth(3, 200)
        self.table_gardes.setColumnWidth(4, 330)


        self.table_workers_inf.hideColumn(0)
        self.table_workers_inf.setColumnWidth(1, 40)
        self.table_workers_inf.setColumnWidth(2, 150)
        self.table_workers_inf.setColumnWidth(3, 70)
        self.table_workers_inf.setColumnWidth(4, 80)
        self.table_workers_surv.hideColumn(0)
        self.table_workers_surv.setColumnWidth(1, 40)
        self.table_workers_surv.setColumnWidth(2, 150)
        self.table_workers_surv.setColumnWidth(3, 70)
        self.table_workers_surv.setColumnWidth(4, 80)



        self.worker_name = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")

        self.add_worker_button_inf = self.findChild(QtWidgets.QPushButton, "pushButton_12")
        self.add_worker_button_inf.setIcon(QIcon("./icons/plus2.png"))
        self.edit_worker_button_inf = self.findChild(QtWidgets.QPushButton, "pushButton_13")
        self.edit_worker_button_inf.setIcon(QIcon("./icons/edit2.png"))
        self.delete_worker_button_inf = self.findChild(QtWidgets.QPushButton, "pushButton_14")
        self.delete_worker_button_inf.setIcon(QIcon("./icons/trash.png"))

        self.add_worker_button_surv = self.findChild(QtWidgets.QPushButton, "pushButton_15")
        self.add_worker_button_surv.setIcon(QIcon("./icons/plus2.png"))
        self.edit_worker_button_surv = self.findChild(QtWidgets.QPushButton, "pushButton_17")
        self.edit_worker_button_surv.setIcon(QIcon("./icons/edit2.png"))
        self.delete_worker_button_surv = self.findChild(QtWidgets.QPushButton, "pushButton_16")
        self.delete_worker_button_surv.setIcon(QIcon("./icons/trash.png"))

        self.add_planing_button = self.findChild(QtWidgets.QPushButton, "pushButton_18")
        self.add_planing_button.setIcon(QIcon("./icons/plus2.png"))
        self.delete_planing_button = self.findChild(QtWidgets.QPushButton, "pushButton_23")
        self.delete_planing_button.setIcon(QIcon("./icons/trash.png"))
        self.garde_button_inf = self.findChild(QtWidgets.QPushButton, "pushButton_22")
        self.garde_button_surv = self.findChild(QtWidgets.QPushButton, "pushButton_26")
        self.recap_button = self.findChild(QtWidgets.QPushButton, "pushButton_24")
        self.statestiques_button = self.findChild(QtWidgets.QPushButton, "pushButton_25")
        self.statestiques_button.setIcon(QIcon("./icons/file-text.png"))

        self.add_worker_button_inf.clicked.connect(self.add_worker_inf)
        self.edit_worker_button_inf.clicked.connect(self.edit_worker_inf)
        self.delete_worker_button_inf.clicked.connect(self.delete_worker_inf)

        self.add_worker_button_surv.clicked.connect(self.add_worker_surv)
        self.edit_worker_button_surv.clicked.connect(self.edit_worker_surv)
        self.delete_worker_button_surv.clicked.connect(self.delete_worker_surv)

        self.add_planing_button.clicked.connect(self.add_planing)
        self.delete_planing_button.clicked.connect(self.delete_planing)
        self.garde_button_inf.clicked.connect(self.garde)
        self.garde_button_surv.clicked.connect(self.garde_surv)
        self.recap_button.setEnabled(False)
        self.statestiques_button.setEnabled(False)

        self.load_workers_all()

    def add_worker_inf(self):

        dialog = Add_new_inf()
        dialog.ttl.setText("Ajouter un infirmier")
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            if dialog.nom.text() == "":
                message = 'Le champ de nom est vide!'
                self.alert_(message)
            else:
                self.dialog = Threading_loading()
                self.dialog.ttl.setText("إنتظر من فضلك")
                self.dialog.progress.setValue(0)
                self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.dialog.show()

                self.thr = ThreadAddGroupe(dialog.nom.text(), dialog.groupe.currentText())
                self.thr._signal.connect(self.signal_add_worker)
                self.thr._signal_result.connect(self.signal_add_worker)
                self.thr.start()

    def signal_add_worker(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        else:
            self.dialog.progress.setValue(100)
            self.dialog.ttl.setText("Terminer")
            self.dialog.close()
            self.load_workers_all()

    def load_workers_all(self):
        self.dialog = Threading_loading()
        self.dialog.ttl.setText("إنتظر من فضلك")
        self.dialog.progress.setValue(0)
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()

        self.table_workers_inf.setRowCount(0)
        self.table_workers_surv.setRowCount(0)

        self.thr = ThreadLoadInf()
        self.thr._signal_status.connect(self.signal_load_workers_inf)
        self.thr._signal_inf.connect(self.signal_load_workers_inf)
        self.thr._signal_surv.connect(self.signal_load_workers_surv)
        self.thr._signal_finish.connect(self.signal_load_workers_inf)
        self.thr.start()

    def signal_load_workers_inf(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:
            row = progress[0]
            inf = progress[1]
            self.table_workers_inf.insertRow(row)
            self.table_workers_inf.setRowHeight(row, 40)
            check = Check()
            self.table_workers_inf.setItem(row, 0, QTableWidgetItem(str(inf[0])))
            self.table_workers_inf.setCellWidget(row, 1, check)
            self.table_workers_inf.setItem(row, 2, QTableWidgetItem(str(inf[1])))
            self.table_workers_inf.setItem(row, 3, QTableWidgetItem(str(inf[2])))
            self.table_workers_inf.setItem(row, 4, QTableWidgetItem(str(inf[3])))
        else:
            self.dialog.progress.setValue(100)
            self.dialog.ttl.setText("Terminer")
            self.dialog.close()

    def signal_load_workers_surv(self, progress):
        if type(progress) == list:
            row = progress[0]
            inf = progress[1]
            self.table_workers_surv.insertRow(row)
            self.table_workers_surv.setRowHeight(row, 40)
            check = Check()
            self.table_workers_surv.setItem(row, 0, QTableWidgetItem(str(inf[0])))
            self.table_workers_surv.setCellWidget(row, 1, check)
            self.table_workers_surv.setItem(row, 2, QTableWidgetItem(str(inf[1])))
            self.table_workers_surv.setItem(row, 3, QTableWidgetItem(str(inf[2])))
            self.table_workers_surv.setItem(row, 4, QTableWidgetItem(str(inf[3])))

    def add_worker_surv(self):
        dialog = Add_new_inf()
        dialog.ttl.setText("Ajouter un surveillant")
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            if dialog.nom.text() == "":
                message = 'Le champ de nom est vide!'
                self.alert_(message)
            else:
                self.dialog = Threading_loading()
                self.dialog.ttl.setText("إنتظر من فضلك")
                self.dialog.progress.setValue(0)
                self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.dialog.show()

                self.thr = ThreadAddGroupeSurv(dialog.nom.text(), dialog.groupe.currentText())
                self.thr._signal.connect(self.signal_add_worker)
                self.thr._signal_result.connect(self.signal_add_worker)
                self.thr.start()

    def edit_worker_inf(self):
        ch = 0
        for row in range(self.table_workers_inf.rowCount()):
            if self.table_workers_inf.cellWidget(row, 1).check.isChecked():
                row_selected = row
                ch = ch + 1
        if ch > 1 or ch == 0:
            self.alert_("selectioner just un infirmier")
            for row in range(self.table_workers_inf.rowCount()):
                self.table_workers_inf.cellWidget(row, 1).check.setChecked(False)
        else:
            dialog = Add_new_inf()
            dialog.ttl.setText("update infirmier:")
            dialog.nom.setText(self.table_workers_inf.item(row_selected, 2).text())
            dialog.groupe.setCurrentText(self.table_workers_inf.item(row_selected, 3).text())
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                if dialog.nom.text() == "":
                    message = "enter un valide nom"
                    self.alert_(message)
                else:
                    self.dialog = Threading_loading()
                    self.dialog.ttl.setText("إنتظر من فضلك")
                    self.dialog.progress.setValue(0)
                    self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                    self.dialog.show()

                    self.thr = ThreadUpdateGroupe(int(self.table_workers_inf.item(row_selected, 0).text()),
                                                  dialog.nom.text(), dialog.groupe.currentText())
                    self.thr._signal.connect(self.signal_edit_worker_inf)
                    self.thr._signal_list.connect(self.signal_edit_worker_inf)
                    self.thr._signal_result.connect(self.signal_edit_worker_inf)
                    self.thr.start()

    def edit_worker_surv(self):
        ch = 0
        for row in range(self.table_workers_surv.rowCount()):
            if self.table_workers_surv.cellWidget(row, 1).check.isChecked():
                row_selected = row
                ch = ch + 1
        if ch > 1 or ch == 0:
            self.alert_("selectioner just un surveillant")
            for row in range(self.table_workers_surv.rowCount()):
                self.table_workers_surv.cellWidget(row, 1).check.setChecked(False)
        else:
            dialog = Add_new_inf()
            dialog.ttl.setText("update infirmier:")
            dialog.nom.setText(self.table_workers_surv.item(row_selected, 2).text())
            dialog.groupe.setCurrentText(self.table_workers_surv.item(row_selected, 3).text())
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                if dialog.nom.text() == "":
                    message = "enter un valide nom"
                    self.alert_(message)
                else:
                    self.dialog = Threading_loading()
                    self.dialog.ttl.setText("إنتظر من فضلك")
                    self.dialog.progress.setValue(0)
                    self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                    self.dialog.show()

                    self.thr = ThreadUpdateGroupeSurv(int(self.table_workers_surv.item(row_selected, 0).text()),
                                                  dialog.nom.text(), dialog.groupe.currentText())
                    self.thr._signal.connect(self.signal_edit_worker_inf)
                    self.thr._signal_list.connect(self.signal_edit_worker_inf)
                    self.thr._signal_result.connect(self.signal_edit_worker_inf)
                    self.thr.start()


    def signal_edit_worker_inf(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        else:
            self.dialog.progress.setValue(100)
            self.dialog.ttl.setText("Terminer")
            self.dialog.close()
            self.worker_name.setText("")
            self.table_workers_inf.setRowCount(0)
            self.table_workers_surv.setRowCount(0)
            self.load_workers_all()

    def delete_worker_inf(self):
        ch = 0
        for row in range(self.table_workers_inf.rowCount()):
            if self.table_workers_surv.cellWidget(row, 1).check.isChecked():
                row_selected = row
                ch = ch + 1
        if ch > 1 or ch == 0:
            self.alert_("selectioner just un surveillant")
            for row in range(self.table_workers_inf.rowCount()):
                self.table_workers_inf.cellWidget(row, 1).check.setChecked(False)
        else:
            delete_worker(int(self.table_workers_inf.item(row_selected, 0).text()))
            delete_group_inf(int(self.table_workers_surv.item(row_selected, 0).text()))
            self.table_workers_inf.removeRow(row_selected)
            self.table_workers_inf.removeRow(0)
            self.load_workers_all()

    def delete_worker_surv(self):
        ch = 0
        for row in range(self.table_workers_surv.rowCount()):
            if self.table_workers_surv.cellWidget(row, 1).check.isChecked():
                row_selected = row
                ch = ch + 1
        if ch > 1 or ch == 0:
            self.alert_("selectioner just un surveillant")
            for row in range(self.table_workers_surv.rowCount()):
                self.table_workers_surv.cellWidget(row, 1).check.setChecked(False)
        else:
            delete_worker(int(self.table_workers_surv.item(row_selected, 0).text()))
            delete_group_surv(int(self.table_workers_surv.item(row_selected, 0).text()))
            self.table_workers_surv.removeRow(row_selected)
            self.load_workers_all()


    def load_garde_month(self):
        self.dialog = Threading_loading()
        self.dialog.ttl.setText("إنتظر من فضلك")
        self.dialog.progress.setValue(0)
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()

        self.thr = ThreadLoadGardeMonth(self.service)
        self.thr._signal.connect(self.signal_load_garde_month)
        self.thr._signal_list.connect(self.signal_load_garde_month)
        self.thr._signal_result.connect(self.signal_load_garde_month)
        self.thr.start()

    def signal_load_garde_month(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:
            row = progress[0]
            print(row)
            month = progress[1]
            self.table_gardes.insertRow(row)
            self.table_gardes.setRowHeight(row, 40)
            check = Check()
            self.table_gardes.setItem(row, 0, QTableWidgetItem(str(month[0])))
            self.table_gardes.setCellWidget(row, 1, check)
            m = ""
            if month[1] == 1:
                m = "janvier"
            elif month[1] == 2:
                m = "février"
            elif month[1] == 3:
                m = "mars"
            elif month[1] == 4:
                m = "avril"
            elif month[1] == 5:
                m = "mai"
            elif month[1] == 6:
                m = "juin"
            elif month[1] == 7:
                m = "juillet"
            elif month[1] == 8:
                m = "août"
            elif month[1] == 9:
                m = "septembre"
            elif month[1] == 10:
                m = "octobre"
            elif month[1] == 11:
                m = "novembre"
            elif month[1] == 12:
                m = "décembre"
            self.table_gardes.setItem(row, 2, QTableWidgetItem(str(m)))
            self.table_gardes.setItem(row, 3, QTableWidgetItem(str(month[2])))
            self.table_gardes.setItem(row, 4, QTableWidgetItem(str(month[3])))
        else:
            self.dialog.progress.setValue(100)
            self.dialog.ttl.setText("Terminer")
            self.dialog.close()

    def add_planing(self):
        dialog = Add_new_month()
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            if dialog.year.text() == "":
                message = "Entrer une valid année"
                self.alert_(message)
            else:
                m = 0
                if dialog.month.currentIndex() == 0:
                    m = 1
                elif dialog.month.currentIndex() == 1:
                    m = 2
                elif dialog.month.currentIndex() == 2:
                    m = 3
                elif dialog.month.currentIndex() == 3:
                    m = 4
                elif dialog.month.currentIndex() == 4:
                    m = 5
                elif dialog.month.currentIndex() == 5:
                    m = 6
                elif dialog.month.currentIndex() == 6:
                    m = 7
                elif dialog.month.currentIndex() == 7:
                    m = 8
                elif dialog.month.currentIndex() == 8:
                    m = 9
                elif dialog.month.currentIndex() == 9:
                    m = 10
                elif dialog.month.currentIndex() == 10:
                    m = 11
                elif dialog.month.currentIndex() == 11:
                    m = 12

                self.dialog = Threading_loading()
                self.dialog.ttl.setText("إنتظر من فضلك")
                self.dialog.progress.setValue(0)
                self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.dialog.show()

                self.thr = ThreadAddGardeMonth(self.service, m, int(dialog.year.text()))
                self.thr._signal.connect(self.signal_add_garde_month)
                self.thr._signal_result.connect(self.signal_add_garde_month)
                self.thr.start()

    def signal_add_garde_month(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        else:
            if progress == True:
                self.dialog.progress.setValue(100)
                self.dialog.ttl.setText("complete")
                self.dialog.close()
                self.table_gardes.setRowCount(0)
                self.load_garde_month()
            else:
                self.dialog.progress.setValue(100)
                self.dialog.ttl.setText("complete")
                self.dialog.close()
                message = "le mois est déjà existant"
                self.alert_(message)


    def delete_planing(self):
        ch = 0
        for row in range(self.table_gardes.rowCount()):
            if self.table_gardes.cellWidget(row, 1).check.isChecked():
                row_selected = row
                ch = ch + 1
        if ch > 1 or ch == 0:
            self.alert_("selectioner just un mois")
            for row in range(self.table_workers.rowCount()):
                self.table_workers.cellWidget(row, 1).check.setChecked(False)
        else:
            self.dialog = Threading_loading()
            self.dialog.ttl.setText("إنتظر من فضلك")
            self.dialog.progress.setValue(0)
            self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.dialog.show()

            self.thr = ThreadDeleteGardeMonth(int(self.table_gardes.item(row_selected, 0).text()))
            self.thr._signal.connect(self.signal_delete_garde_month)
            self.thr._signal_list.connect(self.signal_delete_garde_month)
            self.thr._signal_result.connect(self.signal_delete_garde_month)
            self.thr.start()

    def signal_delete_garde_month(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        else:
            self.dialog.progress.setValue(100)
            self.dialog.ttl.setText("Terminer")
            self.dialog.close()
            self.table_gardes.setRowCount(0)
            self.load_garde_month()

    def garde(self):
        ch = 0
        for row in range(self.table_gardes.rowCount()):
            if self.table_gardes.cellWidget(row, 1).check.isChecked():
                row_selected = row
                ch = ch + 1
        if ch > 1 or ch == 0:
            self.alert_("selectioner just un mois")
            for row in range(self.table_gardes.rowCount()):
                self.table_workers.cellWidget(row, 1).check.setChecked(False)
        else:
            m = self.table_gardes.item(row_selected, 2).text()
            y = self.table_gardes.item(row_selected, 3).text()
            if m == "janvier":
                m = 1
            elif m == "février":
                m = 2
            elif m == "mars":
                m = 3
            elif m == "avril":
                m = 4
            elif m == "mai":
                m = 5
            elif m == "juin":
                m = 6
            elif m == "juillet":
                m = 7
            elif m == "août":
                m = 8
            elif m == "septembre":
                m = 9
            elif m == "octobre":
                m = 10
            elif m == "novembre":
                m = 11
            elif m == "décembre":
                m = 12

            y = int(y)

            self.next_page = planing_garde.GuardUi("inf", m, y)
            self.next_page.show()
            self.close()


    def garde_surv(self):
        ch = 0
        for row in range(self.table_gardes.rowCount()):
            if self.table_gardes.cellWidget(row, 1).check.isChecked():
                row_selected = row
                ch = ch + 1
        if ch > 1 or ch == 0:
            self.alert_("selectioner just un mois")
            for row in range(self.table_gardes.rowCount()):
                self.table_gardes.cellWidget(row, 1).check.setChecked(False)
        else:
            m = self.table_gardes.item(row_selected, 2).text()
            y = self.table_gardes.item(row_selected, 3).text()
            if m == "janvier":
                m = 1
            elif m == "février":
                m = 2
            elif m == "mars":
                m = 3
            elif m == "avril":
                m = 4
            elif m == "mai":
                m = 5
            elif m == "juin":
                m = 6
            elif m == "juillet":
                m = 7
            elif m == "août":
                m = 8
            elif m == "septembre":
                m = 9
            elif m == "octobre":
                m = 10
            elif m == "novembre":
                m = 11
            elif m == "décembre":
                m = 12

            y = int(y)

            self.next_page = planing_garde.GuardUi("surv", m, y)
            self.next_page.show()
            self.close()



    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()



    def h(self):
        self.pushButton_4.setStyleSheet("""
        background-color: rgb(0, 92, 157);
        background-repeat: none;
        padding-left: 50px;
        background-position: center left;
        """)
        self.pushButton_2.setStyleSheet("""background-color: rgb(0, 0, 0);
        background-repeat: none;
        padding-left: 50px;
        background-position: center left;
        """)
        self.pushButton_3.setStyleSheet("""background-color: rgb(0, 0, 0);
        background-repeat: none;
        padding-left: 50px;
        background-position: center left;
        """)
        self.fragment.setCurrentIndex(0)

        self.table_workers_inf.setRowCount(0)
        self.table_workers_surv.setRowCount(0)
        self.load_workers_all()


    def sort(self):
        self.pushButton_3.setStyleSheet("""background-color: rgb(0, 92, 157);
        background-repeat: none;
        padding-left: 50px;
        background-position: center left;""")
        self.pushButton_4.setStyleSheet("""background-color: rgb(0, 0, 0);
        background-repeat: none;
        padding-left: 50px;
        background-position: center left;""")
        self.pushButton_2.setStyleSheet("""background-color: rgb(0, 0, 0);
        background-repeat: none;
        padding-left: 50px;
        background-position: center left;""")
        self.fragment.setCurrentIndex(1)

        self.table_gardes.setRowCount(0)
        self.load_garde_month()



    def sett(self):
        self.pushButton_2.setStyleSheet("""background-color: rgb(0, 92, 157);
        background-repeat: none;
        padding-left: 50px;
        background-position: center left;""")
        self.pushButton_3.setStyleSheet("""background-color: rgb(0, 0, 0);
        background-repeat: none;
        padding-left: 50px;
        background-position: center left;""")
        self.pushButton_4.setStyleSheet("""background-color: rgb(0, 0, 0);
        background-repeat: none;
        padding-left: 50px;
        background-position: center left;""")
        self.fragment.setCurrentIndex(2)


    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def restore_or_maximize_window(self):
        global WINDOW_SIZE
        win_status = WINDOW_SIZE

        if win_status == 0:
            WINDOW_SIZE = 1
            self.showMaximized()
            self.restoreButton.setIcon(QtGui.QIcon("./icons/minimize.png"))  # Show minized icon
        else:
            WINDOW_SIZE = 0
            self.showNormal()
            self.restoreButton.setIcon(QtGui.QIcon("./icons/maximize.png"))  # Show maximize icon

    def slideLeftMenu(self):
        width = self.left_side_menu.width()

        # If minimized
        if width == 50:
            # Expand menu
            newWidth = 180
            self.pushButton_4.setText(" Travailleurs")
            self.pushButton_3.setText(" Planing")
            self.pushButton_2.setText("  Parametre")

        else:
            # Restore menu
            newWidth = 50
            self.pushButton_4.setText("ttttttttt")
            self.pushButton_3.setText("tttttttt")
            self.pushButton_2.setText(" tttttttttttttttttttttt")

        # Animate the transition
        self.animation = QPropertyAnimation(self.left_side_menu, b"minimumWidth")  # Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)  # Start value is the current menu width
        self.animation.setEndValue(newWidth)  # end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()