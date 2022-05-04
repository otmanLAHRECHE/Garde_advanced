import sqlite3

from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import QSize, QPropertyAnimation, QDate
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMessageBox, QTableWidgetItem, qApp, QCompleter

import planing_garde
from custom_widgets import Check
from database_operations import delete_worker
from dialogs import Add_new_inf, Threading_loading
from threads import ThreadAddWorker, ThreadAddGroupe, ThreadLoadWorkers, ThreadLoadInf, ThreadAddGroupeSurv, \
    ThreadUpdateGroupe, ThreadUpdateGroupeSurv

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
        self.table_workers_inf.setColumnWidth(2, 280)
        self.table_workers_inf.setColumnWidth(3, 130)
        self.table_workers_surv.hideColumn(0)
        self.table_workers_surv.setColumnWidth(1, 40)
        self.table_workers_surv.setColumnWidth(2, 280)
        self.table_workers_surv.setColumnWidth(3, 130)



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

        self.add_worker_button_inf.clicked.connect(self.add_worker)
        self.edit_worker_button_inf.clicked.connect(self.edit_worker)
        self.delete_worker_button_inf.clicked.connect(self.delete_worker)
        self.add_planing_button.clicked.connect(self.add_planing)
        self.delete_planing_button.clicked.connect(self.delete_planing)
        self.garde_button.clicked.connect(self.garde)
        self.recap_button.clicked.connect(self.recap)
        self.statestiques_button.clicked.connect(self.statestiques)

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

                self.thr = ThreadAddGroupe(dialog.nom.text(), self.worker_name.text())
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
            self.worker_name.setText("")
            self.load_workers_all()

    def load_workers_all(self):
        self.dialog = Threading_loading()
        self.dialog.ttl.setText("إنتظر من فضلك")
        self.dialog.progress.setValue(0)
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()

        self.table_workers_inf.setRowCount(0)
        self.table_workers_surv.setRowCount(0)

        self.thr = ThreadLoadInf(self.service)
        self.thr._signal.connect(self.signal_load_workers_inf)
        self.thr._signal_inf.connect(self.signal_load_workers_inf)
        self.thr._signal_surv.connect(self.signal_load_workers_surv)
        self.thr._signal_result.connect(self.signal_load_workers_inf)
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

                self.thr = ThreadAddGroupeSurv(dialog.nom.text(), self.worker_name.text())
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
            self.table_workers_inf.removeRow(row_selected)
            delete_worker(int(self.table_workers_inf.item(row_selected, 0).text()))
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
            self.table_workers_surv.removeRow(row_selected)
            delete_worker(int(self.table_workers_surv.item(row_selected, 0).text()))
            self.table_workers_surv.removeRow(0)
            self.load_workers_all()






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
        self.load_workers()


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