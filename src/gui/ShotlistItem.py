'''
Created on 08.01.2015

@author: Florian
'''
from PyQt4.QtGui import QWidget, QPixmap, QLabel, QPushButton, QHBoxLayout,\
    QVBoxLayout

class ShotlistItem(QWidget):
    
    def __init__(self,parent=None):
        super(ShotlistItem, self).__init__(parent)
        shotPicto = QPixmap()
        shotPictoLabel = QLabel("shotPicto")
        shotPictoLabel.setPixmap(shotPicto)
        shotSource = QLabel("SOURCEID")
        moveToFrontBtn = QPushButton("<-")
        moveToBackBtn = QPushButton("->")
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(moveToFrontBtn)
        buttonLayout.addWidget(moveToBackBtn)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(shotPictoLabel)
        mainLayout.addLayout(buttonLayout)
        
    def changePosition(self):
        return        