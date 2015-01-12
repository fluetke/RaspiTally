'''
Created on 04.01.2015

@author: Florian
'''
from PyQt4.QtNetwork import QTcpServer, QHostAddress
from PyQt4.QtGui import QApplication
from ConnectionHandler import ConnectionHandlerThread
from os.path import sys
from PyQt4.QtCore import qDebug, pyqtSignal, QSettings, QTimer
from RequestHandler import RequestHandler
from nodes import TallyServer
from src.gui.MainWindow import MainWindow
from src.gui.SettingsDialog import SettingsDialog
import socket
from src.gui.SignalAssignDialog import SignalAssignDialog
from storage import Container
from time import sleep
from src.TallyHandler import TallyHandler


threadList = list()
clientList = list()
shotList = list()
serverInterface = Container()
CLIENT_PORT = 3713
streamUrl = Container()

def initHandling():
    connHndl = ConnectionHandlerThread(server.nextPendingConnection())
    connHndl.finished.connect(connHndl.deleteLater)
    connHndl.dataReceived.connect(rqstHandler.processData)
    connHndl.start()
    threadList.append(connHndl)
    
def storeSourceList(source):
    qDebug("CLIENT::Adding Sources to Assign Dialog")
    sigAssignWindow.addSourcesToDialog(source)

def startConfigMode():
    sigAssignWindow.show()
    if not serverInterface.isEmpty() and not serverInterface.isList():
        tempInterface = serverInterface.load()
        tempInterface.configurationReady()

def endConfigMode(newId):
    settings.beginGroup("client")
    settings.setValue("id", str(newId))
    settings.endGroup()
    settings.sync()
    window.setWindowTitle("TV Tally: " + newId)

def confirmSelectedSource():
    serverInterface.load().configurationDone()
    
def storeStreamUrl(url):
    qDebug("CLIENT::Storing streamurl in assign window")
    streamUrl.store(url)
    sigAssignWindow.videoFeedView.setToolTip(streamUrl.load())

def connectSignals():
    rqstHandler.configStart.connect(startConfigMode)
    rqstHandler.newSourcelist.connect(storeSourceList)
    rqstHandler.streamAnswer.connect(storeStreamUrl)
    rqstHandler.configEnd.connect(endConfigMode)
    rqstHandler.tallyRequest.connect(setTallyState)
#     rqstHandler.streamAnswer.connect()
    rqstHandler.newClientlist.connect(window.updateSourceList)
#     rqstHandler.newShotlist.connect() #TODO: implement handling of shotlist updates
    configWindow.okBtn.clicked.connect(createServerInterface)
    sigAssignWindow.videoSourceSelected.connect(setConfSrcLive)
    sigAssignWindow.okBtn.clicked.connect(confirmSelectedSource)
    pass

def setTallyState(self, state):
    qDebug("CLIENT::CHANGING TALLY STATE")
    if window != None:
        window.tallyState.changeStatus(state)
    else:
        qDebug("MainWindow not initialized ERROR")
    if tallyLight != None:
        tallyLight.setState(state)

def setConfSrcLive(src):
    if not serverInterface.isEmpty():
        serverInterface.load().setVideoSrcToStatus(src)
    else:
        qDebug("CLIENT::ERROR - SERVER INTERFACE NOT INITIALIZED")

def createServerInterface():
    ip = socket.gethostbyname(socket.gethostname())
    srv_ip = settings.value("server/ip")
    port = settings.value("server/port", type=int)
    tempSrvInterface = TallyServer(srv_ip, port)
    tempSrvInterface.openConnection()
    tempSrvInterface.registerClient("", settings.value("client/type"), (ip,CLIENT_PORT))
    serverInterface.store(tempSrvInterface)
    
def printData(data):
    qDebug(data)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = QSettings("TallyClient.ini", QSettings.IniFormat)
    tallyLight = TallyHandler()
    configWindow = SettingsDialog(settings)
    sigAssignWindow = SignalAssignDialog()
    window = MainWindow()
    rqstHandler = RequestHandler()
    
    connectSignals()
    window.show()

    #check if serverWasFound anywhere, if not show config
    if serverInterface.isEmpty:
        configWindow.show()
    
    #start tcp server and listen for requests
    #server = QTcpServer()
    #server.newConnection.connect(initHandling)
    #server.listen(QHostAddress.Any, CLIENT_PORT)
    
    app.exec()