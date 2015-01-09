'''
Created on 04.01.2015

@author: Florian
'''
from PyQt4.QtNetwork import QTcpServer, QHostAddress
from PyQt4.QtGui import QApplication
from ConnectionHandler import ConnectionHandlerThread
from os.path import sys
from PyQt4.QtCore import qDebug, pyqtSignal, QSettings
from RequestHandler import RequestHandler
from nodes import TallyServer
from src.gui.MainWindow import MainWindow
from src.gui.SettingsDialog import SettingsDialog
import socket
from src.gui import SignalAssignDialog

threadList = list()
clientList = list()
shotList = list()
serverInterface = None
CLIENT_PORT = 3713

def initHandling():
    connHndl = ConnectionHandlerThread(server.nextPendingConnection())
    connHndl.finished.connect(connHndl.deleteLater)
    connHndl.dataReceived.connect(rqstHandler.processData)
    connHndl.start()
    threadList.append(connHndl)
    
def connectSignals():
#     rqstHandler.configStart.connect()
#     rqstHandler.configEnd.connect()
    rqstHandler.tallyRequest.connect(setTallyState)
#     rqstHandler.streamAnswer.connect()
#     rqstHandler.newClientlist.connect()
#     rqstHandler.newShotlist.connect()
    configWindow.okBtn.clicked.connect(createServerInterface)
    pass

def setTallyState(self, state):
    qDebug("CLIENT::CHANGING TALLY STATE")
    pass

def createServerInterface():
    ip = socket.gethostbyname(socket.gethostname())
    srv_ip = settings.value("server/ip")
    port = settings.value("server/port", type=int)
    serverInterface = TallyServer(srv_ip, port)
    serverInterface.registerClient("", settings.value("client/type"), (ip,CLIENT_PORT))
    
def printData(data):
    qDebug(data)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = QSettings("TallyClient.ini", QSettings.IniFormat)
    configWindow = SettingsDialog(settings)
    sigAssignWindow = SignalAssignDialog()
    window = MainWindow()
    rqstHandler = RequestHandler()
    
    connectSignals()
    window.show()
    
    #check if serverWasFound anywhere, if not show config
    if serverInterface == None:
        configWindow.show()
    
    

    #start tcp server and listen for requests
    server = QTcpServer()
    server.newConnection.connect(initHandling)
    server.listen(QHostAddress.Any, CLIENT_PORT)
    
    app.exec()