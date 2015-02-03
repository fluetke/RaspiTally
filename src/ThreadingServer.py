'''
Created on 31.01.2015

@author: Florian
'''
from PyQt4.QtNetwork import QTcpServer, QHostAddress
from PyQt4.QtCore import qDebug, QThread, pyqtSignal, Qt
from PyQt4.Qt import qDebug
from DataWrangler import ListData
from ConnectionHandler_ import ConnectionHandler
from PyQt4 import QtCore

class ThreadingServer(QTcpServer):
    '''
    This is the threading TCP-server which will take care of all the communication requests by tally nodes
    '''
    
    threads = ListData()
    connections = ListData()
    dataReceived = pyqtSignal(str)

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        # initiate super class
        super(ThreadingServer, self).__init__(parent)
        
    def startListening(self, port):
        
        if not self.listen(QHostAddress.Any, port):
            qDebug("ThreadingServer::Error starting server")
        else:
            qDebug("ThreadingServer::Listening on port " + str(port))
            
    def incomingConnection(self, socketDescriptor):
        
        qDebug("ThreadingServer::Incoming connection on Socket " + str(socketDescriptor))
        
        #TODO: add thread stuff here
        thread = QThread(self)
        connectionHandler = ConnectionHandler(socketDescriptor)
        
        connectionHandler.moveToThread(thread)
        
        connectionHandler.error.connect(self.handleError)
        thread.started.connect(connectionHandler.handle, Qt.QueuedConnection)
        connectionHandler.finished.connect(thread.quit)
        connectionHandler.finished.connect(connectionHandler.deleteLater)
        connectionHandler.dataReceived.connect(self.dataReceived)
        thread.finished.connect(thread.deleteLater)
       # thread.started.connect(lambda: print("THREAD STARTED"))
        
        thread.start()
        
        # add created objects to lists for longterm storage
        self.threads.addItem(thread) #add thread to list of threads
        self.connections.addItem(connectionHandler) # add connection to list of connections
        
    def handleError(self, error, errormsg):
        qDebug("ThreadingServer:: Error " + str(error) + " - " + str(errormsg))