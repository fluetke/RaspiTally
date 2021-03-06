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
from network.nodes import TallyServer
from gui.MainWindow import MainWindow
from gui.SettingsDialog import SettingsDialog
import socket
from gui.SignalAssignDialog import SignalAssignDialog
from storage import Container
from TallyHandler import TallyHandler
from gui.AddShotDialog import AddShotDialog
#from ThreadingServer import ThreadingServer

# TODO: replace with datawrangler class to profit from qtsignals
clientList = list()
shotList = list()
serverInterface = Container()
CLIENT_IP = "192.168.178.32"
CLIENT_PORT = 3713
streamUrl = Container()

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
    
def storeStreamUrl(url):
    qDebug("CLIENT::Storing streamurl in assign window")
    streamUrl.store(url)
    sigAssignWindow.videoFeedView.setToolTip(streamUrl.load())

def connectSignals():
    
    rqstHandler.configStart.connect(startConfigMode)
    rqstHandler.newSourcelist.connect(sigAssignWindow.addSourcesToDialog)
    rqstHandler.streamAnswer.connect(storeStreamUrl)
    rqstHandler.configEnd.connect(endConfigMode)
    rqstHandler.changeYourTally.connect(tallyLight.setState)
    rqstHandler.changeYourTally.connect(window.tallyState.changeStatus)
    rqstHandler.newClientlist.connect(window.updateSourceList)
    rqstHandler.newShotlist.connect(window.populateShotlist) 
    rqstHandler.controlModeEnabled.connect(window.enableControlMode)
    #rqstHandler.deregClient.connect(shutdownPart2) #shutdown server and close application
    configWindow.okBtn.clicked.connect(createServerInterface)
    window.shutdown.connect(shutdownClient)
    
    
def mvShotDwnInServer(shotPos):
    serverInterface.load().movShot(shotPos,shotPos+1)
    
def mvShotUpInServer(shotPos):
    serverInterface.load().movShot(shotPos, shotPos-1)

def addShotInServer(shot,pos):
    serverInterface.load().addShot(shot[0],shot[1],pos)

def createServerInterface():
    srv_ip = settings.value("server/ip")
    port = settings.value("server/port", type=int)
    qDebug("ServerIP from Config:" + srv_ip)
    qDebug("ServerPort from config: " + str(port))
    tempSrvInterface = TallyServer(srv_ip, port, app)
    tempSrvInterface.openConnection()
    tempSrvInterface.registerClient("", settings.value("client/type"), (settings.value("client/ip"),settings.value("client/port", type=int)))
    serverInterface.store(tempSrvInterface)
    serverInterface.load().dataReceived.connect(rqstHandler.processData)
    
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
    
def shutdownClient():
    #kill all remaining threads
#     server.quitting.emit()
#     server.close()
    if serverInterface != None:
        serverInterface.load().closeConnection()
    QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = QSettings("TallyClient.ini", QSettings.IniFormat, app)
    tallyLight = TallyHandler(app)
    window = MainWindow()
    sigAssignWindow = SignalAssignDialog(window)
    configWindow = SettingsDialog(settings, window)
    rqstHandler = RequestHandler(app)
    connectSignals()
    window.show()

    #check if serverWasFound anywhere, if not show config
    if serverInterface.isEmpty:
        configWindow.show()
    
    app.exec_()