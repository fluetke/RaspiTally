'''
Created on 04.01.2015

@author: Florian
'''
# system libraries
import socket
from os.path import sys
#framework libraries
#from PyQt4.Qt import QByteArray
#from PyQt4.QtCore import qDebug
from PyQt4.QtNetwork import QTcpServer, QHostAddress
from PyQt4.QtGui import QApplication

# project libraries
from ConnectionHandler import ConnectionHandler
from RequestHandler import RequestHandler
from nodes import TallyServer
from Wirecast import WirecastConnector
from ThreadingServer import ThreadingServer


#Globals
SERVER_IP = "127.0.0.1"
SERVER_PORT = 3771
SWITCHER_PORT = 3117
streamUrl = "rtsp://192.168.178.29/tallytest.sdp"

# # start new thread for each new connection
# def initHandling():
#     connHndl = ConnectionHandler(server.nextPendingConnection())
#     connHndl.finished.connect(connHndl.deleteLater)
#     connHndl.dataReceived.connect(rqstHandler.processData)
#     connHndl.setParent(app)
#     connHndl.start()
#     threadList.append(connHndl)
    
# connect signals to slots
def connectSignals():
    server.dataReceived.connect(rqstHandler.processData)
    rqstHandler.streamRequest.connect(returnStreamUrl)
    rqstHandler.stateRequest.connect(wirecast.setSource)
    rqstHandler.sourceListRequest.connect(wirecast.getSources)
    wirecast.sourcesReady.connect(serverInterface.updateSourceList)
    wirecast.sourceSet.connect(serverInterface.setTallyToStatus)

# return streamurl to server 
def returnStreamUrl():
    serverInterface.setStreamUrl(streamUrl) 



if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    #init vars for 
    rqstHandler = RequestHandler()
    serverInterface = TallyServer( SERVER_IP , SERVER_PORT, app )
    serverInterface.openConnection()
    wirecast = WirecastConnector(app)
    threadList = list()
    server = ThreadingServer(app)
    
    #connect signals and slots
    connectSignals()
    
   # serverInterface.registerClient("", "videoMixer", (socket.gethostbyname(socket.gethostname()), 3117))
    serverInterface.registerClient("", "videoMixer", ("127.0.0.1", 3117))
    
#     server = QTcpServer(app)
#     server.newConnection.connect(initHandling)
#     server.listen(QHostAddress.Any, 3117)
    
    server.startListening(SWITCHER_PORT)
    
    sys.exit(app.exec_())