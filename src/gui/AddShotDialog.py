'''
Created on 11.01.2015

@author: Florian
'''
from PyQt4.Qt import QDialog
from PyQt4.QtGui import QPushButton, QPixmap, QVBoxLayout, QHBoxLayout, QLabel,\
    QButtonGroup, QTabWidget
from PyQt4.QtCore import pyqtSignal
from gui.addShotPageOneWidget import PageOneWidget
from gui.addShotPageTwoWidget import PageTwoWidget

class AddShotDialog(QDialog):
    '''
    This dialog takes care of the selection of shots to be added to the shotlist
    '''
    
    newShotAtPos = pyqtSignal(tuple,int)
    shotPos=0
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(AddShotDialog, self).__init__(parent)
        self.shotTypes = ["ESTABLISHER", "MASTER", "WIDE", "TWOSHOT", "OVERTHESHOULDER", "MEDIUM", "CLOSEUP", "XTRM_CLOSEUP"]
        self.cameras = list()
        self.pageOne = PageOneWidget(self)
        self.pageTwo = PageTwoWidget(self)
        
        self.pageOne.populateShotTypes(self.shotTypes)
        self.okBtn = QPushButton("OK")
        self.cancelBtn = QPushButton("Cancel")
        
        tabPane = QTabWidget()
        tabPane.addTab(self.pageOne, "Shottypes")
        tabPane.addTab(self.pageTwo, "Videoinputs")
        
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.okBtn)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.cancelBtn)
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(tabPane)
        self.mainLayout.addLayout(self.buttonLayout)
        
        self.setLayout(self.mainLayout)
        self.connectSignals()
        
    def connectSignals(self):
        self.okBtn.clicked.connect(self.onOkClicked)
        self.cancelBtn.clicked.connect(self.hide)
        
    def onOkClicked(self):
        shot = self.getShot()
        self.newShotAtPos.emit(shot, self.shotPos)
        self.hide()
        
    def showWithPos(self,pos):
        self.shotPos = pos
        self.show()
        
    def setupCamselector(self, camlist):
        self.pageTwo.populateCameras(camlist)
        self.cameras = camlist
    
    def getShot(self):
        print("SELECTED SHOT TYPE: " + str(self.pageTwo.checkableButtonGroup.checkedId()) )
        shotType = self.shotTypes[(self.pageOne.checkableButtonGroup.checkedId()+2)*-1]
        listIndex = (self.pageTwo.checkableButtonGroup.checkedId()+2)*-1
        print(listIndex)
        if listIndex < len(self.cameras):
            shotCam = self.cameras[listIndex][0]
            print("ShotType: " + shotType + " ShotCam: " + shotCam)
            return (shotCam, shotType)
        else:
            print("FEHLER IM SYTEM: DIE KAMERA EXISTIERT NICHT/LIST INDEX OUT OF BOUNDS")
            return False
        