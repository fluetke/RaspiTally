'''
Created on 08.01.2015

@author: Florian
'''
# qt framework imports
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,\
    QListWidget, QApplication
from PyQt4 import QtCore

# own import
from gui.StatusBarWidget import StatusBarWidget
from gui.ShotlistItem import ShotlistItem
from gui.VideoWidget import VideoWidget
from gui.AddShotDialog import AddShotDialog

class MainWindow(QWidget):
    '''
    classdocs
    '''
    
    # init signals   
    addShotAtPos = pyqtSignal(tuple, int)
    delShotAtPos = pyqtSignal(int)
    movShotUp = pyqtSignal(int)
    movShotDown = pyqtSignal(int)
    
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        ##setup all Widgets
        # display area
        self.tallyState = StatusBarWidget(self)
        self.liveMonitor = VideoWidget(self)
        self.sourceList = QListWidget(self)
        self.quitBtn = QPushButton("&Quit")
        # interaction area
        #self.shotlist = QListWidget()
        self.emergencyBtn = QPushButton("&EMERGENCY")
        self.goLiveBtn = QPushButton("GO &LIVE")
        self.nextBtn = QPushButton("&NEXT")
        self.addShotDiag = AddShotDialog(self)
        
        # init components
        self.tallyState.setFixedSize(384,64)
        self.quitBtn.setFixedSize(64,64)
        self.sourceList.setFixedHeight(200)
        self.emergencyBtn.setFixedHeight(64)
        self.nextBtn.setFixedHeight(64)
        self.goLiveBtn.setFixedHeight(64)
        
        #layout definition
        self.mainLayout = QVBoxLayout()
        self.statusLayout = QHBoxLayout()
        self.previewLayout = QHBoxLayout()
        self.actionBarLayout = QHBoxLayout()
        self.shotListOuterLayout = QHBoxLayout()
        self.shotListLayout = QHBoxLayout()
        
        # fill layouts 
        self.statusLayout.addStretch(192)
        self.statusLayout.addWidget(self.tallyState)
        self.statusLayout.addStretch(128)
        self.statusLayout.addWidget(self.quitBtn)
        self.previewLayout.addWidget(self.liveMonitor)
        self.previewLayout.addWidget(self.sourceList)
        self.actionBarLayout.addStretch()
        self.actionBarLayout.addWidget(self.emergencyBtn)
        self.actionBarLayout.addWidget(self.goLiveBtn)
        self.actionBarLayout.addWidget(self.nextBtn)
        self.actionBarLayout.addStretch()
        self.shotListLayout.setSpacing(0)
        self.shotListOuterLayout.setSpacing(0)
        self.shotListOuterLayout.addLayout(self.shotListLayout)
        self.shotListOuterLayout.addStretch()
        self.mainLayout.addLayout(self.statusLayout)
        self.mainLayout.addLayout(self.previewLayout)
        self.mainLayout.addLayout(self.shotListOuterLayout)
        self.mainLayout.addLayout(self.actionBarLayout)
        
        #set mainlayout for window
        self.setLayout(self.mainLayout) 
        
        # setup Window details
        self.setWindowTitle("TV Tally")
        self.resize(1024,600)
        self.connectSignals()
        
    ''' clear and refill the shotlist'''
    def populateShotlist(self, shotList):
        # thanks to this guy: http://stackoverflow.com/a/13103617, last-checked 19.01.2015
        for i in reversed(range(self.shotListLayout.count())):
            widget = self.shotListLayout.itemAt(i).widget()
            self.shotListLayout.removeWidget(widget)
            widget.setParent(None)
            
        #here all widgets will be added to the shotlist
        iteratr = 0
        for item in shotList:
            newItem = ShotlistItem(item[0], item[1], iteratr, self)
            self.shotListLayout.addWidget(newItem)
            self.shotListLayout.setAlignment(newItem, QtCore.Qt.AlignLeft)
            if  iteratr == len(shotList)-1:
                newItem.moveToBackBtn.setDisabled(True)
            newItem.addShotAtPos.connect(self.addShotDiag.showWithPos)
            newItem.delShotAtPos.connect(self.delShotAtPos)
            newItem.movShotDown.connect(self.movShotDown)
            newItem.movShotUp.connect(self.movShotUp)
            iteratr += 1
            
    def connectSignals(self):
        self.quitBtn.clicked.connect(QApplication.quit) #TODO add clean shutdown of server, and deregistering here
        self.addShotDiag.newShotAtPos.connect(self.addShotAtPos)
        self.emergencyBtn.clicked.connect(self.fullscreenToggle)
        
    def updateSourceList(self, sources):
        self.sourceList.clear()
        self.addShotDiag.setupCamselector(sources) # TODO: move this to signal connection
        for source in sources: #FIXME: fix setupCamSelector Method
            self.sourceList.addItem(source[0] + ":" + source[1])
        
    def fullscreenToggle(self):
        if self.isFullScreen():
            self.showNormal()
            #btn.setText("NOT FullScreen")
        else:
            self.showFullScreen()
            #self.btn.setText("FULLSCREEN")        