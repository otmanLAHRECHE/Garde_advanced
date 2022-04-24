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