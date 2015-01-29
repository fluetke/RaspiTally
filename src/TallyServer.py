'''
Created on 04.01.2015

@author: Florian
'''
from PyQt4.QtNetwork import QTcpServer, QHostAddress
from PyQt4.QtGui import QApplication
from ConnectionHandler import ConnectionHandlerThread
from os.path import sys
from PyQt4.QtCore import qDebug, pyqtSignal
from RequestHandler import RequestHandler
from nodes import TallySwitcher, TallyClient
from storage import Container
from DataWrangler import ListData
from ConfigHandler import ConfigHandler


## YES I KNOW GLOBAL VARS ARE BAD AND EVIL 
## BUT I DONT CARE FOR KNOW, AS LONG AS IT WORKS DURING EVAL
## FUCK SAFETY AND BEST PRACTICE

#lists of things
#streamUrl = Container()

def initHandling():
    qDebug("Threadlist size is: " + str(len(threadList)))
    connHndl = ConnectionHandlerThread(server.nextPendingConnection())
    connHndl.finished.connect(connHndl.deleteLater)
    connHndl.error.connect(networkErrorPrinter)
    connHndl.dataReceived.connect(rqstHandler.processData)
    connHndl.setParent(app)
    connHndl.start()
    threadList.append(connHndl)
    
def networkErrorPrinter(sockerr, errmsg):
    qDebug("SOCKET ERROR(" + str(sockerr) + "): " + str(errmsg))
    
def connectSignals():
    qDebug("MAIN:: CONNECTING SIGNALS AND SLOTS")
    rqstHandler.regClient.connect(clientSetup.registerClient) #connect client registration procedure
    rqstHandler.configEnd.connect(clientSetup.finalizeConfiguration)
    rqstHandler.stateRequest.connect(switchSource)
    rqstHandler.newSourcelist.connect(clientSetup.sources.updateData)
    rqstHandler.tallyRequest.connect(switchTally)
    rqstHandler.newShot.connect(shots.addItem)
    rqstHandler.movShot.connect(shots.movItem)
    rqstHandler.delShot.connect(shots.remItem)
    #rqstHandler.streamAnswer.connect(saveStreamUrl)
    #rqstHandler.deregClient.connect(deregisterClient)
    rqstHandler.nextShotRequest.connect(continueWithNext)
    clientSetup.clientReady.connect(storeClient)
    clientSetup.directorReady.connect(storeDirector)
    clientSetup.switcherReady.connect(storeSwitcher)
    clientSetup.clientRemoved.connect(deregisterClient)
#     clientSetup.confActive.connect(rqstHandler.setIpFilter)
#     clientSetup.confInactive.connect(rqstHandler.clearIpFilter)
    
def continueWithNext():
    if not clientSetup.configMode:
        if shots.length() > 1:
            switchSource(shots.itemAt(1)[0], "LIVE") 
    
def storeClient(client):
    '''adds a client to the client list '''
    
    #connect client to client and shotslist to receive updates
    client.updateShotList(shots.data)
    shots.dataChanged.connect(client.updateShotList)
    clients.dataChanged.connect(client.updateClientList)
    client.setParent(app)
    clients.addItem(client)
        
def storeSwitcher(switcher):
    ''' stores a videoswitcher announced by the confighandler in memory'''
    
    switcher._id = "TVID130"
    switcher.openConnection()
    # switcher.getStreamUrl()
    switcher.getSourceList()
    switcher.setParent(app)
    videoSwitcher.store(switcher)
    print("TallyServer::VideoSwitcher stored in memory")
     
def storeDirector(director):
    '''stores a new director node in memory, overwriting the old one'''
    
    director._id = "DIRECTOR" 
    director.endConfigurationMode(director._id)
    director.setParent(app)
    directorNode.store(director)
    print("TallyServer::DirectorConsole stored in memory")

def switchSource(clientId, status):
    assert videoSwitcher != None
    ''' instruct the VideoSwitcher(in this case Wirecast) 
        to set source assigned to clientID to status '''
    
    source = "732" #id of blank shot here
    try: 
        source = clientSetup.idToSource[clientId]
    except KeyError:
        source = clientId
    finally: 
        if source != None:
            videoSwitcher.load().setSourceToStatus(source, status)
            clientSetup.updateSelectedSource(source)
            if status == "LIVE":
                shots.remItem(0)
                if shots.length() == 0 or clientId != shots.itemAt(0)[0]:
                    shots.addItem((clientId, "UNDEFINED"), 0)
                    if shots.length() > 1:
                        switchSource(shots.itemAt(1)[0], "PREVIEW")
            
        else:
            qDebug("ERROR --- Source is " + str(source) + " status is " + str(status)) 
            
           

# instruct client to switch to status and turn tally light on if existent
def switchTally(sourceId, status):
    for client in clients.data:
        if client.status == status and client.source != sourceId:
            client.setTally("OFF")
            
        if client.source == sourceId:
            client.setTally(status)
            
    clients.dataChanged.emit(clients.data) # emit dataChanged signal of client list here to initiate client updates
      
def deregisterClient(clientId):#TODO: implement
    pass
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # packet containers of data, as workaround for pythons bitchyness with globals
    #store the director node info for the old school tally variant 
    directorNode = Container()
    videoSwitcher = Container()
    # data lists
    threadList = list()
    clients = ListData(app)
    shots = ListData(app)
    
    shots.addItem(("BLANK","UNDEFINED"))
        
    rqstHandler = RequestHandler(app)
    clientSetup = ConfigHandler(app)
    connectSignals()

    server = QTcpServer(app)
    server.newConnection.connect(initHandling)
    if not server.listen(QHostAddress.Any, 3771):
        qDebug("SERVER FAILED")
    else: 
        qDebug("Server listening on port: " + str(server.serverPort()))
    
    app.exec_()
