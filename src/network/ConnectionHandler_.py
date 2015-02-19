'''
Created on 04.01.2015

@author: Florian
'''
from PyQt4.QtCore import pyqtSignal, QThread, QByteArray, QDataStream, QIODevice,\
    qDebug, QMutex, QObject, QMutexLocker
from PyQt4.QtNetwork import QTcpSocket, QNetworkAddressEntry


class ConnectionHandler(QObject):
    '''
    classdocs
    '''
    finished = pyqtSignal()
    error = pyqtSignal(int, str)
    dataReceived = pyqtSignal(str)
    
    def __init__(self, sockDesc, parent=None):
        '''
        Constructor
        '''
        super(ConnectionHandler, self).__init__(parent)
        qDebug("ConnectionHandler::Receiving socket descriptor " + str(sockDesc))
        self.socketDescriptor = sockDesc
        self.networkMutex = QMutex()
        self.quit = False
    
    def handle(self):
        '''
        This handles incoming connections, one at a time 
        in this case, it collects incoming data and pipes 
        it to the datahandler class for further processing
        connection pattern mainly taken from QT-blockingfortuneclient 
        example and adjusted to fit the current project
        '''
        
        qDebug("ConnectionHandler::Taking over connection on Socket " + str(self.socketDescriptor) + " for further processing")
        
        locker = QMutexLocker(self.networkMutex)
        
        networkSocket = QTcpSocket(self)
#         networkSocket.disconnected.connect(self.shutdownThread)
        
        if not networkSocket.setSocketDescriptor(self.socketDescriptor):
            self.error.emit(networkSocket.error(), networkSocket.errorString())
            self.quit = True
        
        timeout = 10000
        
        # receive data and pack into data_received for further processing
        while not self.quit:
#            
            # wait for the first 2 bytes to arrive
            while networkSocket.bytesAvailable() < 2:
                if not networkSocket.waitForReadyRead(timeout):
                    print("ConnectionHandler::Packetsize not received - quitting")
                    self.error.emit(networkSocket.error(), networkSocket.errorString())
                    self.quit = True
                    break 

            inpStream = QDataStream(networkSocket) #create inputStream from socketConnection
            inpStream.setVersion(QDataStream.Qt_4_0)
            blockSize = inpStream.readUInt16() # read first two bytes where message size is stored
            
            while networkSocket.bytesAvailable() < blockSize and not self.quit:
                if not self.networkSocket.waitForReadyRead(timeout):
                    print("ConnectionHandler::Packet Payload not received - quitting")
                    self.error.emit(networkSocket.error(), networkSocket.errorString())
                    self.quit = True  
                
            #read data from socket inputstream
            data = inpStream.readString()
            
            try:
                data = str(data, "UTF-8")
                qDebug("ConnectionHandler::Received Data from Socket " + str(self.socketDescriptor) + ": " + data)
            
            except TypeError:
                # Python v2.
                pass    
            except UnicodeError:
                qDebug("ConnectionHandler::UNICODE ERROR - Could not decode message, please resend")
            
            self.dataReceived.emit(data) #emit converted data
        
        networkSocket.disconnectFromHost()
        if not networkSocket.waitForDisconnected(timeout):
            self.error.emit(networkSocket.error(), networkSocket.errorString())
            networkSocket.abort()
        else:
            networkSocket.close()
        
        self.finished.emit()
        
    
        
    # set quit flag to true to stop connection handler
    def closeConnection(self):
        self.quit = True
        
        

        
        