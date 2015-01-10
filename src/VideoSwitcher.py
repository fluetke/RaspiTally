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
from wsgiref.simple_server import ServerHandler
from PyQt4.Qt import QByteArray

threadList = list()
sourceList = list()
serverInterface = None
streamUrl = "rtsp://media-us-2.soundreach.net/slcn_sports.sdp"

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
    serverInterface.updateSourceList(sourceList)

def printData(data):
    qDebug(data)
    
def setToState(source, state):
    pass
  
def getSourcesFromWirecast():
    testList = list() #list of sources for testing, no guarantee they will look like this coming from wirecast
    testList.append(("SOURCE1", "OFF"))
    testList.append(("SOURCE2", "LIVE"))
    testList.append(("SOURCE3", "PREVIEW"))
    
    for source in testList:
        sourceList.append((source[0], source[1]))
    return

def setToStateInWirecast(source, state):
    return True
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    rqstHandler = RequestHandler()
    connectSignals()
    getSourcesFromWirecast()
    qDebug("VIDEOSWITCHER::HELLO - REGISTERING WITH SERVER")
    serverInterface = TallyServer("127.0.0.1", 3771 )
    serverInterface.openConnection()
    serverInterface.registerClient("", "videoMixer", ("127.0.0.1", 3117))
    

    server = QTcpServer()
    server.newConnection.connect(initHandling)
    server.listen(QHostAddress.Any, 3117)
    
    app.exec()