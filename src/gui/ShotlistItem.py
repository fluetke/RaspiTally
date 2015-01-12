'''
Created on 08.01.2015

@author: Florian
'''
from PyQt4.QtGui import QWidget, QPixmap, QLabel, QPushButton, QHBoxLayout,\
    QVBoxLayout, QApplication, QListWidgetItem
from PyQt4.Qt import qDebug

class ShotlistItem(QWidget):
    
    def __init__(self,shotType, parent=None):
        super(ShotlistItem, self).__init__(parent)
        
        #init widgets used in this widget
        shotPicto = QPixmap("gui/img/"+shotType+".png")
       # qDebug(QApplication.+"/gui/img/medium.png")
        shotPictoLbl = QLabel("shotPicto")
        shotClientIdLbl = QLabel("CAM_ID")
        moveToFrontBtn = QPushButton("<-")
        moveToBackBtn = QPushButton("->")
        clientIdLbl = QLabel("CAM_1")
        
        #init layouts
        buttonLayout = QHBoxLayout()
        mainLayout = QVBoxLayout()
        
        #setup layouts
        buttonLayout.addWidget(moveToFrontBtn)
        buttonLayout.addWidget(moveToBackBtn)
        mainLayout.addWidget(clientIdLbl)
        mainLayout.addWidget(shotPictoLbl)
        mainLayout.addLayout(buttonLayout)
        
        #init components
        shotPictoLbl.setPixmap(shotPicto)
        shotPictoLbl.setFixedHeight(120)
        moveToBackBtn.setFixedHeight(64)
        moveToFrontBtn.setFixedHeight(64)
        shotPictoLbl.setAutoFillBackground(True)
        shotPictoLbl.setStyleSheet("background:#ffffff;")
        self.setLayout(mainLayout)
            
        #setup fenster
        self.setFixedWidth(200)    
        self.setAutoFillBackground(True)
        
        
    def changePosition(self):
        return