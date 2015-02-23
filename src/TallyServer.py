'''
Created on 04.01.2015

@author: Florian
'''
from PyQt4.QtGui import QApplication
from os.path import sys
from PyQt4.QtCore import qDebug
from RequestHandler import RequestHandler
from storage import Container
from DataWrangler import ListData
from ConfigHandler import ConfigHandler
# from ThreadingServer import ThreadingServer
from network.EventConnectionHandler import EventConnectionHandler
from PyQt4.QtNetwork import QTcpServer, QHostAddress


## YES I KNOW GLOBAL VARS ARE BAD AND EVIL 
## BUT I DONT CARE FOR KNOW, AS LONG AS IT WORKS DURING EVAL
## FUCK SAFETY AND BEST PRACTICE

#usefull data for server operation
SERVER_PORT = 3771
    
def connectSignals():
    qDebug("TallyServer::Connecting Signals and Slots")
    rqstHandler.regClient.connect(clientSetup.registerClient) #connect client registration procedure
    rqstHandler.deregClient.connect(clientSetup.deregisterClient)
    rqstHandler.configEnd.connect(clientSetup.finalizeConfiguration)
    rqstHandler.stateRequest.connect(switchSource)
    rqstHandler.newSourcelist.connect(clientSetup.sources.updateData)
    rqstHandler.tallyRequest.connect(switchTally)
    rqstHandler.newShot.connect(shots.addItem)
    rqstHandler.movShot.connect(shots.movItem)
    rqstHandler.delShot.connect(shots.remItem)
    #rqstHandler.deregClient.connect(deregisterClient)
    rqstHandler.nextShotRequest.connect(continueWithNext)
    clientSetup.clientReady.connect(storeClient)
    clientSetup.directorReady.connect(storeDirector)
    clientSetup.switcherReady.connect(storeSwitcher)
    clientSetup.clientRemoved.connect(deregisterClient)
    #clientSetup.newRequest.connect()
   # server.dataReceived.connect(rqstHandler.processData)
    server.newConnection.connect(handleConnection)
    
def continueWithNext():
    if not clientSetup.configMode:
        if shots.length() > 1:
            switchSource(shots.itemAt(1)[0], "LIVE") 
    
def storeClient(client):
    '''adds a client to the client list '''
    qDebug("Adding Client to List - Client ID " + str(client._id))
    #connect client to client and shotslist to receive updates
    client.updateShotList(shots.data)
    shots.dataChanged.connect(client.updateShotList)
    clients.dataChanged.connect(client.updateClientList)
    client.setParent(app)
    client.nodeFinished.connect(clients.remove)
    clientSetup.directorReady.connect(client.enableControlledMode)
    clients.addItem(client)
        
def storeSwitcher(switcher):
    ''' stores a videoswitcher announced by the confighandler in memory'''
    
    switcher._id = "TVID130"
    #switcher.openConnection()
    # switcher.getStreamUrl() #TODO: Fix the handling of wirecast broadcast information in VideoSwitcher
    switcher.getSourceList()
    switcher.setParent(app)
    videoSwitcher.store(switcher)
    switcher.nodeFinished.connect(lambda: videoSwitcher.store(None))
    print("TallyServer::VideoSwitcher stored in memory")
     
def storeDirector(director):
    '''stores a new director node in memory, overwriting the old one'''
    
    director._id = "DIRECTOR" 
    director.endConfigurationMode(director._id)
    director.updateShotList(shots.data)
    shots.dataChanged.connect(director.updateShotList)
    clients.dataChanged.connect(director.updateClientList)
    director.setParent(app)
    directorNode.store(director)
    director.nodeFinished.connect(lambda: directorNode.store(None))
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
            qDebug("TallyServer::ERROR --- Source is " + str(source) + " status is " + str(status)) 
            
           

# instruct client to switch to status and turn tally light on if existent
def switchTally(sourceId, status):
    for client in clients.data:
        if client.status == status and client.source != sourceId:
            client.setTally("OFF")
            
        if client.source == sourceId:
            client.setTally(status)
            
    clients.dataChanged.emit(clients.data) # emit dataChanged signal of client list here to initiate client updates
      
def deregisterClient(clientId):#TODO: implement
    print("TallyServer::Deregistering Client with ID: " + str(clientId))
    for client in clients.data:
        print(str(client._id))
        if client._id == clientId:
            clients.remove(client)
            client.goodbye()

# def removeNode(node):
#     clients.remove(node)
        
def handleConnection():
    qDebug("New Connection incoming")
    socket = server.nextPendingConnection()
    connectionHdl = EventConnectionHandler(socket, app)
    clientSetup.newRequest.connect(connectionHdl.handleRequest)
    connectionHdl.dataReceived.connect(rqstHandler.processData)
    connections.append(connectionHdl)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # packet containers of data, as workaround for pythons bitchyness with globals
    #store the director node info for the old school tally variant 
    directorNode = Container()
    videoSwitcher = Container()
    # data lists
    clients = ListData(app)
    shots = ListData(app)
    connections = list()
    
    #add initial blank item to shotlist, to prevent layout errors
    shots.addItem(("BLANK","UNDEFINED"))
        
    rqstHandler = RequestHandler(app)
    clientSetup = ConfigHandler(app)
   # server = ThreadingServer(app)#
    server = QTcpServer(app)
    
    connectSignals()
    
    #server.startListening(SERVER_PORT)
    if server.listen(QHostAddress.Any, SERVER_PORT):
        qDebug("Server listening on port " + str(SERVER_PORT))
    
    app.exec_()
