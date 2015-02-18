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
from nodes import TallyServer
#from Wirecast import WirecastConnector
from ThreadingServer import ThreadingServer
from PyQt4.Qt import qDebug
from asyncio.tasks import sleep

#Globals
SERVER_IP = "127.0.0.1"
SERVER_PORT = 3771
SWITCHER_IP = "127.0.0.1"
SWITCHER_PORT = 3117
streamUrl = "rtsp://192.168.178.29/tallytest.sdp"

# connect signals to slots
def connectSignals():
    #check prerequisites
    if server != None and serverInterface != None and rqstHandler != None:
        server.dataReceived.connect(rqstHandler.processData)
        rqstHandler.streamRequest.connect(lambda: serverInterface.setStreamUrl(streamUrl))
        rqstHandler.stateRequest.connect(handleStateRequest)
        rqstHandler.sourceListRequest.connect(handleListRequest)
    else:
        qDebug("VideoSwitcher::Signal connection prerequisites not met - one or more vars are None")

def handleListRequest():
    sources = [["1", "Camera Schorsch", "OFF"], ["2", "Camera Lisa", "OFF"], ["3", "Camera Bart", "OFF"], ["4", "Selfie Cam", "LIVE"]]
    qDebug("TestVideoSwitcher::Sending Sourcelist: " + str(sources))
    sleep(100)
    serverInterface.updateSourceList(sources)
        
def handleStateRequest(sourceId, status):
    qDebug("TestVideoSwitcher::Setting Source " + str(sourceId) + " to status " + str(status))
    sleep(100)
    serverInterface.setTallyToStatus(sourceId, status)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    #init vars
    rqstHandler = RequestHandler()
    serverInterface = TallyServer( SERVER_IP , SERVER_PORT, app )
    #wirecast = WirecastConnector(app)
    server = ThreadingServer(app)
    
    #connect signals and slots
    connectSignals()
    
    #open connection to server
    serverInterface.openConnection()
    
    #register with server
    serverInterface.registerClient("", "videoMixer", (socket.gethostbyname(socket.gethostname()), 3117)) # works on mac, doesnt work on linux
    
    #start listening for commands
    server.startListening(SWITCHER_PORT)
    
    #run the app
    sys.exit(app.exec_())
