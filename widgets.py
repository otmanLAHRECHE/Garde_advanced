from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets


class Chose_worker(QWidget):
    def __init__(self, list_workers):
        super(Chose_worker, self).__init__()

        widget = QtWidgets.QHBoxLayout()
        self.chose = QtWidgets.QComboBox()
        self.chose.addItem("")
        for worker in list_workers:
            self.chose.addItem(worker[0])
        widget.addWidget(self.chose)





        self.setLayout(widget)