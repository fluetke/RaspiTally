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
from src.applescript import asrun, asquote



threadList = list()
sourceList = list()
serverInterface = None
streamUrl = "rtsp://media-us-2.soundreach.net/slcn_sports.sdp"
sourceListScript = '''property currentDoc : "None"
property sources : list
property tempSources : list
property tempSource : list

tell application "Wirecast5"
    set sources to {}
    set currentDoc to last document
    set currentLayer to the layer named "Master Layer 1" of currentDoc
    set tempSources to every shot of currentLayer
    repeat with source in tempSources
        set tempSource to {}
        copy id of source as text to the end of tempSource
        copy name of source as text to the end of tempSource
        if live of source then
            copy "live" to the end of tempSource
        else if preview of source then
            copy "preview" to the end of tempSource
        else
            copy "off" to the end of tempSource
        end if
        copy tempSource to the end of sources
    end repeat
    return sources
end tell
'''

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
    qDebug("SWITCHING " + str(source) + " TO STATE " + str(state))
    return True
    
  
def getSourcesFromWirecast():
    appleScriptReturn = asrun(asquote())
    print(str(appleScriptReturn))
    return str(appleScriptReturn)

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