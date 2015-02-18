'''
Created on 09.01.2015

@author: Florian
'''
from PyQt4.Qt import QDialog, qDebug
from PyQt4.QtGui import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout,\
    QButtonGroup, QFont
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
        self.guiFont = QFont("Arial", 18)
        
        # init widgets
        self.titleLbl = QLabel("Auswaehlen der Video-Quelle")
        self.processDescLbl = QLabel("Bitte klicken sie auf die unten gelisteten Quellen, bis das Signal ihrer Kamera im Monitor links erscheint. Bestaetigen Sie dann mit OK")
        self.processDescLbl.setFont(self.guiFont)
        self.srcLbl = QLabel("Quellen:")
        self.srcLbl.setFont(self.guiFont)
        self.okBtn = QPushButton("OK")
        self.okBtn.setFont(self.guiFont)
        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.setFont(self.guiFont)
        self.sourceListView = QWidget()
        self.videoFeedView = VideoWidget()
        self.sourceBtnGrp = QButtonGroup() 
        self.sourceBtnGrp.setExclusive(True)
        
        
        #init layouts
        self.mainLayout = QVBoxLayout()
        self.feedViewLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        
        # setting up layouts
        self.feedViewLayout.addWidget(self.videoFeedView)
        self.feedViewLayout.addWidget(self.processDescLbl)
        self.buttonLayout.addWidget(self.okBtn)
        self.buttonLayout.addWidget(self.cancelBtn)
        self.mainLayout.addWidget(self.titleLbl)
        self.mainLayout.addLayout(self.feedViewLayout)
        self.mainLayout.addWidget(self.srcLbl)
        self.mainLayout.addWidget(self.sourceListView)
        self.mainLayout.addLayout(self.buttonLayout)
        
        #apply layout to main Widget
        self.setLayout(self.mainLayout)
        
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
            sourceBtn.setFont(self.guiFont)
            sourceBtn.setCheckable(True)
            self.sourceBtnGrp.addButton(sourceBtn)
            sourceLayout.addWidget(sourceBtn)
        self.sourceListView.setLayout(sourceLayout)
            
    # resolve the button id returned from our buttongroup to a sourceid stored in sourcelist
    def resolveIdToSource(self, id):
        qDebug("ASSIGNDIALOG::BUTTON" + self.sourceList[(self.sourceBtnGrp.checkedId()+2)*-1])
        qDebug("EMITTING SOURCE SELECTED SIGNAL")
        self.videoSourceSelected.emit(self.sourceList[(self.sourceBtnGrp.checkedId()+2)*-1]) #map the negative id to a positive list index
        