from PyQt5 import QtWidgets, uic


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