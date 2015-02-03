'''
Created on 04.01.2015

@author: Florian
'''
from PyQt4.QtCore import pyqtSignal, QThread, QByteArray, QDataStream, QIODevice,\
    qDebug, QMutex
from PyQt4.QtNetwork import QTcpSocket, QNetworkAddressEntry


class ConnectionHandler(QThread):
    '''
    classdocs
    '''
    finished = pyqtSignal()
    error = pyqtSignal(int, str)
    dataReceived = pyqtSignal(object)
    
    
    def __init__(self, connDesc, parent=None):
        '''
        Constructor
        '''
        super(ConnectionHandler, self).__init__(parent)
        self.networkSocket = connDesc
        self.networkSocket.setParent(self)
        self.networkMutex = QMutex()
        self.quit = False
        self.networkSocket.disconnected.connect(self.handleDisconnect)
        
    def __del__(self):
        qDebug("ConnectionHandler::Destructor")
        qDebug("ConnectionHandler::NetworkSocket ConnectionState - " + str(self.networkSocket.connected))
        qDebug("ConnectionHandler::NetworkMutex Locked - " + str(self.networkMutex.locked()))
        qDebug("ConnectionHandler::Quit Flag - " + str(self.quit))
        self.networkMutex.lock()
        self.quit = True
        self.networkMutex.unlock()
        self.wait()
        
    def handleDisconnect(self):
        qDebug("ConnectionHandler::Connection lost, quitting")
        self.quit = True
        self.wait()
    
    def run(self):
        '''
        This handles incoming connections, one at a time 
        in this case, it collects incoming data and pipes 
        it to the datahandler class for further processing
        connection pattern mainly taken from QT-blockingfortuneclient 
        example and adjusted to fit the current project
        '''
        qDebug("CONNECTION_HANDLER:: NEW CONNECTION")
        timeout = 4000
        inpStream = QDataStream(self.networkSocket)
        inpStream.setVersion(QDataStream.Qt_4_0)
        # receive data and pack into data_received for further processing
        while not self.quit:
#
            #qDebug("WAITING TO RECEIVE DATA")
            # wait for the first 2 bytes to arrive
            while self.networkSocket.bytesAvailable() < 2:
                #qDebug("WAITING FOR READY READ")
                if not self.networkSocket.waitForReadyRead(): #TODO: implement keep alive method
                    self.error.emit(self.networkSocket.error(), self.networkSocket.errorString())
                    self.networkMutex.lock()
                    self.quit = True
                    self.networkMutex.unlock()
                    break
                    #return 
#                 
            inpStream = QDataStream(self.networkSocket) #create inputStream from socketConnection
            inpStream.setVersion(QDataStream.Qt_4_0)
            blockSize = inpStream.readUInt16() # read first two bytes where message size is stored
            #qDebug("BLOCKSIZE IS: " + str(blockSize))
            while self.networkSocket.bytesAvailable() < blockSize and not self.quit:
                #qDebug("WAITING FOR DATA TO ARRIVE")
                if not self.networkSocket.waitForReadyRead():
                    self.error.emit(self.networkSocket.error(), self.networkSocket.errorString())
                    self.networkSocket.close()
                    return
                
            #qDebug("LOCKING THE SOCKET FOR TRANSFER")
            self.networkMutex.lock()
            data = inpStream.readString()
            #qDebug("READING DATA")
            self.networkMutex.unlock()
            #qDebug("UNLOCKING THE SOCKET")
            
            try:
                data = str(data, "UTF-8")
                qDebug("DATA IS::" + data)
            
            except TypeError:
                # Python v2.
                pass    
            except UnicodeError:
                print("UNICODE ERROR: Could not decode message, please resend")
            
            #qDebug("CONNECTION_HANDLER:: EMITTING SIGNAL DATA_RECEIVED")
            self.dataReceived.emit(data) #emit converted data
            if data != None: 
                if data.startswith("DEREGISTER"):
                    self.networkMutex.lock()
                    self.quit = True
                    self.networkMutex.unlock()
        
        qDebug("DISCONNECTING")
        self.networkSocket.disconnectFromHost()
        self.networkSocket.waitForDisconnected()
        #qDebug("CONNECTION_HANDLER:: EMITTING SIGNAL FINISHED")
        self.finished.emit()
        
         
        