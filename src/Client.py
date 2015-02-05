'''
Created on 04.01.2015

@author: Florian
'''
from PyQt4.QtNetwork import QTcpServer, QHostAddress
from PyQt4.QtGui import QApplication
from ConnectionHandler import ConnectionHandler
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
from ThreadingServer import ThreadingServer

# TODO: replace with datawrangler class to profit from qtsignals
# threadList = list()
clientList = list()
shotList = list()
serverInterface = Container()
CLIENT_IP = "192.168.178."
CLIENT_PORT = 3713
streamUrl = Container()

# def initHandling():
#     connHndl = ConnectionHandler(server.nextPendingConnection(),server)
#     connHndl.finished.connect(connHndl.deleteLater)
#     connHndl.dataReceived.connect(rqstHandler.processData)
#     connHndl.setParent(app)
#     connHndl.start()
#     threadList.append(connHndl)
    
# def storeSourceList(source):
#     qDebug("CLIENT::Adding Sources to Assign Dialog")
#     sigAssignWindow.addSourcesToDialog(source)

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

# def confirmSelectedSource():
#     srvInt=serverInterface.load()
#     srvInt.configurationDone()
    
def storeStreamUrl(url):
    qDebug("CLIENT::Storing streamurl in assign window")
    streamUrl.store(url)
    sigAssignWindow.videoFeedView.setToolTip(streamUrl.load())

def connectSignals():
    server.dataReceived.connect(rqstHandler.processData)
    rqstHandler.configStart.connect(startConfigMode)
    rqstHandler.newSourcelist.connect(sigAssignWindow.addSourcesToDialog)
    rqstHandler.streamAnswer.connect(storeStreamUrl)
    rqstHandler.configEnd.connect(endConfigMode)
    rqstHandler.changeYourTally.connect(tallyLight.setState)
    rqstHandler.changeYourTally.connect(window.tallyState.changeStatus)
    rqstHandler.newClientlist.connect(window.updateSourceList)
    rqstHandler.newShotlist.connect(window.populateShotlist) 
    configWindow.okBtn.clicked.connect(createServerInterface)
    
    
    
def mvShotDwnInServer(shotPos):
    serverInterface.load().movShot(shotPos,shotPos+1)
    
def mvShotUpInServer(shotPos):
    serverInterface.load().movShot(shotPos, shotPos-1)

def addShotInServer(shot,pos):
    serverInterface.load().addShot(shot[0],shot[1],pos)

# def setTallyState(self, tid, state):
#     qDebug("CLIENT::CHANGING TALLY STATE")
#     if window != None:
#         window.tallyState.changeStatus(state)
#     else:
#         qDebug("MainWindow not initialized ERROR")
#     if tallyLight != None:
#         tallyLight.setState(tid, state)

# def setConfSrcLive(src):
#     if not serverInterface.isEmpty():
#         serverInterface.load().setVideoSrcToStatus(src)
#     else:
#         qDebug("CLIENT::ERROR - SERVER INTERFACE NOT INITIALIZED")

def createServerInterface():
    srv_ip = settings.value("server/ip")
    port = settings.value("server/port", type=int)
    qDebug("ServerIP from Config:" + srv_ip)
    qDebug("ServerPort from config: " + str(port))
    tempSrvInterface = TallyServer(srv_ip, port, app)
    tempSrvInterface.openConnection()
    tempSrvInterface.registerClient("", settings.value("client/type"), (CLIENT_IP,CLIENT_PORT))
    serverInterface.store(tempSrvInterface)
    
    #connect ServerInterface Signals
    window.addShotAtPos.connect(addShotInServer)
    window.delShotAtPos.connect(serverInterface.load().delShot)
    window.movShotDown.connect(mvShotDwnInServer)
    window.movShotUp.connect(mvShotUpInServer)
    window.nextBtn.clicked.connect(serverInterface.load().moveToNextShot)
    window.goLiveBtn.clicked.connect(goLive)
    sigAssignWindow.videoSourceSelected.connect(serverInterface.load().setVideoSrcToStatus)
    sigAssignWindow.okBtn.clicked.connect(serverInterface.load().configurationDone)
    
def goLive():
    myID = settings.value("client/id", None , str)
    if myID != None:
        serverInterface.load().setVideoSrcToStatus(myID, "LIVE")
    else:
        print("SHIT MY ID IS EMPTY")
    
# def printData(data):
#     qDebug(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = QSettings("TallyClient.ini", QSettings.IniFormat, app)
    tallyLight = TallyHandler(app)
    window = MainWindow()
    sigAssignWindow = SignalAssignDialog(window)
    configWindow = SettingsDialog(settings, window)
    rqstHandler = RequestHandler(app)
    server = ThreadingServer(app)
    connectSignals()
    window.show()

    #check if serverWasFound anywhere, if not show config
    if serverInterface.isEmpty:
        configWindow.show()
    
    server.startListening(CLIENT_PORT)
    
    app.exec_()