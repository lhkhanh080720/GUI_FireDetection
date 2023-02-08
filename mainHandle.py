from PyQt5 import QtCore, QtGui, QtWidgets
from mainv1 import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap
import sys
import cv2
import numpy as np

class MAIN_HANDLE(Ui_MainWindow):
    def __init__(self):
        self.setupUi(MainWindow)

        #------------------add feature------------------#
        self.cap1 = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L2)
        self.cap2 = cv2.VideoCapture('/dev/video1', cv2.CAP_V4L2)
        # self.start_camera_threads()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame1)
        self.timer.timeout.connect(self.update_frame2)
        self.timer.start(1)

    def update_frame1(self):
        ret, frame = self.cap1.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.labelText1.setPixmap(QPixmap.fromImage(image))
    
    def update_frame2(self):
        ret, frame = self.cap2.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.labelText2.setPixmap(QPixmap.fromImage(image))
         
    def closeEvent(self, event):
        self.cap1.release()
        self.cap2.release()
        event.accept()      

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MAIN_HANDLE()
    MainWindow.show()
    sys.exit(app.exec_())