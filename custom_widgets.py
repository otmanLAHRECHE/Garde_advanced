from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets


class Check(QWidget):
    def __init__(self):
        super(Check, self).__init__()

        layout = QtWidgets.QHBoxLayout()
        self.check = QtWidgets.QCheckBox()
        self.check.setFixedHeight(30)
        self.check.setFixedWidth(30)

        layout.addStretch(1)
        layout.addWidget(self.check)

        self.setLayout(layout)