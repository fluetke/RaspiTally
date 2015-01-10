'''
Created on 08.01.2015

@author: Florian
'''
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,\
    QListWidget
from src.gui.StatusBarWidget import StatusBarWidget
from src.gui.ShotlistItem import ShotlistItem

class MainWindow(QWidget):
    '''
    classdocs
    '''
        
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        ##setup all Widgets
        # display area
        self.tallyState = StatusBarWidget()
        self.liveMonitor = QWidget()
        self.sourceList = QListWidget()
        self.quitBtn = QPushButton("&Quit")
        
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
        statusLayout.addWidget(self.tallyState)
        statusLayout.addWidget(self.quitBtn)
        previewLayout.addWidget(self.liveMonitor)
        previewLayout.addWidget(self.sourceList)
        actionBarLayout.addWidget(self.emergencyBtn)
        actionBarLayout.addWidget(self.goLiveBtn)
        actionBarLayout.addWidget(self.nextBtn)
        
        mainLayout.addLayout(statusLayout)
        mainLayout.addLayout(previewLayout)
        mainLayout.addWidget(self.shotlist)
        mainLayout.addLayout(actionBarLayout)
        
        #set mainlayout for window
        self.setLayout(mainLayout)
        
        # fill lists for preview
        self.shotitem = ShotlistItem()
        self.shotlist.addItem("TEST")
        #shotlist.addItem()
        
        # setup Window details
        self.setWindowTitle("TV Tally")
        self.resize(1024,600)
        
    def updateSourceList(self, sources):
        for source in sources:
            self.sourceList.addItem(source[0] + ":" + source[1])
             
    # def fullscreenToggle(self):
        # if self.isFullScreen():
            # self.showNormal()
            # btn.setText("NOT FullScreen")
        # else:
            # self.showFullScreen()
            # self.btn.setText("FULLSCREEN")        