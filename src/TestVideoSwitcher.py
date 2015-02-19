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
#from Wirecast import WirecastConnector
from PyQt4.Qt import qDebug

from PyQt4.QtNetwork import QTcpServer

#Globals
SERVER_IP = "127.0.0.1"
SERVER_PORT = 3771
SWITCHER_IP = "127.0.0.1"
SWITCHER_PORT = 3117
streamUrl = "rtsp://192.168.178.29/tallytest.sdp"

# connect signals to slots
def connectSignals():
    #check prerequisites
    if serverInterface != None and rqstHandler != None:
        serverInterface.dataReceived.connect(rqstHandler.processData)
        rqstHandler.streamRequest.connect(lambda: serverInterface.setStreamUrl(streamUrl))
        rqstHandler.stateRequest.connect(handleStateRequest)
        rqstHandler.sourceListRequest.connect(handleListRequest)
    else:
        qDebug("VideoSwitcher::Signal connection prerequisites not met - one or more vars are None")

def handleListRequest():
    sources = [["1", "Camera Schorsch", "OFF"], ["2", "Camera Lisa", "OFF"], ["3", "Camera Bart", "OFF"], ["4", "Selfie Cam", "LIVE"]]
    qDebug("TestVideoSwitcher::Sending Sourcelist: " + str(sources))
   # sleep(1)
    serverInterface.updateSourceList(sources)
    qDebug("Sources sent")
        
def handleStateRequest(sourceId, status):
    qDebug("TestVideoSwitcher::Setting Source " + str(sourceId) + " to status " + str(status))
    #sleep(1)
    serverInterface.setTallyToStatus(sourceId, status)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    #init vars
    rqstHandler = RequestHandler()
    serverInterface = TallyServer( SERVER_IP , SERVER_PORT, app )
    #wirecast = WirecastConnector(app)
    
    #connect signals and slots
    connectSignals()
    
    #open connection to server
    serverInterface.openConnection()
    #sleep(1000)
    #register with server
    serverInterface.registerClient("", "videoMixer", (SWITCHER_IP,SWITCHER_PORT)) # works on mac, doesnt work on linux

    #run the app
    sys.exit(app.exec_())
