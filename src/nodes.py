'''
Created on 06.01.2015

@author: Florian
'''
from PyQt4.QtCore import QObject, qDebug, QMutex, QByteArray, QDataStream,\
    QIODevice, QTimer, pyqtSignal, QMutexLocker
from PyQt4.QtNetwork import QTcpSocket, QHostAddress, QAbstractSocket
import json

class TallyNode(QObject):
    '''
    classdocs
    '''

    #default address vars
    _id = "default"
    ip = ""
    port = 0
    nodeConnection = None
    mutex = None
    keepAliveTimer = None
    nodeFinished = pyqtSignal(object)
    
    def __init__(self, ip, port, parent=None):
        super(TallyNode, self).__init__(parent)
        self.ip = ip
        self.port = port
        self.nodeConnection = QTcpSocket(self)
        self.nodeConnection.disconnected.connect(self.disconnectHandler)
        self.mutex = QMutex()
        self.keepAliveTimer = QTimer(self)
        self.keepAliveTimer.timeout.connect(self.keepAlive)

    def disconnectHandler(self):
        self.keepAliveTimer.stop()
        if self.openConnection():
            print("Nodes::Reconnected with server - continuing operation")
            self.keepAlive()
            self.keepAliveTimer.start(3000)
        else:
            qDebug("Nodes::Reconnect failed - assuming dead end - goodbye")
            self.nodeFinished.emit(self)
            
    #  connect to remote host and catch as many exceptions as possible
    def openConnection(self, timeout=4000):
        locker = QMutexLocker(self.mutex)
        try:
            self.nodeConnection.connectToHost(self.ip,self.port)
        
        except QTcpSocket.HostNotFoundError:
            qDebug("Remote Host " + str(self.ip) + ":" + str(self.port) + " not found")
        except QTcpSocket.ConnectionRefusedError:
            qDebug("Connection refused by Host")
        except QTcpSocket.NetworkError:
            qDebug("Connection closed: Network error")
        except QTcpSocket.RemoteHostClosedError:
            qDebug("Connection closed by remote Host")
        except QTcpSocket.SocketAccessError:
            qDebug("Error could not AccessSocket -> Socket Access Error")
        except QTcpSocket.SocketAddressNotAvailableError:
            qDebug("ERROR: Socket Address Not Available")
        except QTcpSocket.SocketTimeoutError:
            qDebug("ERROR: Socket Timed out")
        except QTcpSocket.UnfinishedSocketOperationError:
            qDebug("Error blocked by unfinished socket operation")
        
        if self.nodeConnection.waitForConnected(timeout):
            qDebug("SUCCESS: Connection Established")
            self.keepAliveTimer.start(timeout-1000)
            return True
        else:
            qDebug("FAIL: Connection could not be established")
            self.nodeConnection.close()
            self.nodeConnection.deleteLater()
            self.nodeFinished.emit(self)
            return False
    
    # default request sending method inherited by all classes in node
    def sendRequest(self, request):
        locker = QMutexLocker(self.mutex)
        timeout = 4000
        
        block = QByteArray()
        out = QDataStream(block, QIODevice.WriteOnly)
        out.setVersion(QDataStream.Qt_4_0)
        out.writeUInt16(0)

        try:
            # Python v3.
            request = bytes(request, encoding='UTF-8')
        except:
            # Python v2.
            pass

        out.writeString(request)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)
        
        self.nodeConnection.write(block) # write stuff to socket
        
        if self.nodeConnection.state() == QAbstractSocket.ConnectedState:
            if self.nodeConnection.waitForBytesWritten(timeout):
                qDebug("Node::Request send to " + str(self.ip) + ":" + str(self.port))
        else:
            qDebug("Nodes::Remote host abruptly closed the connection")
        

           
    def keepAlive(self):
        self.sendRequest("KEEPALIVE") 
        
    def closeConnection(self):
        self.nodeConnection.close()
        self.nodeConnection.waitForDisconnected()
        
    def __del__(self):
        self.keepAliveTimer.stop()
        self.nodeFinished.emit(self)
        qDebug("Nodes::TallyNode deleted")
        
class TallyClient(TallyNode):
    
    _id = "DEFAULT_CLIENT"
    c_type = "camera"
    source = None
    status = "OFF"
    
    #init class and superclass
    def __init__(self, ip_address, port, parent=None):
        super(TallyClient, self).__init__(ip_address, port, parent)
        self.ip = ip_address
        self.port = port
        
    #network requests here
    def startConfigurationMode(self):
        request = "CONFIG_STARTED"
        self.sendRequest(request)
        
    def storeSourceList(self, sourceList): #TODO: implement request handling for this 
        sourceString = json.dumps(sourceList)
        request = "STORE_SOURCELIST:" + sourceString
        self.sendRequest(request)
    
    def endConfigurationMode(self, clientId):
        request = "CONFIG_DONE:" + clientId
        self.sendRequest(request)
            
    def setTally(self, status):
        request = "SET_TALLY:" + status
        self.status = status
        self.sendRequest(request)
    
    def updateClientList(self, clientList):
        sublist = list()
        for client in clientList:
            sublist.append((client._id, client.status))
        request = "UPDATE_CLIENTLIST:"
        request += json.dumps(sublist)
        self.sendRequest(request)
        
    def updateShotList(self, shotList):
        request = "UPDATE_SHOTLIST:"
        request += json.dumps(shotList)
        self.sendRequest(request)
        
    def setStreamUrl(self, url="NOURL"):
        request = "SET_STREAM_URL:" + url
        self.sendRequest(request)
        
class TallyServer(TallyNode):
    
    stream_Url = "localhost"
    
    def __init__(self, ip_address, port, parent=None):
        super(TallyServer, self).__init__(ip_address, port, parent)
        
    #Network Handling code here
    def registerClient(self, clientID, clientType, clientAddress):
        request = "REGISTER:" + str(clientID) + ":" + str(clientType) + ":" + str(clientAddress[0]) + ":" + str(clientAddress[1])
        self.sendRequest(request)
    
    def deregisterClient(self, clientID):
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
    
class TallySwitcher(TallyNode):
    
    c_type = "videoMixer"
    
    def __init__(self, ip_address, port, parent=None):
        super(TallySwitcher, self).__init__(ip_address, port, parent)
     
    def setSourceToStatus(self, sourceId, status):
        request = "SET_SOURCE:" + sourceId + ":" + status
        self.sendRequest(request)
    
    def getStreamUrl(self):
        request = "GET_STREAM_URL:N U L L" 
        self.sendRequest(request)
    
    def getSourceList(self):
        request = "GET_SOURCELIST"
        self.sendRequest(request)