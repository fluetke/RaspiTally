'''
Created on 04.01.2015

@author: Florian
'''
from PyQt4.QtCore import pyqtSignal, QThread, QByteArray, QDataStream, QIODevice,\
    qDebug, QMutex
from PyQt4.QtNetwork import QTcpSocket, QNetworkAddressEntry

class ConnectionHandlerThread(QThread):
    '''
    classdocs
    '''
    finished = pyqtSignal()
    error = pyqtSignal(QTcpSocket.SocketError)
    dataReceived = pyqtSignal(object)
    
    
    def __init__(self, connDesc, parent=None):
        '''
        Constructor
        '''
        super(ConnectionHandlerThread, self).__init__(parent)
        self.networkSocket = connDesc
        self.networkMutex = QMutex()
        
        
        
    def run(self):
        '''
        This handles incoming connections, one at a time 
        in this case, it collects incoming data and pipes 
        it to the datahandler class for further processing 
        '''
        qDebug("CONNECTION_HANDLER:: NEW CONNECTION")
        
        # receive data and pack into data_received for further processing
        self.networkSocket.waitForReadyRead(1000)
        self.networkMutex.lock()
        data_size = self.networkSocket.bytesAvailable()
        qDebug(str(data_size))
        data_received = self.networkSocket.readAll()
        self.networkMutex.unlock()
        if len(data_received) < data_size:
            qDebug("ERROR_ DATA RECEIVED TOO SHORT")
        qDebug(data_received)
        qDebug("CONNECTION_HANDLER:: EMITTING SIGNAL DATA_RECEIVED")
        #print(data_received)
        #print(data_received.data())
        data_received_str = data_received.data().decode('UTF-8') # convert data to string for further processing
        #print(data_received_str)
        qDebug("DATA IS::" + data_received_str)
        self.dataReceived.emit(data_received_str) #emit converted data
        #qDebug(networkSocket.peerAddress().toString() + ":" + str(networkSocket.peerPort()))
        #FIXME: Warnings/Errors about thread safety when writing to the socket here 
        #networkSocket.write("OK..."+ data_received)
        #networkSocket.waitForBytesWritten(msecs=100)
            
        self.networkSocket.disconnectFromHost()
        self.networkSocket.waitForDisconnected()
        qDebug("CONNECTION_HANDLER:: EMITTING SIGNAL FINISHED")
        self.finished.emit()
        
         
        