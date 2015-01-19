'''
Created on 09.01.2015

@author: Florian
'''
from PyQt4.Qt import QDialog, qDebug
from PyQt4.QtGui import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout,\
    QButtonGroup
from gui.VideoWidget import VideoWidget
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
        self.titleLbl = QLabel("Auswaehlen der Video-Quelle")
        self.processDescLbl = QLabel("Bitte klicken sie auf die unten gelisteten Quellen, bis das Signal ihrer Kamera im Monitor links erscheint. Bestaetigen Sie dann mit OK")
        self.srcLbl = QLabel("Quellen:")
        self.okBtn = QPushButton("OK")
        self.cancelBtn = QPushButton("Cancel")
        self.sourceListView = QWidget()
        self.videoFeedView = VideoWidget()
        self.sourceBtnGrp = QButtonGroup() 
        self.sourceBtnGrp.setExclusive(True)
        
        
        #init layouts
        mainLayout = QVBoxLayout()
        feedViewLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        
        # setting up layouts
        feedViewLayout.addWidget(self.videoFeedView)
        feedViewLayout.addWidget(self.processDescLbl)
        buttonLayout.addWidget(self.okBtn)
        buttonLayout.addWidget(self.cancelBtn)
        mainLayout.addWidget(self.titleLbl)
        mainLayout.addLayout(feedViewLayout)
        mainLayout.addWidget(self.srcLbl)
        mainLayout.addWidget(self.sourceListView)
        mainLayout.addLayout(buttonLayout)
        
        #apply layout to main Widget
        self.setLayout(mainLayout)
        
        #connect signals
        self.connectSignals()
                
        #setup widgets
        self.processDescLbl.setWordWrap(True)
        self.sourceListView.setFixedHeight(100)
        
        #setup dialog details
        self.setWindowTitle("Select Source")
        #self.showMaximized()
        #self.showFullScreen()
        
    # connect the signals to their respective slots
    def connectSignals(self):
        self.sourceBtnGrp.buttonClicked.connect(self.resolveIdToSource)
        self.okBtn.clicked.connect(self.close) #TODO: link this button to server-action
        self.cancelBtn.clicked.connect(self.close)
        pass
        
    # add sources received from server to dialog for config
    def addSourcesToDialog(self, sources):
        self.sourceList = sources
        sourceLayout = QHBoxLayout()
        for source in sources:
            qDebug("ADDING SOURCE: " +str(source) + " TO THE ASSIGN DIALOG")
            sourceBtn = QPushButton(source)
            sourceBtn.setCheckable(True)
            self.sourceBtnGrp.addButton(sourceBtn)
            sourceLayout.addWidget(sourceBtn)
        self.sourceListView.setLayout(sourceLayout)
            
    # resolve the button id returned from our buttongroup to a sourceid stored in sourcelist
    def resolveIdToSource(self, id):
        qDebug("ASSIGNDIALOG::BUTTON" + self.sourceList[(self.sourceBtnGrp.checkedId()+2)*-1])
        qDebug("EMITTING SOURCE SELECTED SIGNAL")
        self.videoSourceSelected.emit(self.sourceList[(self.sourceBtnGrp.checkedId()+2)*-1]) #map the negative id to a positive list index
        