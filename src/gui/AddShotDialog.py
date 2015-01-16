'''
Created on 11.01.2015

@author: Florian
'''
from PyQt4.Qt import QDialog
from PyQt4.QtGui import QPushButton, QPixmap, QVBoxLayout, QHBoxLayout, QLabel
from PyQt4.uic.uiparser import ButtonGroup
from PyQt4.QtCore import pyqtSignal

class AddShotDialog(QDialog):
    '''
    classdocs
    '''

    newShot = pyqtSignal(list)
    
    def __init__(self, parent):
        '''
        Constructor
        '''
        super(AddShotDialog, self).__init__(parent)
        shotTypes = list("establisher", "master", "wide", "two", "overtheshoulder", "medium", "closeup", "xtrm_closeup")
        okBtn = QPushButton()
        cancelBtn = QPushButton()
        
        shotSelector = ButtonGroup()
        establisherBtn = QPushButton(QPixmap("img/establisher.png"))
        masterBtn = QPushButton(QPixmap("img/master.png"))
        wideBtn = QPushButton(QPixmap("img/wide.png"))
        twoBtn = QPushButton(QPixmap("img/two.png"))
        otsBtn = QPushButton(QPixmap("img/ots.png"))
        mediumBtn = QPushButton(QPixmap("img/medium.png"))
        closeUpBtn = QPushButton(QPixmap("img/closeup.png"))
        xtrmCloseUpBtn = QPushButton(QPixmap("img/xtrm_closeup.png"))
        shotSelector.add(establisherBtn)
        shotSelector.add(masterBtn)
        shotSelector.add(wideBtn)
        shotSelector.add(twoBtn)
        shotSelector.add(otsBtn)
        shotSelector.add(mediumBtn)
        shotSelector.add(closeUpBtn)
        shotSelector.add(xtrmCloseUpBtn)
        page1HeadingLbl = QLabel("Select Shot-Type")
        page2HeadingLbl = QLabel("Select Camera")
        page1CancelBtn = QPushButton("Cancel")
        page1NextBtn = QPushButton("Next")
        page2BackBtn = QPushButton("Back")
        page2OkBtn = QPushButton("OK")
        shotSelector.setExclusive(True)
        page1SrcBtnFirstRow = QHBoxLayout()
        page1SrcBtnSecondRow = QHBoxLayout()
        page1SrcBtnFirstRow.addWidget(establisherBtn)
        page1SrcBtnFirstRow.addWidget(masterBtn)
        page1SrcBtnFirstRow.addWidget(wideBtn)
        page1SrcBtnFirstRow.addWidget(twoBtn)
        page1SrcBtnSecondRow.addWidget(otsBtn)
        page1SrcBtnSecondRow.addWidget(mediumBtn)
        page1SrcBtnSecondRow.addWidget(closeUpBtn)
        page1SrcBtnSecondRow.addWidget(xtrmCloseUpBtn)
        page1BtnLayout = QHBoxLayout()
        page1BtnLayout.addWidget(page1CancelBtn)
        page1BtnLayout.addStretch()
        page1BtnLayout.addWidget(page1NextBtn)
        page2BtnLayout = QHBoxLayout()
        page2BtnLayout.addWidget(page2BackBtn)
        page2BtnLayout.addStretch()
        page2BtnLayout.addWidget(page2OkBtn)
        camSelector = ButtonGroup()
        camSelector.setExclusive(True)
        camBtnLayout = QHBoxLayout()
        page1mainLayout = QVBoxLayout()
        page2mainLayout = QVBoxLayout()
        
        page1mainLayout.addWidget(page1HeadingLbl)
        page1mainLayout.addSpacing(10)
        page1mainLayout.addLayout(page1SrcBtnFirstRow)
        page1mainLayout.addLayout(page1SrcBtnSecondRow)
        page1mainLayout.addSpacing(10)
        page1mainLayout.addLayout(page1BtnLayout)
        
        page2mainLayout.addWidget(page2HeadingLbl)
        page2mainLayout.addSpacing(10)
        page2mainLayout.addLayout(camBtnLayout)
        page2mainLayout.addStretch()
        page2mainLayout.addLayout(page2BtnLayout)
        
        self.setLayout(page1mainLayout)
        
    def connectSignals(self):
       pass #connect signals here
    
    def setupCamselector(self, camlist):
        pass # fill camselector here
    
    def nextPage(self):
        pass #add handling for next page here
    
    def previousPage(self):
        pass # add handling for going to previous page here
    
    def confirmShot(self):
        pass # emit okbtn clicked signal here for further processing of the shot