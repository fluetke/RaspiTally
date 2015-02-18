'''
Created on 08.01.2015

@author: Florian
'''
# qt framework imports
from PyQt4.QtCore import pyqtSignal, QSize
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,\
    QListWidget, QApplication, QFont, QIcon
from PyQt4 import QtCore

# own import
from gui.StatusBarWidget import StatusBarWidget
from gui.ShotlistItem import ShotlistItem
from gui.VideoWidget import VideoWidget
from gui.AddShotDialog import AddShotDialog
from PyQt4.Qt import QPixmap

class MainWindow(QWidget):
    '''
    classdocs
    '''
    
    # init signals   
    addShotAtPos = pyqtSignal(tuple, int)
    delShotAtPos = pyqtSignal(int)
    movShotUp = pyqtSignal(int)
    movShotDown = pyqtSignal(int)
    shutdown = pyqtSignal()
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.guiFont = QFont("Arial", 12)
        ##setup all Widgets
        # display area
        self.tallyState = StatusBarWidget(self)
        self.liveMonitor = VideoWidget(self)
        self.sourceList = QListWidget(self)
        self.quitIcon = QPixmap("gui/img/btn_close.png")
        self.quitBtn = QPushButton()
        self.quitBtn.setIcon(QIcon(self.quitIcon))
        self.quitBtn.setIconSize(QSize(32,32))
        self.quitBtn.setStyleSheet("background: #555")
        # interaction area
        #self.shotlist = QListWidget()
        self.emergencyBtn = QPushButton("&EMERGENCY")
        #self.emergencyBtn.setDisabled(True)
        self.goLiveBtn = QPushButton("GO &LIVE")
        self.nextBtn = QPushButton("&NEXT")
        self.addShotDiag = AddShotDialog(self)
        
        # init components
        self.tallyState.setFixedSize(384,64)
        self.quitBtn.setFixedSize(64,64)
        self.sourceList.setFixedHeight(200)
        self.sourceList.setFont(self.guiFont)
        self.emergencyBtn.setFixedSize(192,64)
        self.emergencyBtn.setFont(self.guiFont)
        self.emergencyBtn.setStyleSheet("background: #555")
        self.nextBtn.setFixedSize(192,64)
        self.nextBtn.setFont(self.guiFont)
        self.nextBtn.setStyleSheet("background: #555")
        self.goLiveBtn.setFixedSize(192,64)
        self.goLiveBtn.setFont(self.guiFont)
        self.goLiveBtn.setStyleSheet("background: #555")
        
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
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.actionBarLayout)
        
        #set mainlayout for window
        self.setLayout(self.mainLayout) 
        self.isControlledMode = False
        # setup Window details
        self.setWindowTitle("TV Tally")
        self.resize(1024,600)
        self.setStyleSheet("background: #333; color: #fff") # set interface to night mode
        self.connectSignals()
        
    def enableControlMode(self):
        self.goLiveBtn.setDisabled(True)
        self.nextBtn.setDisabled(True)
        self.isControlledMode=True
        
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
            if not self.isControlledMode:
                newItem.addShotAtPos.connect(self.addShotDiag.showWithPos)
                newItem.delShotAtPos.connect(self.delShotAtPos)
                newItem.movShotDown.connect(self.movShotDown)
                newItem.movShotUp.connect(self.movShotUp)
            iteratr += 1
            
    def connectSignals(self):
        self.quitBtn.clicked.connect(self.shutdown) #TODO add clean shutdown of server, and deregistering here
        self.addShotDiag.newShotAtPos.connect(self.addShotAtPos)
        self.emergencyBtn.clicked.connect(self.fullscreenToggle)
        
    def updateSourceList(self, sources):
        self.sourceList.clear()
        self.addShotDiag.setupCamselector(sources) # TODO: move this to signal connection
        for source in sources: #FIXME: fix setupCamSelector Method
            self.sourceList.addItem(source[0] + ":" + source[1])
        
    def updateTally(self,status):
        if status == "LIVE":
            self.goLiveBtn.setStyleSheet("background: #f00")
        if status == "PREVIEW":
            self.goLiveBtn.setStyleSheet("background: #0f0")
        if status == "OFF":
            self.goLiveBtn.setStyleSheet(None)
        self.tallyState.changeStatus(status)
        
    def fullscreenToggle(self):
        if self.isFullScreen():
            self.showNormal()
            #btn.setText("NOT FullScreen")
        else:
            self.showFullScreen()
            #self.btn.setText("FULLSCREEN")        
