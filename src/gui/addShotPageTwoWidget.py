'''
Created on 19.01.2015

@author: Florian
'''
from PyQt4.QtGui import QGridLayout, QLabel, QPushButton, QPixmap, QIcon,\
    QButtonGroup, QVBoxLayout, QWidget, QFont
from PyQt4.Qt import QHBoxLayout, qDebug

class PageTwoWidget(QWidget):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(PageTwoWidget, self).__init__(parent)
        
        self.guiFont = QFont("Arial", 14)
        self.selectorLayout = QGridLayout()
        self.pageLabel = QLabel("Select Camera")
        self.checkableButtonGroup = QButtonGroup()
        self.checkableButtonGroup.setExclusive(True)
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.pageLabel)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.selectorLayout)
        self.mainLayout.addStretch()
        
        self.setLayout(self.mainLayout)
        
    def populateCameras(self, clientList):
        iteratr = 0
        qDebug("populating cameras")
        for camera in clientList:
            cameraSelector = QPushButton(camera[0])
            cameraSelector.setCheckable(True)
            cameraSelector.setFont(self.guiFont)
            cameraSelector.setFixedHeight(64)
            #shotTypeSelectorPikto = QPixmap("img" + shotType + ".png")
            #cameraSelector.setIcon(QIcon(shotTypeSelectorPikto))
            self.checkableButtonGroup.addButton(cameraSelector)
            
            self.selectorLayout.addWidget(cameraSelector, iteratr / 4, iteratr%4)
            print("CAMERA_" + str(iteratr) + "ADDED")
            iteratr += 1
            
            #self.selectorLayout.addWidget(cameraSelector, 1 if iteratr>4 else 0, iteratr%4)
                   
            
            