'''
Created on 06.01.2015

@author: Florian
'''
from PyQt4.QtCore import QObject, qDebug, QByteArray, QDataStream,\
    QIODevice, pyqtSignal
from PyQt4.QtNetwork import QTcpSocket, QAbstractSocket
from network.Message import TallyMessage

class CommunicationNode(QObject):
    '''
    Communication Interface between client and a tallyserver
    '''

    #signals
    dataReceived = pyqtSignal(object)
    nodeFinished = pyqtSignal(object)
    error = pyqtSignal(int)
    
    #default address vars
    _id = "default"
    ip = ""
    port = 0
    socket = None

    
    def __init__(self, ip, port, parent=None):
        ''' 
        initialize CommunicationNode with server ip and port as well as parent object
        '''
        super(CommunicationNode, self).__init__(parent)
        
        self.ip = ip
        self.port = port
        self.socket = QTcpSocket(self)
        self.socket.setSocketOption(QAbstractSocket.KeepAliveOption,1) #enable keepalive on socket
        
        #connect signals
        self.socket.disconnected.connect(self.disconnectHandler)
        self.socket.readyRead.connect(self.receiveData)
        self.nodeFinished.connect(self.deleteLater)


    def disconnectHandler(self):
        '''
        try to reconnect to server in case of disconnect
        '''
        if self.openConnection():
            qDebug("CommunicationNode::Reconnected with server - continuing operation")
        else:
            qDebug("CommunicationNode::Reconnect failed - assuming dead end - goodbye")
            self.nodeFinished.emit(self)
            
            
    def openConnection(self, tmout=4000):
        '''
        open connection to remote host, abort after tmout milliseconds
        catch as many exceptions as possible during connection attempt
        '''
        timeout = tmout
        try:
            self.socket.connectToHost(self.ip,self.port)
            
        except QTcpSocket.HostNotFoundError:
            qDebug("CommunicationNode::Remote Host " + str(self.ip) + ":" + str(self.port) + " not found")
        except QTcpSocket.ConnectionRefusedError:
            qDebug("CommunicationNode::Connection refused by Host")
        except QTcpSocket.NetworkError:
            qDebug("CommunicationNode::Connection closed: Network error")
        except QTcpSocket.RemoteHostClosedError:
            qDebug("CommunicationNode::Connection closed by remote Host")
        except QTcpSocket.SocketAccessError:
            qDebug("CommunicationNode::Error could not AccessSocket -> Socket Access Error")
        except QTcpSocket.SocketAddressNotAvailableError:
            qDebug("CommunicationNode::ERROR: Socket Address Not Available")
        except QTcpSocket.SocketTimeoutError:
            qDebug("CommunicationNode::ERROR: Socket Timed out")
        except QTcpSocket.UnfinishedSocketOperationError:
            qDebug("CommunicationNode::Error blocked by unfinished socket operation")
        
        if self.socket.waitForConnected(timeout):
            qDebug("CommunicationNode::SUCCESS: Connection Established")
            return True
        
        else:
            qDebug("CommunicationNode::FAIL: Connection could not be established")
            self.socket.close()
            self.socket.deleteLater()
            self.nodeFinished.emit(self)
            return False
    
    
    def sendRequest(self, request):
        '''
        send data to server, return False in case of error 
        '''
        qDebug("CommunicationNode::Preparing  Data for sending")
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
        
        qDebug("CommunicationNode::Writing Stuff to socket")
        self.socket.write(block) # write stuff to socket
        qDebug("CommunicationNode::Request: " + str(request)+ " written to Socket")
        
        if not self.socket.waitForBytesWritten(timeout):
            qDebug("CommunicationNode::ERROR - Bytes could not be written")
            self.error.emit(self.socket.error(), self.socket.errorString())
            return False
        
        return True
    
    
    def receiveData(self):
        '''
        receive data from server, repeat until no more bytes are available
        '''
        
        qDebug("CommunicationNode::" + str(self.socket.bytesAvailable()) + " Bytes of Data available on Socket " + str(self.socket.socketDescriptor()))
        
        while self.socket.bytesAvailable() > 0:
            if self.socket.bytesAvailable() < 2:
                qDebug("CommunicationNode::Waiting for 2 bytes of data")
                return False
    
            inpStream = QDataStream(self.socket) #create inputStream from socketConnection
            inpStream.setVersion(QDataStream.Qt_4_0)
            blockSize = inpStream.readUInt16() # read first two bytes where message size is stored
                
            while self.socket.bytesAvailable() < blockSize:
                if not self.networkSocket.waitForReadyRead():
                    self.error.emit(self.socket.error(), self.socket.errorString())
                    return
           
            #read data from socket inputstream
            data = inpStream.readString()
                        
            try:
                data = str(data, "UTF-8")
            except TypeError:
                # Python v2.
                pass    
            except UnicodeError:
                qDebug("EventConnectionHandler::Socket(" + str(self.socket.socketDescriptor()) + ") UNICODE ERROR - Could not decode message, please resend")
                
            self.dataReceived.emit(TallyMessage(self.socket.socketDescriptor(), "", data)) #emit converted data
#             qDebug(str(self.socket.bytesAvailable()) + " Bytes remaining on socket")
        return True
       
        
    def closeConnection(self):
        '''
        close the connection to the server 
        '''
        self.socket.close()