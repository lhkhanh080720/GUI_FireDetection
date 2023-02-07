from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5 import uic
import sys

class MYUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainv1.ui", self)
        self.show()

        #---------------------------#
        self.plainTextEdit.setPlainText("")
        self.pushButton.clicked.connect(self.btnHandle)

    def btnHandle(self):
        name = self.plainTextEdit.toPlainText()
        self.labelText.setText("Hi: " + name)

if __name__ == "__main__":
    # Default
    app = QApplication(sys.argv)

    my_ui = MYUI()

    # Default
    app.exec_()