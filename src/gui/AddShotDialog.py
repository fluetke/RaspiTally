'''
Created on 11.01.2015

@author: Florian
'''
from PyQt4.Qt import QDialog
from PyQt4.QtGui import QPushButton, QPixmap, QVBoxLayout, QHBoxLayout, QLabel,\
    QButtonGroup
from PyQt4.QtCore import pyqtSignal

class AddShotDialog(QDialog):
    '''
    classdocs
    '''

    newShot = pyqtSignal(list)
    shotPos=0
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(AddShotDialog, self).__init__(parent)
        self.shotTypes = ["establisher", "master", "wide", "two", "overtheshoulder", "medium", "closeup", "xtrm_closeup"]
        self.okBtn = QPushButton()
        self.cancelBtn = QPushButton()
        
        self.shotSelector = QButtonGroup()
        self.establisherBtn = QPushButton("Esta")
        self.estaPicto = QPixmap("img/Closeup.png")
        #establisherBtn.
        self.masterBtn = QPushButton("Master")
        self.masterPicto = QPixmap("img/medium.png")
        self.wideBtn = QPushButton("Wide")
        
        self.twoBtn = QPushButton("Two")
        self.otsBtn = QPushButton("OTS")
        self.mediumBtn = QPushButton("Medium")
        self.closeUpBtn = QPushButton("Close")
        self.xtrmCloseUpBtn = QPushButton("XClose")
        self.shotSelector.addButton(self.establisherBtn)
        self.shotSelector.addButton(self.masterBtn)
        self.shotSelector.addButton(self.wideBtn)
        self.shotSelector.addButton(self.twoBtn)
        self.shotSelector.addButton(self.otsBtn)
        self.shotSelector.addButton(self.mediumBtn)
        self.shotSelector.addButton(self.closeUpBtn)
        self.shotSelector.addButton(self.xtrmCloseUpBtn)
        self.page1HeadingLbl = QLabel("Select Shot-Type")
        self.page2HeadingLbl = QLabel("Select Camera")
        self.page1CancelBtn = QPushButton("Cancel")
        self.page1NextBtn = QPushButton("Next")
        self.page2BackBtn = QPushButton("Back")
        self.page2OkBtn = QPushButton("OK")
        self.shotSelector.setExclusive(True)
        self.page1SrcBtnFirstRow = QHBoxLayout()
        self.page1SrcBtnSecondRow = QHBoxLayout()
        self.page1SrcBtnFirstRow.addWidget(self.establisherBtn)
        self.page1SrcBtnFirstRow.addWidget(self.masterBtn)
        self.page1SrcBtnFirstRow.addWidget(self.wideBtn)
        self.page1SrcBtnFirstRow.addWidget(self.twoBtn)
        self.page1SrcBtnSecondRow.addWidget(self.otsBtn)
        self.page1SrcBtnSecondRow.addWidget(self.mediumBtn)
        self.page1SrcBtnSecondRow.addWidget(self.closeUpBtn)
        self.page1SrcBtnSecondRow.addWidget(self.xtrmCloseUpBtn)
        self.page1BtnLayout = QHBoxLayout()
        self.page1BtnLayout.addWidget(self.page1CancelBtn)
        self.page1BtnLayout.addStretch()
        self.page1BtnLayout.addWidget(self.page1NextBtn)
        self.page2BtnLayout = QHBoxLayout()
        self.page2BtnLayout.addWidget(self.page2BackBtn)
        self.page2BtnLayout.addStretch()
        self.page2BtnLayout.addWidget(self.page2OkBtn)
        self.camSelector = QButtonGroup()
        self.camSelector.setExclusive(True)
        self.camBtnLayout = QHBoxLayout()
        self.page1mainLayout = QVBoxLayout()
        self.page2mainLayout = QVBoxLayout()
        
        self.page1mainLayout.addWidget(self.page1HeadingLbl)
        self.page1mainLayout.addSpacing(10)
        self.page1mainLayout.addLayout(self.page1SrcBtnFirstRow)
        self.page1mainLayout.addLayout(self.page1SrcBtnSecondRow)
        self.page1mainLayout.addSpacing(10)
        self.page1mainLayout.addLayout(self.page1BtnLayout)
        
        self.page2mainLayout.addWidget(self.page2HeadingLbl)
        self.page2mainLayout.addSpacing(10)
        self.page2mainLayout.addLayout(self.camBtnLayout)
        self.page2mainLayout.addStretch()
        self.page2mainLayout.addLayout(self.page2BtnLayout)
        
        self.setLayout(self.page1mainLayout)
        
        #connect signals and slots
        self.page1NextBtn.clicked.connect(self.nextPage)
        self.page2BackBtn.clicked.connect(self.previousPage)
        self.page1CancelBtn.clicked.connect(self.close)
    
    def storePos(self, pos):
        self.shotPos = pos
    
    def setupCamselector(self, camlist):
        pass # fill camselector here
    
    def nextPage(self):
        self.setLayout(self.page2mainLayout)
    
    def previousPage(self):
        self.setLayout(self.page1mainLayout)
        
    def getShotPos(self):
        return self.shotPos
    
    def getShot(self):
        pass