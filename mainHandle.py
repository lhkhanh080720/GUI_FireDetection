# ===============pyuic5 -x mainv1.ui -o mainv1.py===============
from PyQt5 import QtCore, QtGui, QtWidgets
from mainv1 import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap
import sys
import cv2
import numpy as np
import threading
import time
import psutil
import datetime

class CameraSignal(QtCore.QObject):
    changePixmap1 = QtCore.pyqtSignal(np.ndarray)
    changePixmap2 = QtCore.pyqtSignal(np.ndarray)

class CaptureThread(threading.Thread):
    def __init__(self, camera_id, signal):
        threading.Thread.__init__(self)
        self.camera_id = camera_id
        self.signal = signal
        self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_V4L2)
        self.stop = False

    def run(self):
        while not self.stop:
            ret, frame = self.cap.read()
            if self.camera_id == '/dev/video0':
                self.signal.changePixmap1.emit(frame)
            elif self.camera_id == '/dev/video1':
                self.signal.changePixmap2.emit(frame)

    def __stop__(self): 
        self.stop = True
        print("Da stop " + str(self.stop))

class MAIN_HANDLE(Ui_MainWindow):
    def __init__(self):
        self.setupUi(MainWindow)

        #------------------add feature------------------#
        self.signal = CameraSignal()
        self.signal.changePixmap1.connect(self.update_frame1)
        self.signal.changePixmap2.connect(self.update_frame2)

        self.thread1 = CaptureThread('/dev/video0', self.signal)
        self.thread2 = CaptureThread('/dev/video1', self.signal)
        self.thread1.start()
        self.thread2.start()
        MainWindow.closeEvent = self.closeEvent

        # Update CPU and T
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_CPU)
        self.timer.timeout.connect(self.update_Temp)
        self.timer.start(5000)

    def update_frame1(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.labelText1.setPixmap(QPixmap.fromImage(image))
    
    def update_frame2(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.labelText2.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.thread1.__stop__()
        self.thread2.__stop__()
        self.timer.stop()
        self.signal.disconnect()
        self.signal = None
        event.accept()

    def update_CPU(self):
        per_cpu_percent = psutil.cpu_percent(percpu=True)
        for i, cpu_percent in enumerate(per_cpu_percent):
            if i == 0:
                self.labelCPU1.setText("CPU1: " + str(cpu_percent) + "%")
            if i == 1:
                self.labelCPU2.setText("CPU2: " + str(cpu_percent) + "%")
            if i == 2:
                self.labelCPU3.setText("CPU3: " + str(cpu_percent) + "%")
            if i == 3:
                self.labelCPU4.setText("CPU4: " + str(cpu_percent) + "%")

    def update_Temp(self):
        current_time = datetime.datetime.now().time()
        self.labelREALTIME.setText("TIME = " + str(current_time.strftime("%H:%M:%S")))
        with open("/sys/devices/virtual/thermal/thermal_zone1/temp", "r") as temp_file:
            self.labelTEMP1.setText("CPU: " + str(int(temp_file.read().strip())/1000))
        with open("/sys/devices/virtual/thermal/thermal_zone2/temp", "r") as temp_file:
            self.labelTEMP2.setText("GPU: " + str(int(temp_file.read().strip())/1000))
        with open("/sys/devices/virtual/thermal/thermal_zone5/temp", "r") as temp_file:
            self.labelTEMP3.setText("Thermal Fan: " + str(int(temp_file.read().strip())/1000))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MAIN_HANDLE()
    MainWindow.show()
    sys.exit(app.exec_())
