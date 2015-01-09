'''
Created on 04.01.2015

@author: Florian
'''
from PyQt4.QtCore import pyqtSignal, QThread, QByteArray, QDataStream, QIODevice,\
    qDebug
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
        self.connectionDescriptor = connDesc
        
        
        
    def run(self):
        '''
        This handles incoming connections, one at a time 
        in this case, it collects incoming data and pipes 
        it to the datahandler class for further processing 
        '''
        qDebug("CONNECTION_HANDLER:: NEW CONNECTION")
        #networkSocket = QTcpSocket() #TODO: remove if unused
        
        # throw error if socket connection fails
#         if not networkSocket.setSocketDescriptor(self.connectionDescriptor):
#             self.error.emit(networkSocket.error())
#             return
    
        # receive data and pack into data_received for further processing
        networkSocket = self.connectionDescriptor
        networkSocket.waitForReadyRead(1000)
        data_size = networkSocket.bytesAvailable()
        qDebug(str(data_size))
        data_received = networkSocket.readAll()
        
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
            
        networkSocket.disconnectFromHost()
        #networkSocket.waitForDisconnected()
        qDebug("CONNECTION_HANDLER:: EMITTING SIGNAL FINISHED")
        self.finished.emit()
        
         
        