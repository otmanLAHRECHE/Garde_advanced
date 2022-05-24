



import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect

import chose_service
from threads import ThreadLoadingApp

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'EPSP_Djanet.EPSP_Guard.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("./user_interfaces/loading_app.ui", self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 150))
        # Appy shadow to central widget
        self.centralwidget.setGraphicsEffect(self.shadow)

        self.label = self.findChild(QtWidgets.QLabel, "loading_progress_status")
        self.progress = self.findChild(QtWidgets.QProgressBar, "my_progressBar")
        self.progress.setValue(20)

        self.t = ThreadLoadingApp()
        self.t._signal.connect(self.signal_accepted)
        self.t._signal_result.connect(self.signal_accepted)
        self.t.start()

    def signal_accepted(self, progress):
        if type(progress) == int:
            self.progress.setValue(progress)
        else:
            self.progress.setValue(100)
            self.label.setText("Wellcome")
            self.next_page = chose_service.ChoseService()
            self.next_page.show()
            self.close()

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./icons/app_icon.png"))
    # app.setLayoutDirection(Qt.RightToLeft)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()


