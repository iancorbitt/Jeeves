###########################################################################
# This was copied from Mikael Halen from his page on popdevelop.com
# http://popdevelop.com/2010/05/an-example-on-how-to-make-qlabel-clickable/
###########################################################################

from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
    
class ExtendedQLabel(QLabel):  
   
    def __init(self, parent):  
        QLabel.__init__(self, parent)  
      
    def mouseReleaseEvent(self, ev):  
        self.emit(SIGNAL('clicked()'))  
      