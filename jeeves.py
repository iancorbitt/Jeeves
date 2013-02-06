####################################################
# Jeeves v0.1
# Ian Corbitt, 2013
#
# I'm too lazy to read into the licensing bits, so I'll just say
# that if you use my code, cool, drop me a line
####################################################

import os, sys, time, threading, Queue
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import serial
from digitalClock import DigitalClock
import ExtendQLabel

####################################################
# Variables required
####################################################
# Serial Port Settings
SERIALPORT = "/dev/tty.usbserial-A700fpRz"
BAUD = 57600
# Quote rotation time
FORTUNETIME = 120000
####################################################
# Edit at your own risk below this line

class MainWindow(QtGui.QWidget):
    def __init__(self, queue, endcommand, *args):
        QtGui.QWidget.__init__(self, *args)
        self.queue = queue
        
        # All of the geometry throughout is set for the 7" LCD Cape for the Beaglebone (800x480 resolution)
        
        self.setGeometry(0, 0, 800, 480)
        self.setWindowTitle("Jeeves")
        self.resize(800, 480)
        self.setMinimumSize(800, 480)
        self.center()       
        
        # The stylesheet can be changed to your liking, but I tried to keep it simple and portable across platforms
        
        self.tab_widget = QtGui.QTabWidget()
        self.tab_widget.setStyleSheet("QTabWidget { font: 30pt; font-family: Arial; button-layout: 2 } QTabWidget::tab-bar { alignment: center; } ")
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
        self.tab4 = QtGui.QWidget()
              
        self.tab_widget.addTab(self.tab1, "Main")
        self.tab_widget.addTab(self.tab2, "Automation")
        self.tab_widget.addTab(self.tab3, "Climate")
        self.tab_widget.addTab(self.tab4, "Security")
        
        self.slideSwitchOn = QtGui.QPixmap("content/on.png")
        self.slideSwitchOff = QtGui.QPixmap("content/off.png")
        self.livingRoomLightsSwitchState = False
        self.livingRoomLightsSwitchLabel = ExtendQLabel.ExtendedQLabel(self.tab2)
        self.livingRoomLightsSwitchLabel.setPixmap(QtGui.QPixmap(self.slideSwitchOff))
        self.livingRoomLightsSwitchLabel.move(100, 100)
        self.connect(self.livingRoomLightsSwitchLabel, QtCore.SIGNAL('clicked()'), self.changeSwitchState)
        
        self.calendarWidget = QtGui.QCalendarWidget(self.tab1)
        self.calendarWidget.setGeometry(QtCore.QRect(350, 20, 385, 200))
        self.calendarWidget.setSelectionMode(QtGui.QCalendarWidget.NoSelection)
        self.calendarWidget.setObjectName("calendarWidget")
        
        # The weatherTemp labels are left invisible (unset) until they're populated
        # because I don't like looking at blank data, and it helps flag a non working
        # serial connection
        self.currentWeatherBox = QtGui.QGroupBox(self.tab1)
        self.currentWeatherBox.setGeometry(QtCore.QRect(30, 180, 290, 200))
        self.currentWeatherBox.setAlignment(QtCore.Qt.AlignCenter)
        self.currentWeatherBox.setObjectName("currentWeatherBox")
        self.outdoorWeatherTemp = QtGui.QLabel(self.currentWeatherBox)
        self.outdoorWeatherTemp.setGeometry(QtCore.QRect(10, 10, 250, 30))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setFamily("Verdana")
        self.outdoorWeatherTemp.setFont(font)
        self.outdoorWeatherTemp.setObjectName("outdoorWeatherTemp")
        self.indoorWeatherTemp = QtGui.QLabel(self.currentWeatherBox)
        self.indoorWeatherTemp.setGeometry(QtCore.QRect(10, 40, 250, 30))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setFamily("Verdana")
        self.indoorWeatherTemp.setFont(font)
        self.indoorWeatherTemp.setObjectName("indoorWeatherTemp")
        
        self.fortuneText = QtGui.QTextEdit(self.tab1)
        self.fortuneText.setGeometry(QtCore.QRect(350, 290, 385, 90))
        self.fortuneText.setTextInteractionFlags(Qt.TextInteractionFlag(0)) # I don't want any interaction allowed, so the 0 flag is set
        
        self.digitalClock = DigitalClock(self.tab1)
        self.digitalClock.setGeometry(QtCore.QRect(30, 20, 290, 140))
        self.digitalClock.setObjectName("digitalClock")
        
        box = QtGui.QGridLayout()
        box.addWidget(self.tab_widget)
        
        self.setLayout(box)
        self.endcommand = endcommand
        
    def closeEvent(self, ev):
        self.endcommand()
    
    def changeSwitchState(self):
        if self.livingRoomLightsSwitchState == False:
            self.livingRoomLightsSwitchLabel.setPixmap(QtGui.QPixmap(self.slideSwitchOn))
            self.livingRoomLightsSwitchState = True
            print("Set to on")
        elif self.livingRoomLightsSwitchState == True:
            self.livingRoomLightsSwitchLabel.setPixmap(QtGui.QPixmap(self.slideSwitchOff))
            self.livingRoomLightsSwitchState = False
            print("Set to off")

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message to ensure validity and process valid ones
                # Debug lines are commented out, uncomment for testing
                data = msg.split(',')
                if msg.endswith('*') and msg.startswith('$') and len(data)==11:
                    self.outdoorWeatherTemp.setText('Outdoor Temperature: ' + data[1] + 'F')
                    #print "Debug: Outdoor Temp: " + data[1] + 'F'
                elif msg.endswith('*') and msg.startswith('$') and data[3]=="indoor":
                    self.indoorWeatherTemp.setText('Indoor Temperature: ' + data[1] + 'F')
                    #print "Debug: Outdoor Temp: " + data[1] + 'F'
            except Queue.Empty:
                pass
    
    def processFortune(self):
        # You can change this to use which ever fortune script you like
        cmd = "fortune"
        stdouterr = os.popen4(cmd)[1].read()
        self.fortuneText.setText(stdouterr)
    
    def center(self):
        # This is here to ensure the widget is centered, it might go away if testing shows it isn't needed
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


class ThreadedClient:
    def __init__(self):
        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui = MainWindow(self.queue, self.endApplication)
        self.gui.show()
        self.periodicFortune()

        # Timers to periodically call periodicSerial and periodicFortune
        self.serialTimer = QtCore.QTimer()
        QtCore.QObject.connect(self.serialTimer,
                           QtCore.SIGNAL("timeout()"),
                           self.periodicSerial)
        self.serialTimer.start(100)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()
        
        self.fortuneTimer = QtCore.QTimer()
        QtCore.QObject.connect(self.fortuneTimer,
                               QtCore.SIGNAL("timeout()"),
                               self.periodicFortune)
        self.fortuneTimer.start(FORTUNETIME)
        
    def periodicFortune(self):
        self.gui.processFortune()

    def periodicSerial(self):
        # I chose to check for self.running here due to my more rapid call here
        self.gui.processIncoming()
        if not self.running:
            root.quit()
    
    def endApplication(self):
        self.running = 0

    def workerThread1(self):
        # Thread for reading the serial port
        while self.running:
            ser = serial.Serial(SERIALPORT, BAUD)
            msg = ser.readline()[:-2] # Strip those end-line characters...possibly not needed but required for my setup
            if (msg):
                self.queue.put(msg)
            else: pass  
            ser.close()

root = QtGui.QApplication(sys.argv)
client = ThreadedClient()
sys.exit(root.exec_())