'''
Created on 08.01.2015

@author: Florian
'''
from PyQt4.QtGui import QWidget, QLabel, QPixmap, QColor, QHBoxLayout
from PyQt4.Qt import qDebug, QFont
from PyQt4.QtCore import Qt
class StatusBarWidget(QWidget):
    
    def __init__(self, parent=None):
        super(StatusBarWidget, self).__init__(parent)
        self.guiFont = QFont("Arial", 18)
        self.statusLabel = QLabel("UNDEFINED")
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setFont(self.guiFont)
        
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
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.statusLabel)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.statusIndicatorR)
        self.setLayout(self.mainLayout)
        
    # this method acts as a slot for state-changed signals
    # it updates the statusDisplay color and label text
    def changeStatus(self, status):
    # reset indicator to unknown state
        indicatorColor = QColor(127, 127, 127)
        indicatorText = "UNDEFINED"
        qDebug("StatusBarWidget::requested Status is " + str(status))
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
        self.statusIndicatorL.setPixmap(self.indicatorSquare)
        self.statusIndicatorR.setPixmap(self.indicatorSquare)
        self.statusLabel.setText(indicatorText)        
