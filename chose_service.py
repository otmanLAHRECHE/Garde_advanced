

import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect
import app
import app_inf_urgence


class ChoseService(QtWidgets.QMainWindow):
    def __init__(self):
        super(ChoseService, self).__init__()
        uic.loadUi("./user_interfaces/chose_service.ui", self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 150))
        # Appy shadow to central widget
        self.centralwidget.setGraphicsEffect(self.shadow)

        self.chose = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.suivant = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.suivant.clicked.connect(self.suivant_clicked)

    def suivant_clicked(self):
        if self.chose.currentIndex() == 0:
            print("nothing")
        elif self.chose.currentIndex() == 1:
            self.next_page = app.AppUi("urgence")
            self.next_page.show()
            self.close()
        elif self.chose.currentIndex() == 2:
            self.next_page = app_inf_urgence.AppInfUi("inf")
            self.next_page.show()
            self.close()
        elif self.chose.currentIndex() == 3:
            self.next_page = app.AppUi("dentiste")
            self.next_page.show()
            self.close()
        elif self.chose.currentIndex() == 4:
            self.next_page = app.AppUi("dentiste_inf")
            self.next_page.show()
            self.close()
        elif self.chose.currentIndex() == 5:
            self.next_page = app.AppUi("pharm")
            self.next_page.show()
            self.close()
        elif self.chose.currentIndex() == 6:
            self.next_page = app.AppUi("labo")
            self.next_page.show()
            self.close()
        elif self.chose.currentIndex() == 7:
            self.next_page = app.AppUi("admin")
            self.next_page.show()
            self.close()
        elif self.chose.currentIndex() == 8:
            self.next_page = app.AppUi("radio")
            self.next_page.show()
            self.close()


