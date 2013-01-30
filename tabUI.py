import os, sys, time, threading, Queue
from PyQt4 import QtGui, QtCore
import serial
from digitalClock import DigitalClock

SERIALPORT = "/dev/tty.usbserial-A700fpRz"
BAUD = 57600

class MainWindow(QtGui.QWidget):
    def __init__(self, queue, endcommand, *args):
        QtGui.QWidget.__init__(self, *args)
        self.queue = queue
        self.setGeometry(0, 0, 800, 480)
        self.setWindowTitle("Jeeves")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.resize(800, 480)
        self.setMinimumSize(800, 480)
        self.center()       
      
        self.tab_widget = QtGui.QTabWidget()
        self.tab_widget.setStyleSheet("QTabWidget { font: 30pt; } QTabWidget::tab-bar { alignment: center; } ")
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
        self.tab4 = QtGui.QWidget()
              
        self.tab_widget.addTab(self.tab1, "Main")
        self.tab_widget.addTab(self.tab2, "Automation")
        self.tab_widget.addTab(self.tab3, "Climate")
        self.tab_widget.addTab(self.tab4, "Security")
        
        
        self.calendarWidget = QtGui.QCalendarWidget(self.tab1)
        self.calendarWidget.setGeometry(QtCore.QRect(340, 20, 380, 250))
        self.calendarWidget.setObjectName("calendarWidget")
        
        self.currentWeatherBox = QtGui.QGroupBox(self.tab1)
        self.currentWeatherBox.setGeometry(QtCore.QRect(30, 180, 290, 200))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.currentWeatherBox.setFont(font)
        self.currentWeatherBox.setAlignment(QtCore.Qt.AlignCenter)
        self.currentWeatherBox.setObjectName("currentWeatherBox")
        #self.weatherRadar = QtWebKit.QWebView(self.currentWeatherBox)
        self.outdoorWeatherTemp = QtGui.QLabel(self.currentWeatherBox)
        self.outdoorWeatherTemp.setGeometry(QtCore.QRect(10, 10, 230, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.outdoorWeatherTemp.setFont(font)
        self.outdoorWeatherTemp.setObjectName("outdoorWeatherTemp")
        self.indoorWeatherTemp = QtGui.QLabel(self.currentWeatherBox)
        self.indoorWeatherTemp.setGeometry(QtCore.QRect(10, 40, 230, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.indoorWeatherTemp.setFont(font)
        self.indoorWeatherTemp.setObjectName("indoorWeatherTemp")
        
        self.fortuneBox = QtGui.QGroupBox(self.tab1)
        self.fortuneBox.setGeometry(QtCore.QRect(340, 290, 380, 90))
        
        self.digitalClock = DigitalClock(self.tab1)
        self.digitalClock.setGeometry(QtCore.QRect(30, 20, 290, 140))
        self.digitalClock.setObjectName("digitalClock")
        
        box = QtGui.QGridLayout()
        box.addWidget(self.tab_widget)
        
        self.setLayout(box)
        self.endcommand = endcommand
        
    def closeEvent(self, ev):
        self.endcommand()

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                data = msg.split(',')
                if msg.endswith('*') and msg.startswith('$') and len(data)==11:
                    self.outdoorWeatherTemp.setText('Outdoor Temperature: ' + data[1] + 'F')
                    print "Debug: Outdoor Temp: " + data[1] + 'F'
                elif msg.endswith('*') and msg.startswith('$') and data[3]=="indoor":
                    self.indoorWeatherTemp.setText('Indoor Temperature: ' + data[1] + 'F')
                    print "Debug: Outdoor Temp: " + data[1] + 'F'
            except Queue.Empty:
                pass
    
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self):
        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui = MainWindow(self.queue, self.endApplication)
        self.gui.show()

        # A timer to periodically call periodicCall :-)
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer,
                           QtCore.SIGNAL("timeout()"),
                           self.periodicCall)
        # Start the timer -- this replaces the initial call to periodicCall
        self.timer.start(100)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            root.quit()

    def endApplication(self):
        self.running = 0

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. 
        Put your stuff here.
        """
        while self.running:
            ser = serial.Serial(SERIALPORT, BAUD)
            msg = ser.readline()[:-2]
            if (msg):
                self.queue.put(msg)
            else: pass  
            ser.close()

root = QtGui.QApplication(sys.argv)
client = ThreadedClient()
sys.exit(root.exec_())