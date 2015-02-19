'''
Created on 06.01.2015

@author: Florian
'''
from PyQt4.QtCore import QObject, qDebug, QMutex, QByteArray, QDataStream,\
    QIODevice, QTimer, pyqtSignal, QMutexLocker
from PyQt4.QtNetwork import QTcpSocket, QHostAddress, QAbstractSocket
import json
from network.CommunicationNode import CommunicationNode
from network.Message import TallyMessage
        
class TallyClient(QObject):
    
    _id = "DEFAULT_CLIENT"
    c_type = "camera"
    source = None
    status = "OFF"
    
    nodeFinished = pyqtSignal(object)
    sendRequest = pyqtSignal(object)
    #init class and superclass
    def __init__(self, ip_address, socketId, parent=None):
        super(TallyClient, self).__init__(parent)
        self.ip = ip_address
        self.port = socketId
        
    #network requests here
    def startConfigurationMode(self):
        request = "CONFIG_STARTED"
        self.sendRequest.emit(TallyMessage("",self.port,request))
        
    def storeSourceList(self, sourceList): #TODO: implement request handling for this 
        sourceString = json.dumps(sourceList)
        request = "STORE_SOURCELIST:" + sourceString
        self.sendRequest.emit(TallyMessage("",self.port,request))
    
    def endConfigurationMode(self, clientId):
        request = "CONFIG_DONE:" + clientId
        self.sendRequest.emit(TallyMessage("",self.port,request))
            
    def setTally(self, status):
        request = "SET_TALLY:" + str(self._id) + ":" + str(status)
        self.status = status
        self.sendRequest.emit(TallyMessage("",self.port,request))
    
    def updateClientList(self, clientList):
        sublist = list()
        for client in clientList:
            sublist.append((client._id, client.status))
        request = "UPDATE_CLIENTLIST:"
        request += json.dumps(sublist)
        self.sendRequest.emit(TallyMessage("",self.port,request))
        
    def updateShotList(self, shotList):
        request = "UPDATE_SHOTLIST:"
        request += json.dumps(shotList)
        self.sendRequest.emit(TallyMessage("",self.port,request))
        
    def setStreamUrl(self, url="NOURL"):
        request = "SET_STREAM_URL:" + url
        self.sendRequest.emit(TallyMessage("",self.port,request))
        
    def enableControlledMode(self):
        request = "SET_CONTROLLED_MODE"
        self.sendRequest.emit(TallyMessage("",self.port,request))
        
    #say goodbye to server
    def goodbye(self):
        request = "DEREGISTER:" + self._id
        self.sendRequest.emit(TallyMessage("",self.port,request))
        
class TallyServer(CommunicationNode):
    
    stream_Url = "localhost"
    
    def __init__(self, ip_address, port, parent=None):
        super(TallyServer, self).__init__(ip_address, port, parent)
        
    #Network Handling code here
    def registerClient(self, clientID, clientType, clientAddress):
        request = "REGISTER:" + str(clientID) + ":" + str(clientType) + ":" + str(clientAddress[0]) + ":" + str(clientAddress[1])
        self.sendRequest(request)
    
    def deregisterClient(self, clientID=None):
        if clientID == None:
            clientID = self._id
        request = "DEREGISTER:" + str(clientID)
        self.sendRequest(request)
    
    def configurationReady(self):
        request = "CONFIG_STARTED"
        self.sendRequest(request)
    
    def configurationDone(self):
        request = "CONFIG_DONE"
        self.sendRequest(request)
    
    # orders the server to set a specific video src to a certain status(client orders)
    def setVideoSrcToStatus(self, clientId, status="LIVE"):
        request = "SET_SOURCE:" + clientId + ":" + status
        qDebug("REQUEST READY FOR SENDING:" + request)
        self.sendRequest(request)
    
    # order the server to set a specific tally client to a certain status(videoMixer orders)
    def setTallyToStatus(self, sourceId, status):
        request = "SET_TALLY:" + sourceId + ":" + status
        self.sendRequest(request)
    
    def addShot(self, source, image, pos):
        shotString = json.dumps((source,image))
        request = "ADD_SHOT:" + shotString + ":" + str(pos)
        self.sendRequest(request)
    
    def delShot(self, pos):
        request = "DEL_SHOT:" + str(pos)
        self.sendRequest(request)
    
    def movShot(self, fRom, to):
        request = "MOVE_SHOT:" + str(fRom) + ":" + str(to)
        self.sendRequest(request)
    
    def getStreamUrl(self, clientId):
        request = "GET_STREAM_URL:" + clientId
        self.sendRequest(request)
    
    def setStreamUrl(self, url):
        request = "SET_STREAM_URL:" + url
        self.sendRequest(request)
    
    def updateSourceList(self, sourcelist):
        sourceString = json.dumps(sourcelist)
        request = "UPDATE_SOURCELIST:" + sourceString
        self.sendRequest(request)
        
    def moveToNextShot(self):
        request = "NEXT_SHOT"
        self.sendRequest(request)
    
class TallySwitcher(QObject):
    
    c_type = "videoMixer"
    sendRequest = pyqtSignal(object)
    nodeFinished = pyqtSignal(object)
    
    def __init__(self, ip_address, socketID, parent=None):
        super(TallySwitcher, self).__init__(parent)
        self.ip = ip_address
        self.port = socketID
     
    def setSourceToStatus(self, sourceId, status):
        request = "SET_SOURCE:" + sourceId + ":" + status
        self.sendRequest.emit(TallyMessage("",self.port,request))
    
    def getStreamUrl(self):
        request = "GET_STREAM_URL:N U L L" 
        self.sendRequest.emit(TallyMessage("",self.port,request))
    
    def getSourceList(self):
        request = "GET_SOURCELIST"
        self.sendRequest.emit(TallyMessage("",self.port,request))