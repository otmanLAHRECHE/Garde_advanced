from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QDialogButtonBox, QVBoxLayout, QLabel


class Threading_loading(QtWidgets.QMainWindow):
    def __init__(self):
        super(Threading_loading, self).__init__()
        uic.loadUi('./user_interfaces/threading.ui', self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 150))
        # Appy shadow to central widget
        self.centralwidget.setGraphicsEffect(self.shadow)

        self.ttl = self.findChild(QtWidgets.QLabel, "loading_progress_status")
        self.progress = self.findChild(QtWidgets.QProgressBar, "my_progressBar")


class Update_worker_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Update_worker_dialog, self).__init__()
        uic.loadUi("./user_interfaces/update_worker_name.ui", self)

        self.setWindowTitle("metre a jour")
        self.worker = self.findChild(QtWidgets.QLineEdit, "lineEdit")


class Add_new_month(QtWidgets.QDialog):
    def __init__(self):
        super(Add_new_month, self).__init__()
        uic.loadUi("./user_interfaces/add_new_month.ui", self)

        self.setWindowTitle("ajouter nouveau planing")
        self.month = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.year = self.findChild(QtWidgets.QLineEdit, "lineEdit")


class CustomDialog(QtWidgets.QDialog):
    def __init__(self, msg, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Alert")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(msg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class Saving_progress_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Saving_progress_dialog, self).__init__()
        uic.loadUi("./user_interfaces/saving_dialog.ui", self)
        self.label = self.findChild(QtWidgets.QLabel, "label")
        self.progress = self.findChild(QtWidgets.QProgressBar, "progressBar")
        self.progress.setValue(0)


class Add_new_inf(QtWidgets.QDialog):
    def __init__(self):
        super(Add_new_inf, self).__init__()
        uic.loadUi("./user_interfaces/add_new_inf.ui", self)

        self.setWindowTitle("ajouter nouvelle infermier")
        self.ttl = self.findChild(QtWidgets.QLabel, "label")
        self.groupe = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.nom = self.findChild(QtWidgets.QLineEdit, "lineEdit")

class Auto_plus(QtWidgets.QDialog):
    def __init__(self, num_days, mois, medecins):
        super(Auto_plus, self).__init__()
        uic.loadUi("./user_interfaces/auto_plus.ui", self)

        self.month = mois

        self.setWindowTitle("auto garde")
        self.type = self.findChild(QtWidgets.QComboBox, "comboBox_2")
        self.agent = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.add_agent = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.empty_list_agents = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.radio_all = self.findChild(QtWidgets.QRadioButton, "radioButton_2")
        self.radio_periode = self.findChild(QtWidgets.QRadioButton, "radioButton")
        self.start_day = self.findChild(QtWidgets.QSpinBox, "spinBox")
        self.end_day = self.findChild(QtWidgets.QSpinBox, "spinBox_2")
        self.jour_fr = self.findChild(QtWidgets.QSpinBox, "spinBox_3")
        self.add_jour_fr = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.empty_list_jour_fr = self.findChild(QtWidgets.QPushButton, "pushButton_4")
        self.classement = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.list_jour_fr = self.findChild(QtWidgets.QListWidget, "listWidget_2")

        self.add_agent.clicked.connect(self.add_to_classemnt)
        self.empty_list_agents.clicked.connect(self.empty_classement)

        self.add_jour_fr.clicked.connect(self.add_day_fr)
        self.empty_list_jour_fr.clicked.connect(self.empty_day_fr)

        self.radio_all.setChecked(True)
        self.start_day.setEnabled(False)
        self.end_day.setEnabled(False)

        self.radio_all.toggled.connect(self.radio_all_toggled)
        self.radio_periode.toggled.connect(self.radio_periode_toggled)

        for i in medecins:
            self.agent.addItem(i[0])


    def radio_all_toggled(self, selected):
        if selected:
            self.start_day.setEnabled(False)
            self.end_day.setEnabled(False)

    def radio_periode_toggled(self, selected):
        if selected:
            self.start_day.setEnabled(True)
            self.end_day.setEnabled(True)


    def add_to_classemnt(self):
        self.classement.addItem(self.agent.currentText())

    def empty_classement(self):
        self.classement.clear()

    def add_day_fr(self):
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
        self.list_jour_fr.addItem(str(self.jour_fr.value())+" "+m)



    def empty_day_fr(self):
        self.list_jour_fr.clear()



