import time
import threading 
import RPi.GPIO as GPIO 
import Adafruit_ADS1x15
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QTimer, QSize
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap,QIcon
import sys
import Adafruit_DHT
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import datetime
import serial

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 4
count = 40
maxVal = 0
amp = 0.1

sourceState = 0
maxTime = 5
maxCurrent = 2.5

global stop_threads 

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        title = "Relay Test Unit"
        left = 2
        top = 30
        width = 796
        height = 450
        
        self.setWindowTitle(title)
        self.setGeometry(left,  top, width, height)
        self.setFixedSize(width, height)
        
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        self.setStyleSheet("background-color: white;")
        
        mainVBox = QVBoxLayout()
        topBox = QHBoxLayout()
        button1Box = QHBoxLayout()
        button2Box = QHBoxLayout()
        bottomBox = QHBoxLayout()
        
        self.labelTemp = QLabel(self)
        self.labelTemp.setAlignment(Qt.AlignLeft)
        self.labelTemp.setAlignment(Qt.AlignTop)
        self.labelTemp.setFixedHeight(40)
        self.labelTemp.setText("Temperature")
        self.labelTime = QLabel(self)
        self.labelTime.setAlignment(Qt.AlignRight)
        self.labelTime.setFixedHeight(40)
        self.labelTime.setText("Time")
        
        self.btn1 = QToolButton()
        self.btn1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn1.setFixedSize(110,100)
        self.btn1.setText("MCB Test")
        self.btn1.setFont(QtGui.QFont("Calibri", 9))
        self.btn2 = QToolButton()
        self.btn2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn2.setFixedSize(110,100)
        self.btn2.setText("OCR Test")
        self.btn2.setFont(QtGui.QFont("Calibri", 9))
        self.btn3 = QToolButton()
        self.btn3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn3.setFixedSize(110,100)
        self.btn3.setText("Voltage Relay Test")
        self.btn3.setFont(QtGui.QFont("Calibri", 9))
        self.btn4 = QToolButton()
        self.btn4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn4.setFixedSize(110,100)
        self.btn4.setText("Extra")
        self.btn4.setFont(QtGui.QFont("Calibri", 9))
        self.btn5 = QToolButton()
        self.btn5.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn5.setFixedSize(110,100)
        self.btn5.setText("Logged Data")
        self.btn5.setFont(QtGui.QFont("Calibri", 9))
        self.btn6 = QToolButton()
        self.btn6.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn6.setFixedSize(110,100)
        self.btn6.setText("Settings")
        self.btn6.setFont(QtGui.QFont("Calibri", 9))
        self.btn7 = QToolButton()
        self.btn7.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn7.setFixedSize(110,100)
        self.btn7.setText("How To Use")
        self.btn7.setFont(QtGui.QFont("Calibri", 9))
        self.btn8 = QToolButton()
        self.btn8.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn8.setFixedSize(110,100)
        self.btn8.setText("About")
        self.btn8.setFont(QtGui.QFont("Calibri", 9))
        self.btn9 = QPushButton()
        self.btn9.setFixedSize(60,55)

        pixmapMCB = QPixmap("MCB.jpg")
        pixmapCurrRelay = QPixmap("Current Relay.jpg")
        pixmapVoltRelay = QPixmap("Voltage Relay.jpg")
        
        pixmapEmpty = QPixmap("Empty.jpg")
        
        pixmapDataLog = QPixmap("DataLog.jpg")
        pixmapSettings = QPixmap("Settings.jpg")
        pixmapUManual = QPixmap("User Manual.jpg")
        pixmapAbout = QPixmap("About.jpg")
        pixmapClose = QPixmap("Close.png")
        
        self.btn1.setIcon(QIcon(pixmapMCB))
        self.btn1.setIconSize(QSize(106,80))
        self.btn2.setIcon(QIcon(pixmapCurrRelay))
        self.btn2.setIconSize(QSize(106,80))
        self.btn3.setIcon(QIcon(pixmapVoltRelay))
        self.btn3.setIconSize(QSize(106,80))
        self.btn4.setIcon(QIcon(pixmapEmpty))
        self.btn4.setIconSize(QSize(106,80))
        self.btn5.setIcon(QIcon(pixmapDataLog))
        self.btn5.setIconSize(QSize(106,80))
        self.btn6.setIcon(QIcon(pixmapSettings))
        self.btn6.setIconSize(QSize(106,80))
        self.btn7.setIcon(QIcon(pixmapUManual))
        self.btn7.setIconSize(QSize(106,80))
        self.btn8.setIcon(QIcon(pixmapAbout))
        self.btn8.setIconSize(QSize(106,80))
        self.btn9.setIcon(QIcon(pixmapClose))
        self.btn9.setIconSize(QSize(50,50))

        self.btn1.clicked.connect(self.MCBTest)
        self.btn9.clicked.connect(self.closeFunction)
        
        topBox.addWidget(self.labelTemp)
        topBox.addWidget(self.labelTime)

        button1Box.addWidget(self.btn1)
        button1Box.addWidget(self.btn2)
        button1Box.addWidget(self.btn3)
        button1Box.addWidget(self.btn4)
        button2Box.addWidget(self.btn5)
        button2Box.addWidget(self.btn6)
        button2Box.addWidget(self.btn7)
        button2Box.addWidget(self.btn8)
        bottomBox.addWidget(self.btn9)
        
        mainVBox.addLayout(topBox)
        mainVBox.addLayout(button1Box)
        mainVBox.addLayout(button2Box)
        mainVBox.addLayout(bottomBox)
        
        clockTimer = QTimer(self)
        clockTimer.timeout.connect(self.showTime)
        clockTimer.start(1000)
        self.showTime()
        
        
       
        
        
        
        
        
        wid.setLayout(mainVBox)
        self.show()
        
    def showTime(self):
        now = datetime.datetime.now()
        now = now.strftime("%a %d-%m-%Y\n%I:%M:%S %p")
        self.labelTime.setText(now)
        
    def MCBTest(self):
        self.w = mcbWindow()
        self.w.show()
        
    def closeFunction(self):
        window.close()
        
class mcbWindow(QMainWindow):
    global sourceState
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MCB Test")
        left = 2
        top = 30
        width = 796
        height = 450
        self.setGeometry(left,  top, width, height)
        self.setFixedSize(width, height)
        
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        self.setStyleSheet("background-color: white;")
        
        mainVBox = QVBoxLayout()
        topBox = QHBoxLayout()
        bottomBox = QHBoxLayout()
        graphVBox = QVBoxLayout()
        settingsVBox = QVBoxLayout()
        buttonHBox = QHBoxLayout()
        
        #Designing TopBox
        self.labelTemp = QLabel(self)
        self.labelTemp.setAlignment(Qt.AlignLeft)
        self.labelTemp.setAlignment(Qt.AlignTop)
        self.labelTemp.setFixedHeight(40)
        self.labelTemp.setText("Temperature")
        self.labelTime = QLabel(self)
        self.labelTime.setAlignment(Qt.AlignRight)
        self.labelTime.setFixedHeight(40)
        self.labelTime.setText("Time")
        
        topBox.addWidget(self.labelTemp)
        topBox.addWidget(self.labelTime)
        
        clockTimer = QTimer(self)
        clockTimer.timeout.connect(self.showTime)
        clockTimer.start(1000)
        self.showTime()
        
        #Designing Graph anf Buttons
        self.plotMCB = MatplotlibWidget()
        self.plotMCB.setFixedSize(550,350)
        graphVBox.addWidget(self.plotMCB)
        
        self.backButton = QToolButton()
        self.backButton.setFixedSize(60,30)
        #self.backButton.setText("Back")
        self.backButton.clicked.connect(self.closeFunction)
        self.onButton = QToolButton()
        self.onButton.setFixedSize(60,30)
        self.onButton.setText("On")
        self.onButton.clicked.connect(self.onButtonFunction)
        self.onTimeButton = QToolButton()
        self.onTimeButton.setFixedSize(90,30)
        self.onTimeButton.setText("On+Time")
        self.onTimeButton.clicked.connect(self.onTimeButtonFunction)
        self.offButton = QToolButton()
        self.offButton.setFixedSize(60,30)
        self.offButton.setText("Off")
        self.offButton.clicked.connect(self.offButtonFunction)
        
        pixmapBack = QPixmap("Back.png")     
        self.backButton.setIcon(QIcon(pixmapBack))
        self.backButton.setIconSize(QSize(60,35))
        
        buttonHBox.addWidget(self.backButton)
        buttonHBox.addWidget(self.onButton)
        buttonHBox.addWidget(self.onTimeButton)
        buttonHBox.addWidget(self.offButton)
        graphVBox.addLayout(buttonHBox)
        
        #Designing Settings
        currentLabel = QLabel(self)
        currentLabel.setText("Maximim Current")
        currentLabel.setFont(QtGui.QFont("Calibri", 12))
        currentLabel.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.currentSelector = QComboBox()
        self.currentSelector.addItem("2.5 Amps")
        self.currentSelector.addItem("5 Amps")
        self.currentSelector.addItem("7.5 Amps")
        self.currentSelector.addItem("10 Amps")
        self.currentSelector.addItem("12.5 Amps")
        self.currentSelector.addItem("15 Amps")
        self.currentSelector.addItem("17.5 Amps")
        self.currentSelector.addItem("20 Amps")
        self.currentSelector.addItem("22.5 Amps")
        self.currentSelector.addItem("25 Amps")
        self.currentSelector.addItem("27.5 Amps")
        self.currentSelector.addItem("30 Amps")
        self.currentSelector.addItem("32.5 Amps")
        self.currentSelector.addItem("35 Amps")
        self.currentSelector.addItem("37.5 Amps")
        self.currentSelector.addItem("40 Amps")
        self.currentSelector.addItem("42.5 Amps")
        self.currentSelector.addItem("45 Amps")
        self.currentSelector.currentIndexChanged.connect(self.currentChange)
        
        timeLabel = QLabel(self)
        timeLabel.setText("Maximim Time")
        timeLabel.setFont(QtGui.QFont("Calibri", 12))
        timeLabel.setAlignment(Qt.AlignCenter)
        self.timeSelector = QComboBox()
        self.timeSelector.addItem("5 Sec")
        self.timeSelector.addItem("10 Sec")
        self.timeSelector.addItem("15 Sec")
        self.timeSelector.addItem("20 Sec")
        self.timeSelector.addItem("25 Sec")
        self.timeSelector.addItem("30 Sec")
        self.timeSelector.addItem("35 Sec")
        self.timeSelector.addItem("40 Sec")
        self.timeSelector.addItem("45 Sec")
        self.timeSelector.addItem("50 Sec")
        self.timeSelector.addItem("55 Sec")
        self.timeSelector.addItem("60 Sec")
        self.timeSelector.addItem("65 Sec")
        self.timeSelector.addItem("70 Sec")
        self.timeSelector.addItem("75 Sec")
        self.timeSelector.addItem("80 Sec")
        self.timeSelector.addItem("85 Sec")
        self.timeSelector.addItem("90 Sec")
        self.timeSelector.currentIndexChanged.connect(self.timeChange)
        
        self.timeVal = QLabel(self)
        self.currVal = QLabel(self)
        self.timeVal.setText("Time: ------- Sec")
        self.currVal.setText("Current: ----- Amps")
        self.timeVal.setFont(QtGui.QFont("Calibri", 12))
        self.timeVal.setAlignment(Qt.AlignCenter)
        self.currVal.setFont(QtGui.QFont("Calibri", 12))
        self.currVal.setAlignment(Qt.AlignCenter)
        
        updateGraphButton = QToolButton()
        updateGraphButton.setText("Update Graph")
        logButton = QToolButton()
        logButton.setText("LogData")
        logButton.setFixedSize(113,30)
        extra2Button = QToolButton()
        extra2Button.setText("Extra")
        
        self.status = QLabel(self)
        self.status.setText("Status: MCB Test Interface Initiated")
        self.status.setAlignment(Qt.AlignLeft)
        self.status.setFont(QtGui.QFont("Calibri", 12))
        
        settingsVBox.addWidget(currentLabel)
        settingsVBox.addWidget(self.currentSelector)
        settingsVBox.addWidget(timeLabel)
        settingsVBox.addWidget(self.timeSelector)
        settingsVBox.addWidget(self.currVal)
        settingsVBox.addWidget(self.timeVal)
        settingsVBox.addWidget(updateGraphButton, alignment=Qt.AlignCenter)
        settingsVBox.addWidget(logButton, alignment=Qt.AlignCenter)
        settingsVBox.addWidget(extra2Button, alignment=Qt.AlignCenter)
        settingsVBox.addWidget(self.status)
        
        
        
        bottomBox.addLayout(graphVBox)
        bottomBox.addLayout(settingsVBox)
        mainVBox.addLayout(topBox)
        mainVBox.addLayout(bottomBox)
        
        
        wid.setLayout(mainVBox)
        self.show()
        
    def showTime(self):
       now = datetime.datetime.now()
       now = now.strftime("%a %d-%m-%Y\n%I:%M:%S %p")
       self.labelTime.setText(now)
       
    def onButtonFunction(self):
       global sourceState
       GPIO.output(21, GPIO.HIGH)
       sourceState = 1
       self.status.setText("Status: Source Turned On Manually")
       while(True):
           QtCore.QTimer.singleShot(10, self.currentSensing)
           time.sleep(0.05)
           if(sourceState == 0):
              self.status.setText("Status: Source Turned Off Manually")
              break
           QtCore.QCoreApplication.processEvents()
           
    def run(self):
        global currTime
        start = time.time()
        while True: 
            #print('thread running') 
            global stop_threads
            end = time.time()
            currTime = end-start
            self.timeVal.setText("Time: {:0.2f} Sec".format(currTime))
            time.sleep(0.01)

            if stop_threads: 
                break
           
       
    def onTimeButtonFunction(self):
       global sourceState
       global maxTime
       global maxCurrent
       global stop_threads
       global currTime
       global amp
       amp = 0.1
       GPIO.output(21, GPIO.HIGH)
       sourceState = 1
       self.status.setText("Status: Source Turned On Manually")
       
       stop_threads = False
       t1 = threading.Thread(target = self.run) 
       t1.start() 
       while(True):
           QtCore.QTimer.singleShot(0, self.currentSensing)
           #time.sleep(0.05)
           if(sourceState == 0):
               self.status.setText("Status: Source Turned Off Manually")
               break
           if(currTime >= maxTime):
               self.status.setText("Status: Maximum Time Reached     ")
               GPIO.output(21, GPIO.LOW)
               sourceState = 0
               break
           if(amp <= 0):
               self.status.setText("Status: MCB Tripped Successfully")
               GPIO.output(21, GPIO.LOW)
               sourceState = 0
               amp = 0.1
               break
           QtCore.QCoreApplication.processEvents()
           
       stop_threads = True
       t1.join() 
       print('thread killed') 
           

    def currentSensing(self):
        global GAIN 
        global count 
        global maxVal 
        global amp 
        series = [0]*count
        value = 0
        for i in range (count):
            value = adc.read_adc(0, gain=GAIN)
            #print(value)
            time.sleep(0.001)
            series[i] = value
            QtCore.QCoreApplication.processEvents()
        maxVal = max(series)
        
        amp = -0.00000000000003*(maxVal**3) + 0.0000000023*(maxVal**2) + 0.0014*maxVal + 0.4
        amp = round(amp,1)
        #print("Init Amp = " + str(amp))
        
        if(amp < 0.3): amp = 0
        #print(amp)
        self.currVal.setText("Current: {:0.2f} Amps".format(amp))
        QtCore.QCoreApplication.processEvents()
       
    def offButtonFunction(self):
       global sourceState
       GPIO.output(21, GPIO.LOW)
       sourceState = 0
       print(sourceState)
       
    
     
       
       
    def currentChange(self,i):
       global maxCurrent
       maxCurrent = (i+1)*2.5
       #print((i+1)*2.5)
       
    def timeChange(self,i):
       global maxTime
       maxTime = (i+1)*5
       #print((i+1)*5)
       
    def closeFunction(self):
       global sourceState
       GPIO.output(21, GPIO.LOW)
       sourceState = 0
       self.close()
       
class MatplotlibWidget(FigureCanvas):
    def __init__(self, parent=None, xlim = 100,ylim = 50, hold=False):
        super(MatplotlibWidget, self).__init__(Figure())       
        self.setParent(parent)
        self.figure = Figure(figsize=(5, 1),dpi = 95)
        self.canvas = FigureCanvas(self.figure)
            
        self.axes = self.figure.add_subplot(111)
        
        self.axes.set_title("TCC Curve")
        self.axes.set_xlabel("Time (Sec)")
        self.axes.set_ylabel("Current (Amps)")
        self.axes.set_xbound(lower = 0, upper = xlim)
        self.axes.set_ylim( bottom = 0, top = 50)
    
if __name__ == "__main__":
    
    App = QApplication(sys.argv)
    print("Window Initiated")
    window = Window()
    sys.exit(App.exec())
