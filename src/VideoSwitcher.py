'''
Created on 04.01.2015

@author: Florian
'''
from PyQt4.QtNetwork import QTcpServer, QHostAddress
from PyQt4.QtGui import QApplication
from ConnectionHandler import ConnectionHandlerThread
from os.path import sys
from PyQt4.QtCore import qDebug
from RequestHandler import RequestHandler
from nodes import TallyServer
from PyQt4.Qt import QByteArray
from applescript import AppleScript
import socket



threadList = list()
sourceList = list()
serverInterface = None
streamUrl = "rtsp://media-us-2.soundreach.net/slcn_sports.sdp"
sourceListScript = AppleScript("appleScript/getListOfSources.scpt")
setStatusScript = AppleScript("appScript/setShotStatus.scpt")

def initHandling():
    connHndl = ConnectionHandlerThread(server.nextPendingConnection())
    connHndl.finished.connect(connHndl.deleteLater)
    connHndl.dataReceived.connect(rqstHandler.processData)
    connHndl.start()
    threadList.append(connHndl)
    
def connectSignals():
    rqstHandler.stateRequest.connect(setSourceState)
    rqstHandler.streamRequest.connect(returnStreamUrl)
    rqstHandler.sourceListRequest.connect(returnSourceList)

def setSourceState(source, state):
    if setToState(source, state): # TODO: Implement setting sources with wirecast here
        serverInterface.setTallyToStatus(source,state)

def returnStreamUrl():
    serverInterface.setStreamUrl(streamUrl) #TODO: implement wirecast streamurl grabber here
    
def returnSourceList():
    sourceList = getSourcesFromWirecast()
    serverInterface.updateSourceList(sourceList)

def printData(data):
    qDebug(data)
    
def setToState(source, state):
    qDebug("SWITCHING " + str(source) + " TO STATE " + str(state))
    try:
        setStatusScript.call("setStatus", source, state)
        
    except ScriptError:
        qDebug("An error occured: ScriptError")
        return False
    return True
    
def getSourcesFromWirecast():
    try:
        sources = sourceListScript.run()
        return sources
    except ScriptError:
        qDebug("Grabbing SourcesList returned an error: ScriptError")
        return False
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    rqstHandler = RequestHandler()
    connectSignals()
    getSourcesFromWirecast()
    qDebug("VIDEOSWITCHER::HELLO - REGISTERING WITH SERVER")
    serverInterface = TallyServer(socket.gethostbyname(socket.gethostname()), 3771 )
    serverInterface.openConnection()
    serverInterface.registerClient("", "videoMixer", ("127.0.0.1", 3117))
    
    server = QTcpServer()
    server.newConnection.connect(initHandling)
    server.listen(QHostAddress.Any, 3117)
    
    app.exec()