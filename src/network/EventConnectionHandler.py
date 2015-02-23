'''
Created on 19.02.2015

@author: Florian
'''
from PyQt4.QtCore import QObject, qDebug, QDataStream, QIODevice, pyqtSignal,\
    QByteArray
from PyQt4.QtNetwork import QTcpSocket, QAbstractSocket
from network.Message import TallyMessage

class EventConnectionHandler(QObject):
    '''
    This is an event based version of the connectionHandler class
    '''

    dataReceived = pyqtSignal(object)


    def __init__(self, socket, parent = None):
        '''
        Constructor
        '''
        super(EventConnectionHandler, self).__init__(parent)
        self.socket = QTcpSocket()
        self.socket = socket
        self.socket.setSocketOption(QAbstractSocket.KeepAliveOption,1)
        self.socket.readyRead.connect(self.receiveData)
        
        
    def receiveData(self):
        qDebug(str(self.socket.bytesAvailable()) + " Bytes of Data available on Socket " + str(self.socket.socketDescriptor()))
        
        if self.socket.bytesAvailable() < 2:
            qDebug("EventConnectionHandler::Waiting for 2 bytes of data")
            return

        inpStream = QDataStream(self.socket) #create inputStream from socketConnection
        inpStream.setVersion(QDataStream.Qt_4_0)
        blockSize = inpStream.readUInt16() # read first two bytes where message size is stored
            
        while self.socket.bytesAvailable() < blockSize:
            if not self.socket.waitForReadyRead():
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
            
        self.dataReceived.emit(TallyMessage(self.socket.socketDescriptor(), None, data)) #emit converted data
        
        
    def sendData(self, data):
        qDebug("sending request to peer")
        block = QByteArray()
        outStream = QDataStream(block, QIODevice.WriteOnly)
        outStream.setVersion(QDataStream.Qt_4_0)
        outStream.writeUInt16(0)
     
        try:
            # Python v3.
            request = bytes(data, encoding='UTF-8')
        except:
            # Python v2.
            pass
     
        outStream.writeString(request)
        outStream.device().seek(0)
        outStream.writeUInt16(block.size() - 2)
             
        self.socket.write(block) # send data to client
        
        if not self.socket.waitForBytesWritten(1000):
            qDebug("Error while sending reqeuest")
            self.error.emit(self.socket.error(), self.socket.errorString())
            return


    def handleRequest(self, msg):
        if msg.recv != self.socket.socketDescriptor():
            return
        
        if msg.payload != "":
            self.sendData(msg.payload)
            