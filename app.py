



from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import QSize, QPropertyAnimation, QDate
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMessageBox, QTableWidgetItem, qApp, QCompleter

from custom_widgets import Check
from dialogs import Threading_loading, Update_worker_dialog, Add_new_month
from threads import ThreadAddWorker, ThreadLoadWorkers, ThreadUpdateWorker, ThreadDeleteWorker, ThreadLoadGardeMonth, \
    ThreadAddGardeMonth, ThreadDeleteGardeMonth

WINDOW_SIZE = 0

class AppUi(QtWidgets.QMainWindow):
    def __init__(self, service):
        super(AppUi, self).__init__()
        uic.loadUi("./user_interfaces/app_model.ui", self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(115, 20)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 150))

        # Appy shadow to central widget
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
        self.ttl = self.findChild(QtWidgets.QLabel, "label_2")
        self.ttl1 = self.findChild(QtWidgets.QLabel, "label")
        self.ttl2 = self.findChild(QtWidgets.QLabel, "label_3")

        self.table_workers = self.findChild(QtWidgets.QTableWidget, "tableWidget_4")
        self.table_gardes = self.findChild(QtWidgets.QTableWidget, "tableWidget_5")

        self.table_workers.hideColumn(0)
        self.table_gardes.hideColumn(0)
        self.table_gardes.setColumnWidth(1, 40)
        self.table_workers.setColumnWidth(1, 40)
        self.table_workers.setColumnWidth(2, 200)

        self.worker_name = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")


        self.add_worker_button = self.findChild(QtWidgets.QPushButton, "pushButton_12")
        self.add_worker_button.setIcon(QIcon("./icons/plus2.png"))
        self.edit_worker_button = self.findChild(QtWidgets.QPushButton, "pushButton_13")
        self.edit_worker_button.setIcon(QIcon("./icons/edit2.png"))
        self.delete_worker_button = self.findChild(QtWidgets.QPushButton, "pushButton_14")
        self.delete_worker_button.setIcon(QIcon("./icons/trash.png"))

        self.add_planing_button = self.findChild(QtWidgets.QPushButton, "pushButton_18")
        self.add_planing_button.setIcon(QIcon("./icons/plus2.png"))
        self.delete_planing_button = self.findChild(QtWidgets.QPushButton, "pushButton_23")
        self.delete_planing_button.setIcon(QIcon("./icons/trash.png"))
        self.garde_button = self.findChild(QtWidgets.QPushButton, "pushButton_22")
        self.recap_button = self.findChild(QtWidgets.QPushButton, "pushButton_24")
        self.statestiques_button = self.findChild(QtWidgets.QPushButton, "pushButton_25")
        self.statestiques_button.setIcon(QIcon("./icons/file-text.png"))

        self.add_worker_button.clicked.connect(self.add_worker)
        self.edit_worker_button.clicked.connect(self.edit_worker)
        self.delete_worker_button.clicked.connect(self.delete_worker)
        self.add_planing_button.clicked.connect(self.add_planing)
        self.delete_planing_button.clicked.connect(self.delete_planing)
        self.garde_button.clicked.connect(self.garde)
        self.recap_button.clicked.connect(self.recap)
        self.statestiques_button.clicked.connect(self.statestiques)

        if self.service == "urgence":
            self.ttl.setText("EPSP Djanet ( Medecins d'urgence )")
            self.ttl1.setText("Liste des Medecins")
            self.ttl2.setText("Medecin nom")
            self.statestiques_button.setEnabled(False)
        elif self.service == "dentiste":
            self.ttl.setText("EPSP Djanet ( Chirurgie dentaire )")
            self.ttl1.setText("Liste des Medecins dentiste")
            self.ttl2.setText("Medecin nom")
            self.statestiques_button.setEnabled(False)
        elif self.service == "labo":
            self.ttl.setText("EPSP Djanet ( Laboratoire )")
            self.ttl1.setText("Liste des laborants")
            self.ttl2.setText("nom")
            self.statestiques_button.setEnabled(False)
        elif self.service == "radio":
            self.ttl.setText("EPSP Djanet ( Radiologie )")
            self.ttl1.setText("Liste des manipulateurs radio")
            self.ttl2.setText("nom")
            self.statestiques_button.setEnabled(True)
        elif self.service == "admin":
            self.ttl.setText("EPSP Djanet ( Administration )")
            self.ttl1.setText("Liste des agents d'administration")
            self.ttl2.setText("nom")
            self.statestiques_button.setEnabled(False)
        elif self.service == "dentiste_inf":
            self.ttl.setText("EPSP Djanet ( Infirmiers dentaire )")
            self.ttl1.setText("Liste des infirmiers dentaire")
            self.ttl2.setText("nom")
            self.statestiques_button.setEnabled(False)
        elif self.service == "inf":
            self.ttl.setText("EPSP Djanet ( Infirmiers d'urgences )")
            self.ttl1.setText("Liste des infirmiers d'urgences")
            self.ttl2.setText("nom")
            self.statestiques_button.setEnabled(False)
        elif self.service == "pharm":
            self.ttl.setText("EPSP Djanet ( Pharmacie )")
            self.ttl1.setText("Liste des pharmaciens")
            self.ttl2.setText("nom")
            self.statestiques_button.setEnabled(False)


        self.load_workers()



    def add_worker(self):
        if self.worker_name.text() == "":
            message = 'Le champ de nom est vide!'
            self.alert_(message)
        else:
            self.dialog = Threading_loading()
            self.dialog.ttl.setText("إنتظر من فضلك")
            self.dialog.progress.setValue(0)
            self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.dialog.show()

            self.thr = ThreadAddWorker(self.service, self.worker_name.text())
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
            self.load_workers()

    def load_workers(self):
        self.dialog = Threading_loading()
        self.dialog.ttl.setText("إنتظر من فضلك")
        self.dialog.progress.setValue(0)
        self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.dialog.show()

        self.thr = ThreadLoadWorkers(self.service)
        self.thr._signal.connect(self.signal_load_workers)
        self.thr._signal_list.connect(self.signal_load_workers)
        self.thr._signal_result.connect(self.signal_load_workers)
        self.thr.start()

    def signal_load_workers(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == list:
            row = progress[0]
            print(row)
            worker = progress[1]
            self.table_workers.insertRow(row)
            self.table_workers.setRowHeight(row, 40)
            check = Check()
            self.table_workers.setItem(row, 0, QTableWidgetItem(str(worker[0])))
            self.table_workers.setCellWidget(row, 1, check)
            self.table_workers.setItem(row, 2, QTableWidgetItem(str(worker[1])))
            self.table_workers.setItem(row, 3, QTableWidgetItem(str(worker[2])))
        else:
            self.dialog.progress.setValue(100)
            self.dialog.ttl.setText("Terminer")
            self.dialog.close()

    def edit_worker(self):
        ch = 0
        for row in range(self.table_workers.rowCount()):
            if self.table_workers.cellWidget(row, 1).check.isChecked():
                row_selected = row
                ch = ch + 1
        if ch > 1 or ch ==0:
            self.alert_("selectioner just une travailleur")
            for row in range(self.table_workers.rowCount()):
                self.table_workers.cellWidget(row, 1).check.setChecked(False)
        else:
            dialog = Update_worker_dialog()
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                if dialog.worker.text() == "":
                    message = "enter un valide nom"
                    self.alert_(message)
                else:
                    self.dialog = Threading_loading()
                    self.dialog.ttl.setText("إنتظر من فضلك")
                    self.dialog.progress.setValue(0)
                    self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                    self.dialog.show()

                    self.thr = ThreadUpdateWorker(int(self.table_workers.item(row_selected, 0).text()), dialog.worker.text())
                    self.thr._signal.connect(self.signal_edit_worker)
                    self.thr._signal_list.connect(self.signal_edit_worker)
                    self.thr._signal_result.connect(self.signal_edit_worker)
                    self.thr.start()

    def signal_edit_worker(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        else:
            self.dialog.progress.setValue(100)
            self.dialog.ttl.setText("Terminer")
            self.dialog.close()
            self.table_workers.setRowCount(0)
            self.load_workers()

    def delete_worker(self):
        ch = 0
        for row in range(self.table_workers.rowCount()):
            if self.table_workers.cellWidget(row, 1).check.isChecked():
                row_selected = row
                ch = ch + 1
        if ch > 1 or ch == 0:
            self.alert_("selectioner just une travailleur")
            for row in range(self.table_workers.rowCount()):
                self.table_workers.cellWidget(row, 1).check.setChecked(False)
        else:
            self.dialog = Threading_loading()
            self.dialog.ttl.setText("إنتظر من فضلك")
            self.dialog.progress.setValue(0)
            self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.dialog.show()

            self.thr = ThreadDeleteWorker(int(self.table_workers.item(row_selected, 0).text()))
            self.thr._signal.connect(self.signal_delete_worker)
            self.thr._signal_list.connect(self.signal_delete_worker)
            self.thr._signal_result.connect(self.signal_delete_worker)
            self.thr.start()

    def signal_delete_worker(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        else:
            self.dialog.progress.setValue(100)
            self.dialog.ttl.setText("Terminer")
            self.dialog.close()
            self.table_workers.setRowCount(0)
            self.load_workers()


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
            self.table_gardes.setItem(row, 2, QTableWidgetItem(str(month[1])))
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
                self.thr._signal_list.connect(self.signal_add_garde_month)
                self.thr._signal_result.connect(self.signal_add_garde_month)
                self.thr.start()

    def signal_add_garde_month(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        else:
            if progress == True:
                self.dialog.progress.setValue(100)
                self.dialog.label.setText("complete")
                self.dialog.close()
                self.table_gardes.setRowCount(0)
                self.load_garde_month()
            else:
                self.dialog.progress.setValue(100)
                self.dialog.label.setText("complete")
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
            self.alert_("selectioner just une travailleur")
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
        print("ok")

    def recap(self):
        print("ok")

    def statestiques(self):
        print("ok")


    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()


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


        self.table_workers.setRowCount(0)
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