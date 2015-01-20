'''
Created on 08.01.2015

@author: Florian
'''
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,\
    QListWidget, QApplication, QGridLayout
from gui.StatusBarWidget import StatusBarWidget
from gui.ShotlistItem import ShotlistItem
from gui.VideoWidget import VideoWidget
from PyQt4.QtCore import pyqtSignal
from PyQt4 import QtCore
from gui.AddShotDialog import AddShotDialog
from PyQt4.Qt import qDebug


class MainWindow(QWidget):
    '''
    classdocs
    '''
        
    addShotAtPos = pyqtSignal(object, int)
    delShotAtPos = pyqtSignal(int)
    movShotUp = pyqtSignal(int)
    movShotDown = pyqtSignal(int)
    
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        ##setup all Widgets
        # display area
        self.tallyState = StatusBarWidget()
        self.tallyState.setFixedSize(384,64)
        self.liveMonitor = VideoWidget()
        self.sourceList = QListWidget()
        self.quitBtn = QPushButton("&Quit")
        self.quitBtn.setFixedSize(64,64)
        self.quitBtn.clicked.connect(QApplication.quit)
        
        # interaction area
        self.shotlist = QListWidget()
        self.emergencyBtn = QPushButton("&EMERGENCY")
        self.goLiveBtn = QPushButton("GO &LIVE")
        self.nextBtn = QPushButton("&NEXT")
        
        #layout definition
        mainLayout = QVBoxLayout()
        statusLayout = QHBoxLayout()
        previewLayout = QHBoxLayout()
        actionBarLayout = QHBoxLayout()
        
        # fill layouts 
        statusLayout.addStretch(192)
        statusLayout.addWidget(self.tallyState)
        statusLayout.addStretch(128)
        statusLayout.addWidget(self.quitBtn)
        
        previewLayout.addWidget(self.liveMonitor)
        previewLayout.addWidget(self.sourceList)
        
        actionBarLayout.addStretch()
        actionBarLayout.addWidget(self.emergencyBtn)
        actionBarLayout.addWidget(self.goLiveBtn)
        actionBarLayout.addWidget(self.nextBtn)
        actionBarLayout.addStretch()
                
        mainLayout.addLayout(statusLayout)
        mainLayout.addLayout(previewLayout)
       
        self.sourceList.setFixedHeight(200)
        self.shotListLayout = QHBoxLayout()
        

        mainLayout.addLayout(self.shotListLayout)
        mainLayout.addLayout(actionBarLayout)
        
        #set mainlayout for window
        self.setLayout(mainLayout)
        
        
        #setup widgets
        self.emergencyBtn.setFixedHeight(64)
        self.nextBtn.setFixedHeight(64)
        self.goLiveBtn.setFixedHeight(64)
        # fill lists for preview
        
        #self.shotlist.addItem(ShotlistItem(self.shotlist))
        #shotlist.addItem()
        
        # setup Window details
        self.setWindowTitle("TV Tally")
        self.resize(1024,600)
        
        
        self.addShotDiag = AddShotDialog(self)
        self.connectSignals()
        
        
    def populateShotlist(self, shotList):
        #qDebug("TESTSHOTLISTUPDATE") # thanks to this guy: http://stackoverflow.com/a/13103617, last-checked 19.01.2015
        for i in reversed(range(self.shotListLayout.count())):
            widget = self.shotListLayout.itemAt(i).widget()
            self.shotListLayout.removeWidget(widget)
            widget.setParent(None)
            
        #here all widgets will be added to the shotlist
        iteratr = 0
        for item in shotList:
            newItem = ShotlistItem(item[0], item[1], iteratr, self)
            self.shotListLayout.addWidget(newItem)
            print("WIDTH OF ITEM: " + str(newItem.width()))
            self.shotListLayout.setSpacing(0)
            self.shotListLayout.setAlignment(newItem, QtCore.Qt.AlignLeft)
            if  iteratr == len(shotList)-1:
                newItem.moveToBackBtn.setDisabled(True)
            newItem.addShotAtPos.connect(self.showAddShotDialog)
            newItem.delShotAtPos.connect(self.delShotAtPos)
            newItem.movShotDown.connect(self.movShotDown)
            newItem.movShotUp.connect(self.movShotUp)
            iteratr += 1
            
    def connectSignals(self):
        self.addShotDiag.okBtn.clicked.connect(self.addShotConfirmed)
        
    def showAddShotDialog(self, pos):
        print("ADD SHOT PRESSED FOR SHOT NR " + str(pos) )
        self.addShotDiag.storePos(pos)
        self.addShotDiag.show()
        
        
    def updateSourceList(self, sources):
        self.sourceList.clear()
        self.addShotDiag.setupCamselector(sources)
        for source in sources:
            self.sourceList.addItem(source[0] + ":" + source[1])
        
    def movDown(self, listPos):
        self.movShotDown.emit(self.listPos)
    
    def movUp(self, listPos):
        self.movShotUp.emit(self.listPos)
        
    def addShotConfirmed(self):
        pos = self.addShotDiag.getShotPos()
        shot = self.addShotDiag.getShot()
        if shot != False:
            self.addShotAtPos.emit(shot, pos)
        self.addShotDiag.close()
        
    def delShot(self,listPos):
        self.delShotAtPos.emit(self.listPos)
            
         
    # def fullscreenToggle(self):
        # if self.isFullScreen():
            # self.showNormal()
            # btn.setText("NOT FullScreen")
        # else:
            # self.showFullScreen()
            # self.btn.setText("FULLSCREEN")        