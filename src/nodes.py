'''
Created on 06.01.2015

@author: Florian
'''
from PyQt4.QtCore import QObject, qDebug, QMutex
from PyQt4.QtNetwork import QTcpSocket, QHostAddress
import json

class TallyNode(QObject):
    '''
    classdocs
    '''

    #default address vars
    id = "default"
    ip = ""
    port = 0
    nodeConnection = None
    mutex = None
    
    def __init__(self, ip, port, parent=None):
        super(TallyNode, self).__init__(parent)
        self.ip = ip
        self.port = port
        self.nodeConnection = QTcpSocket()
        self.nodeConnection.disconnected.connect(self.nodeConnection.deleteLater)
        self.mutex = QMutex()
        
    #  connect to remote host and catch as many exceptions as possible
    def openConnection(self):
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
        finally:
            qDebug("ERROR::" + self.nodeConnection.errorString())
            
        if self.nodeConnection.waitForConnected():
            qDebug("SUCCESS: Connection Established")
            return True
    
    # default request sending method inherited by all classes in node
    def sendRequest(self, byteRequest):
        try: 
            self.mutex.lock()
            self.nodeConnection.write(byteRequest)
            self.nodeConnection.waitForBytesWritten()
            self.mutex.unlock()
        except QTcpSocket.DatagramTooLargeError:
            qDebug("ERROR: Datagramm is too large, try something smaller")
        except QTcpSocket.NetworkError:
            qDebug("ERROR: Network error during transfer")
        except QTcpSocket.RemoteHostClosedError:
            qDebug("ERROR: Remote host closed the connection")
            self.nodeConnection.disconnectFromHost()
            self.nodeConnection.close()
        except QTcpSocket.SocketTimeoutError:
            qDebug("ERROR: Connection timed out")
        except QTcpSocket.UnfinishedSocketOperationError:
            qDebug("ERROR: Socket Operation in progress, please wait and try again")
        finally:
            qDebug("NODE::REQUEST SEND TO " + str(self.ip) + ":" + str(self.port))
            
    def closeConnection(self):
        self.nodeConnection.disconnectFromHost()
        self.nodeConnection.waitForDisconnected()
        self.nodeConnection.close()
        
class TallyClient(TallyNode):
    
    c_type = "camera"
    source = None
    status = "OFF"
    
    #init class and superclass
    def __init__(self, ip_address, port):
        TallyNode.__init__(self, ip_address, port)
        self.ip = ip_address
        self.port = port
        
    #network requests here
    def startConfigurationMode(self):
        request = "CONFIG_STARTED"
        self.sendRequest(bytes(request,'UTF-8'))
        
    def storeSourceList(self, sourceList): #TODO: implement request handling for this 
        sourceString = json.dumps(sourceList)
        request = "STORE_SOURCELIST:" + sourceString
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def endConfigurationMode(self, clientId):
        request = "CONFIG_DONE:" + clientId
        self.sendRequest(bytes(request, 'UTF-8'))
            
    def setTally(self, status):
        request = "SET_TALLY:" + status
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def updateClientList(self, clientList):
        request = "UPDATE_CLIENTLIST:"
        clist = json.dumps(clientList)
        self.sendRequest(bytes(request, 'UTF-8')+clist)
        
    def updateShotList(self, shotList):
        request = "UPDATE_SHOTLIST:"
        slist = json.dumps(shotList)
        self.sendRequest(bytes(request, 'UTF-8')+slist)
        
    def setStreamUrl(self, url):
        request = "SET_STREAM_URL:" + url
        self.sendRequest(bytes(request, 'UTF-8'))
        
class TallyServer(TallyNode):
    
    stream_Url = "localhost"
    
    def __init__(self, ip_address, port):
        TallyNode.__init__(self, ip_address, port)
        
    #Network Handling code here
    def registerClient(self, clientID, clientType, clientAddress):
        request = "REGISTER:" + str(clientID) + ":" + str(clientType) + ":" + str(clientAddress[0]) + ":" + str(clientAddress[1])
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def deregisterClient(self, clientID):
        request = "DEREGISTER:" + str(clientID)
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def configurationReady(self):
        request = "CONFIG_STARTED"
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def configurationDone(self):
        request = "CONFIG_DONE"
        self.sendRequest(bytes(request, 'UTF-8'))
    
    # orders the server to set a specific video src to a certain status(client orders)
    def setVideoSrcToStatus(self, clientId, status="LIVE"):
        request = "SET_SOURCE:" + clientId + ":" + status
        self.sendRequest(bytes(request, 'UTF-8'))
    
    # order the server to set a specific tally client to a certain status(videoMixer orders)
    def setTallyToStatus(self, sourceId, status):
        request = "SET_TALLY:" + sourceId + ":" + status
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def addShot(self, source, image, pos):
        request = "ADD_SHOT:" +source + ":" + image + ":" + pos
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def delShot(self, pos):
        request = "DEL_SHOT:" + pos
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def movShot(self, fRom, to):
        request = "MOVE_SHOT:" + fRom + ":" + to
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def getStreamUrl(self, clientId):
        request = "GET_STREAM_URL:" + clientId
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def setStreamUrl(self, url):
        request = "SET_STREAM_URL:" + url
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def updateSourceList(self, sourcelist):
        sourceString = json.dumps(sourcelist)
        #print(sourceString)
        request = "UPDATE_SOURCELIST:" + sourceString
        self.sendRequest(bytes(request, 'UTF-8'))
    
class TallySwitcher(TallyNode):
    
    def __init__(self, ip_address, port):
        TallyNode.__init__(self, ip_address, port)
     
    def setSourceToStatus(self, sourceId, status):
        request = "SET_SOURCE:" + sourceId + ":" + status
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def getStreamUrl(self):
        request = "GET_STREAM_URL:N U L L" 
        self.sendRequest(bytes(request, 'UTF-8'))
    
    def getSourceList(self):
        request = "GET_SOURCELIST"
        self.sendRequest(bytes(request, 'UTF-8'))