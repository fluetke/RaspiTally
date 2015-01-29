'''
Created on 08.01.2015

@author: Florian
'''
from PyQt4.QtGui import QDialog, QLabel, QPushButton, QSpinBox, QComboBox,\
    QVBoxLayout, QFormLayout, QHBoxLayout
from PyQt4.QtCore import pyqtSignal, QSettings
from PyQt4.Qt import QLineEdit, qDebug

class SettingsDialog(QDialog):
    #list of needed fields 
    #server address(autodetect, if nothing found then manually)
    #client type(director/camera)
    #clientID random but editable for typing
    #2 buttons cancel ok
    # labels for server adress, client type and client id    
    
    def __init__(self, setting, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.settings = setting
                
        # init widgets
        self.titleLbl = QLabel("Server-Informationen")
        self.okBtn = QPushButton("OK")
        self.cancelBtn = QPushButton("Cancel")
        self.srvIpLbl = QLabel("Tally-Server IP")
        self.srvPortLbl = QLabel("Tally-Server Port")
        self.cliTypeLbl = QLabel("Client-Type")
        self.srvIpInput = QLineEdit()
        self.srvPortInput = QSpinBox()
        self.cliTypeInput = QComboBox()
        
        #init layouts
        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.buttonLayout = QHBoxLayout()
        
        # setting up layouts
        self.formLayout.addRow(self.srvIpLbl, self.srvIpInput)
        self.formLayout.addRow(self.srvPortLbl, self.srvPortInput)
        self.formLayout.addRow(self.cliTypeLbl, self.cliTypeInput)
        self.buttonLayout.addWidget(self.okBtn)
        self.buttonLayout.addWidget(self.cancelBtn)
        self.mainLayout.addWidget(self.titleLbl)
        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addLayout(self.buttonLayout)
        
        #apply layout to main Widget
        self.setLayout(self.mainLayout)
        
        #connect signals
        self.connectSignals()
                
        #setup widgets
        self.cliTypeInput.addItem("camera")
        self.cliTypeInput.addItem("director")
        self.srvPortInput.setRange(1,65535)
        self.loadSettings()
        

        #setup dialog details
        self.setWindowTitle("Settings")
        
    def connectSignals(self):
        self.okBtn.clicked.connect(self.storeSettings)
        self.cancelBtn.clicked.connect(self.hide)
        self.okBtn.clicked.connect(self.hide)
        
    def loadSettings(self):
        qDebug("SETTINGS_DIALOG::LOADING SETTINGS")
        self.srvIpInput.setText(self.settings.value("server/ip", "127.0.0.1", type=str))
        self.srvPortInput.setValue(self.settings.value("server/port", "7313", type=int))
        self.cliTypeInput.setCurrentIndex(self.cliTypeInput.findText(self.settings.value("client/type","camera", type=str)))
        
    def storeSettings(self):
        self.settings.beginGroup("server")
        self.settings.setValue("ip", self.srvIpInput.text())
        self.settings.setValue("port", self.srvPortInput.value())
        self.settings.endGroup()
        self.settings.beginGroup("client")
        self.settings.setValue("type", self.cliTypeInput.currentText())
        self.settings.endGroup()
        self.settings.sync()        
        qDebug("SETTINGS_DIALOG::SAVING SETTINGS")