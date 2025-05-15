import time
import Adafruit_ADS1x15
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QWidget
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5 import QtCore, QtWidgets
import sys


adc = Adafruit_ADS1x15.ADS1115()

GAIN = 4
count = 50
maxVal = 0
amp = 0

    
class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()

        title = "Current Sensing"
        left = 500
        top = 200
        width = 300
        height = 250
        iconName = "icon.ico"
        
        self.setWindowTitle(title)
        self.setGeometry(left,  top, width, height)
        
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        
        
        hbox = QHBoxLayout()
        currentLabel = QLabel("Current: ")
        self.currentValue = QLabel("-")
        amps = QLabel(" Amps")
        hbox.addWidget(currentLabel)
        hbox.addWidget(self.currentValue)
        hbox.addWidget(amps)
 
        wid.setLayout(hbox)
        self.show()
        QtCore.QTimer.singleShot(10, self.currentSensing)
        
    def currentSensing(self):
        series = [0]*count
        value = 0
        for i in range (count):
            value = adc.read_adc(0, gain=GAIN)
            #print(value)
            time.sleep(0.001)
            series[i] = value
        maxVal = max(series)
        
        amp = -0.00000000000003*(maxVal**3) + 0.0000000023*(maxVal**2) + 0.0014*maxVal + 0.4
        amp = round(amp,1)
        #print("Init Amp = " + str(amp))
        
        if(amp < 0.3): amp = 0
        #print(amp)
        self.currentValue.setText(str(amp))
        #time.sleep(0.01)
        QtCore.QTimer.singleShot(10, self.currentSensing)
        
if __name__ == "__main__":
    

    App = QApplication(sys.argv)
    print("Window Initiated")
    window = Window()
    sys.exit(App.exec())
    print("Window Initiated")
        

            




        
    
