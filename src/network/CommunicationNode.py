'''
Created on 06.01.2015

@author: Florian
'''
from PyQt4.QtCore import QObject, qDebug, QMutex, QByteArray, QDataStream,\
    QIODevice, QTimer, pyqtSignal, QMutexLocker
from PyQt4.QtNetwork import QTcpSocket, QHostAddress, QAbstractSocket
from network.Message import TallyMessage

class CommunicationNode(QObject):
    '''
    classdocs
    '''

    #signals
    dataReceived = pyqtSignal(object)

    #default address vars
    _id = "default"
    ip = ""
    port = 0
    socket = None
    mutex = None
    #keepAliveTimer = None
    nodeFinished = pyqtSignal(object)
    error = pyqtSignal(int)
    #closingIntent = False
    
    def __init__(self, ip, port, parent=None):
        super(CommunicationNode, self).__init__(parent)
        self.ip = ip
        self.port = port
        self.socket = QTcpSocket(self)
        self.socket.setSocketOption(QAbstractSocket.KeepAliveOption,1)
        self.socket.disconnected.connect(self.disconnectHandler)
        self.socket.readyRead.connect(self.receiveData)
        self.nodeFinished.connect(self.deleteLater)
        self.mutex = QMutex()
#         self.keepAliveTimer = QTimer(self)
#         self.keepAliveTimer.timeout.connect(self.keepAlive)

    def disconnectHandler(self):
        if self.openConnection():
            print("Nodes::Reconnected with server - continuing operation")
        else:
            qDebug("Nodes::Reconnect failed - assuming dead end - goodbye")
            #self.nodeFinished.emit(self)
            
    #  connect to remote host and catch as many exceptions as possible
    def openConnection(self, tmout=4000):
        timeout = tmout
        try:
            self.socket.connectToHost(self.ip,self.port)
        
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
        
        if self.socket.waitForConnected(timeout):
            qDebug("Nodes::SUCCESS: Connection Established")
            #self.keepAliveTimer.start(timeout-1000)
            return True
        else:
            qDebug("Nodes::FAIL: Connection could not be established")
            self.socket.close()
            self.socket.deleteLater()
            self.nodeFinished.emit(self)
            return False
    
    # default request sending method inherited by all classes in node
    def sendRequest(self, request):
#         qDebug("Waiting for mutex to unlock")
#         locker = QMutexLocker(self.mutex)
        qDebug("Preparing  Data for sending")
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
        
        qDebug("Writing Stuff to socket")
        self.socket.write(block) # write stuff to socket
        qDebug("Request: " + str(request)+ " written to Socket")
        
        if not self.socket.waitForBytesWritten(timeout):
            qDebug("ERROR - Bytes could not be written")
            self.error.emit(self.socket.error(), self.socket.errorString())
            return
        
        return 
    
    def receiveData(self):
        #locker = QMutexLocker(self.mutex)
        qDebug(str(self.socket.bytesAvailable()) + " Bytes of Data available on Socket " + str(self.socket.socketDescriptor()))
        
        while self.socket.bytesAvailable() > 0:
            if self.socket.bytesAvailable() < 2:
                qDebug("EventConnectionHandler::Waiting for 2 bytes of data")
                return
    
            inpStream = QDataStream(self.socket) #create inputStream from socketConnection
            inpStream.setVersion(QDataStream.Qt_4_0)
            blockSize = inpStream.readUInt16() # read first two bytes where message size is stored
                
            while self.socket.bytesAvailable() < blockSize:
                if not self.networkSocket.waitForReadyRead():
                    self.error.emit(self.socket.error(), self.socket.errorString())
                    return
           
            #read data from socket inputstream
            data = inpStream.readString()
            #qDebug("DATA IS " + str(data) )
            
            try:
                data = str(data, "UTF-8")
            except TypeError:
                # Python v2.
                pass    
            except UnicodeError:
                qDebug("EventConnectionHandler::Socket(" + str(self.socket.socketDescriptor()) + ") UNICODE ERROR - Could not decode message, please resend")
                
            self.dataReceived.emit(TallyMessage(self.socket.socketDescriptor(), "", data)) #emit converted data
           # qDebug(str(self.socket.bytesAvailable()) + " Bytes remaining on socket")
        return
       
    def keepAlive(self):
        self.sendRequest("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.") 
        
    def closeConnection(self):
        #self.keepAliveTimer.stop()
        self.socket.close()
        #self.socket.waitForDisconnected()
        
        
#     def __del__(self):
# #         if self.keepAliveTimer != None:
# #             self.keepAliveTimer.stop()
#         #self.closeConnection()
#         self.nodeFinished.emit(self)
#         qDebug("Nodes::CommunicationNode deleted")
        
