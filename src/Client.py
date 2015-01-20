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
from gui.MainWindow import MainWindow
from gui.SettingsDialog import SettingsDialog
import socket
from gui.SignalAssignDialog import SignalAssignDialog
from storage import Container
from time import sleep
from TallyHandler import TallyHandler
from gui.AddShotDialog import AddShotDialog


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
    rqstHandler.newShotlist.connect(window.populateShotlist) 
    configWindow.okBtn.clicked.connect(createServerInterface)
    sigAssignWindow.videoSourceSelected.connect(setConfSrcLive)
    sigAssignWindow.okBtn.clicked.connect(confirmSelectedSource)
    
    
def mvShotDwnInServer(shotPos):
    serverInterface.load().movShot(shotPos,shotPos+1)
    
def mvShotUpInServer(shotPos):
    serverInterface.load().movShot(shotPos, shotPos-1)
    
# def updateShotlist(shotlist):
#     shotList = shotlist
#     window.populateShotlist(shotlist)

def addShotInServer(shot,pos):
    serverInterface.load().addShot(shot[0],shot[1],pos)

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
    qDebug("ServerIP from Config:" + srv_ip)
    qDebug("ServerPort from config: " + str(port))
    tempSrvInterface = TallyServer(srv_ip, port)
    tempSrvInterface.openConnection()
    tempSrvInterface.registerClient("", settings.value("client/type"), (ip,CLIENT_PORT))
    serverInterface.store(tempSrvInterface)
    
    #connect ServerInterface Signals
    window.addShotAtPos.connect(addShotInServer)
    window.delShotAtPos.connect(serverInterface.load().delShot)
    window.movShotDown.connect(mvShotDwnInServer)
    window.movShotUp.connect(mvShotUpInServer)
    window.nextBtn.clicked.connect(serverInterface.load().moveToNextShot)
    window.goLiveBtn.clicked.connect(goLive)
    
def goLive():
    myID = settings.value("client/id", None , str)
    if myID != None:
        serverInterface.load().setVideoSrcToStatus(myID, "LIVE")
    else:
        print("SHIT MY ID IS EMPTY")
    
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
    server = QTcpServer()
    server.newConnection.connect(initHandling)
    server.listen(QHostAddress.Any, CLIENT_PORT)
    
    app.exec()