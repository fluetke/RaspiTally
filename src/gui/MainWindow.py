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
        tallyState = StatusBarWidget()
        liveMonitor = QWidget()
        sourceList = QListWidget()
        quitBtn = QPushButton("&Quit")
        
        # interaction area
        shotlist = QListWidget()
        emergencyBtn = QPushButton("&EMERGENCY")
        goLiveBtn = QPushButton("GO &LIVE")
        nextBtn = QPushButton("&NEXT")
        
        #layout definition
        mainLayout = QVBoxLayout()
        statusLayout = QHBoxLayout()
        previewLayout = QHBoxLayout()
        actionBarLayout = QHBoxLayout()
        
        # fill layouts 
        statusLayout.addWidget(tallyState)
        statusLayout.addWidget(quitBtn)
        previewLayout.addWidget(liveMonitor)
        previewLayout.addWidget(sourceList)
        actionBarLayout.addWidget(emergencyBtn)
        actionBarLayout.addWidget(goLiveBtn)
        actionBarLayout.addWidget(nextBtn)
        
        mainLayout.addLayout(statusLayout)
        mainLayout.addLayout(previewLayout)
        mainLayout.addWidget(shotlist)
        mainLayout.addLayout(actionBarLayout)
        
        #set mainlayout for window
        self.setLayout(mainLayout)
        
        # fill lists for preview
        sourceList.addItem("CAM 1")
        sourceList.addItem("CAM 2")
        sourceList.addItem("CAM 3")
        shotitem = ShotlistItem()
        shotlist.addItem("TEST")
        #shotlist.addItem()
        
        # setup Window details
        self.setWindowTitle("TV Tally")
        self.resize(1024,600)
        
    # def fullscreenToggle(self):
        # if self.isFullScreen():
            # self.showNormal()
            # btn.setText("NOT FullScreen")
        # else:
            # self.showFullScreen()
            # self.btn.setText("FULLSCREEN")        