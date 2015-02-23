'''
Created on 04.01.2015

@author: Florian
'''
# system libraries
import socket
from os.path import sys
#framework libraries
from PyQt4.QtGui import QApplication

# project libraries
from RequestHandler import RequestHandler
from network.nodes import TallyServer
from Wirecast import WirecastConnector
from PyQt4.Qt import qDebug


#Globals
SERVER_IP = "127.0.0.1"
SERVER_PORT = 3771
streamUrl = "rtsp://192.168.178.29/tallytest.sdp"

# connect signals to slots
def connectSignals():
    #check prerequisites
    if serverInterface != None and wirecast != None and rqstHandler != None:
        serverInterface.dataReceived.connect(rqstHandler.processData)
        rqstHandler.streamRequest.connect(lambda: serverInterface.setStreamUrl(streamUrl))
        wirecast.sourcesReady.connect(serverInterface.updateSourceList)
        wirecast.sourceSet.connect(serverInterface.setTallyToStatus)
        rqstHandler.stateRequest.connect(wirecast.setSource)
        rqstHandler.sourceListRequest.connect(wirecast.getSources)
    else:
        qDebug("VideoSwitcher::Signal connection prerequisites not met - one or more vars are None")
    

# # return streamurl to server 
# def returnStreamUrl():
#     serverInterface.setStreamUrl(streamUrl) 
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    #init vars
    rqstHandler = RequestHandler()
    serverInterface = TallyServer( SERVER_IP , SERVER_PORT, app )
    wirecast = WirecastConnector(app)
#     server = ThreadingServer(app)
    
    #connect signals and slots
    connectSignals()
    
    #open connection to server
    serverInterface.openConnection()
    
    #register with server
    serverInterface.registerClient("", "videoMixer", (socket.gethostbyname(socket.gethostname()), 3117)) # works on mac, doesnt work on linux
    
    #start listening for commands
#     server.startListening(SWITCHER_PORT)
    
    #run the app
    sys.exit(app.exec_())