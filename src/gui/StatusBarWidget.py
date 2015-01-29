'''
Created on 08.01.2015

@author: Florian
'''
from PyQt4.QtGui import QWidget, QLabel, QPixmap, QColor, QHBoxLayout

class StatusBarWidget(QWidget):
    
    def __init__(self, parent=None):
        super(StatusBarWidget, self).__init__(parent)
        
        self.statusLabel = QLabel("UNDEFINED")
        #Generate Pixmap for colored status indicator
        self.indicatorSquare = QPixmap(48,48)
        self.indicatorSquare.fill(QColor(127,255,255))
        self.statusIndicatorL = QLabel()
        self.statusIndicatorR = QLabel()
        self.statusIndicatorL.setPixmap(self.indicatorSquare)
        self.statusIndicatorR.setPixmap(self.indicatorSquare)
        
        #add layouts for status widget
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.statusIndicatorL)
        self.mainLayout.addWidget(self.statusLabel)
        self.mainLayout.addWidget(self.statusIndicatorR)
        self.setLayout(self.mainLayout)
        
    # this method acts as a slot for state-changed signals
    # it updates the statusDisplay color and label text
    def changeStatus(self, status):
    # reset indicator to unknown state
        indicatorColor = QColor(127, 127, 127)
        indicatorText = "UNDEFINED"
        
        if status == "OFF":
            indicatorColor = QColor(0, 255, 0)
            indicatorText = "STAND BY"
        elif status == "PREVIEW":
            indicatorColor = QColor(255, 255, 0)
            indicatorText = "GET READY"
        elif status == "LIVE":
            indicatorColor = QColor(255, 0, 0)
            indicatorText = "ON AIR"
#       elif status == TState.error: #TODO IMPLEMENT THIS
#           indicatorColor = QColor(0,0,0)
#           indicatorText == "EMERGENCY(OFF)"
#             
        self.indicatorSquare.fill(indicatorColor)
        self.statusLabel.setText(indicatorText)        
