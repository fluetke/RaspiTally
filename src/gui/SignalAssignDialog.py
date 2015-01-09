'''
Created on 09.01.2015

@author: Florian
'''
from PyQt4.Qt import QDialog
from PyQt4.QtGui import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from src.gui.VideoWidget import VideoWidget
from PyQt4.QtCore import pyqtSignal

class SignalAssignDialog(QDialog):
    '''
    classdocs
    '''
    
    videoSourceSelected = pyqtSignal(object)

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(SignalAssignDialog, self).__init__(parent)
                
        # init widgets
        self.titleLbl = QLabel("Server-Informationen")
        self.processDescLbl = QLabel("Bitte klicken sie auf die unten gelisteten Quellen, bis das Signal ihrer Kamera im Monitor links erscheint. Bestätigen Sie dann mit OK")
        self.srcLbl = QLabel("Quellen:")
        self.okBtn = QPushButton("OK")
        self.cancelBtn = QPushButton("Cancel")
        self.sourceListView = QWidget()
        self.videoFeedView = VideoWidget()
        
        
        #init layouts
        mainLayout = QVBoxLayout()
        feedViewLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        
        # setting up layouts
        formLayout.addRow(self.srvIpLbl, self.srvIpInput)
        formLayout.addRow(self.srvPortLbl, self.srvPortInput)
        formLayout.addRow(self.cliTypeLbl, self.cliTypeInput)
        buttonLayout.addWidget(self.okBtn)
        buttonLayout.addWidget(self.cancelBtn)
        mainLayout.addWidget(self.titleLbl)
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(buttonLayout)
        
        #apply layout to main Widget
        self.setLayout(mainLayout)
        
        #connect signals
        self.connectSignals()
                
        #setup widgets
        self.cliTypeInput.addItem("camera")
        self.cliTypeInput.addItem("director")
        self.srvPortInput.setRange(1,65535)
        self.loadSettings()
        

        #setup dialog details
        self.setWindowTitle("Settings")
        self.showMaximized()
        #self.showFullScreen()