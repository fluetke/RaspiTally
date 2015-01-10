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


## YES I KNOW GLOBAL VARS ARE BAD AND EVIL 
## BUT I DONT CARE FOR KNOW, AS LONG AS IT WORKS DURING EVAL
## FUCK SAFETY AND BEST PRACTICE

#lists of things
threadList = list()
clientList = list()
shotList = list()
sourceList = Container()

streamUrl = Container()

#vars for configuration
configMode = Container()
configWaitinglist = list()

def initHandling():
    qDebug("Threadlist size is: " + str(len(threadList)))
    connHndl = ConnectionHandlerThread(server.nextPendingConnection())
    connHndl.finished.connect(connHndl.deleteLater)
    connHndl.dataReceived.connect(rqstHandler.processData)
    connHndl.start()
    threadList.append(connHndl)
    
def connectSignals():
    qDebug("MAIN:: CONNECTING SIGNALS AND SLOTS")
    rqstHandler.regClient.connect(registerClient) #connect client registration procedure
    rqstHandler.configStart.connect(setConfigMode)
    rqstHandler.configEnd.connect(unsetConfigMode)
    rqstHandler.stateRequest.connect(switchSource)
    rqstHandler.newSourcelist.connect(storeSourcelist)
    rqstHandler.tallyRequest.connect(switchTally)
    #rqstHandler.newShotlist.connect(updateRemoteShotlists())
    rqstHandler.newShot.connect(addShot)
    rqstHandler.movShot.connect(moveShot)
    rqstHandler.delShot.connect(delShot)
    rqstHandler.streamAnswer.connect(saveStreamUrl)
    rqstHandler.deregClient.connect(deregisterClient)
    qDebug("MAIN:: DONE CONNECTING SIGNALS AND SLOTS")

#registers a client with the server
def registerClient(clientId, clientType, clientAddress):
    # take the clientAddress, which should be delivered as qByteArray and turn it into string and int respectively
    ipAddress = clientAddress[0]#.data().decode('UTF-8')
    port = int(clientAddress[1])
    
    if clientType == "videoMixer":
        qDebug("SERVER::REGISTERING VIDEO_MIXER_OUTPUT - VIDEO MIXER IS CURRENTLY: " + str(videoSwitcher.isEmpty()))
        if videoSwitcher.isEmpty():
            tempSwitcher = TallySwitcher(ipAddress, port)
            tempSwitcher.id = "TVID130"
            tempSwitcher.openConnection()
            tempSwitcher.getStreamUrl()
            tempSwitcher.getSourceList()
            videoSwitcher.store(tempSwitcher)
            qDebug("SERVER::STORED VIDEOSWITCHER IN MEMORY - AWAITING STREAMURL")
        else:
            qDebug("VIDEOSWITCHER ALREADY PRESENT, PLEASE DEREGISTER BEFORE ADDING NEW VIDEO SWITCHER")
    
    elif clientType == "director": 
        qDebug("SERVER::REGISTERING DIRECTOR_CONSOLE")
        if directorNode.isEmpty():
            dirNode = TallyClient(ipAddress, port)
            dirNode.id = "DIRECTOR" 
            dirNode.c_type = clientType
            dirNode.endConfigurationMode(dirNode.id)
            directorNode.store(dirNode)
            return
        else:
            qDebug("DIRECTOR ALREADY PRESENT - PLEASE DEREGISTER FIRST")
                
    else: #if client is not videoswitcher
        qDebug("SERVER::REGISTERING TALLY_DEVICE")
        if clientId != "":
            for client in clientList: #check if client is already known
                if client.id == clientId:
                    client.ip = ipAddress
                    client.port = port
                    client.setTally("OFF")
                    client.updateClientList(clientList)
                    client.updateShotList(shotList)
                    return #all is done for an existing client, safe to exit here
            
        #if the client is not yet known to the system, create a new one and add it
        newClient = TallyClient(clientAddress[0], clientAddress[1])
        newClient.id = "CAMERA_" + str(len(clientList)+1) #FIXME: if client registration requests pile up, the id for all clients will be the same, as the listlength does not change
        qDebug("STORING NEW CLIENT WITH ID " + str(newClient.id)) 
        #poke client to start configuration, but only if its a camera, as the director has no video input
        #if configClient.isEmpty(): #if configuration is not already preparing a client
        newClient.openConnection()
        newClient.setStreamUrl(streamUrl.load())
        newClient.storeSourceList(generateConfigSourceList())
        newClient.startConfigurationMode()
        configClient.store(newClient)
        #else:
        #    qDebug("SERVER::CONFIG OF ANOTHER CLIENT IN PROGRESS - ADDING REQUEST TO WAITING LIST")
        #    configWaitinglist.append(newClient)
        
        return
                
def generateConfigSourceList():
    configSourceList = list()
    for source in sourceList.load():
        configSourceList.append(source[0])
        
    return configSourceList

# updates clients in list and sends the new clientList    
def updateClients():
    tempClientList = list()
    for client in clientList:
        tempClientList.append((client.id,client.status))
    for client in clientList:
        client.updateClientList(tempClientList)
                                
def setConfigMode():
    qDebug("Setting config mode to True")
    configMode.store(True) # set configmode, so no tally request from other clients are accepted)
    
    
def unsetConfigMode(clientId):
    if not configClient.isEmpty():
        tempConfCli = configClient.load()
        tempConfCli.endConfigurationMode(tempConfCli.id)
        tempConfCli.updateShotList(shotList)
        clientList.append(tempConfCli)
        updateClients() # finally notify the others that new client update can be send now #FIXME: replace with proper signal
    if len(configWaitinglist) > 0:
        configClient.store(configWaitinglist.pop())
        configClient.load().startConfigurationMode(streamUrl, generateConfigSourceList())
    else:
        configMode.store(False)
        
# instruct videoswitcher to switch videosource to status
def switchSource(clientId, status):
    assert videoSwitcher.isEmpty() == False # the videoswitcher should not be empty at this point
    assert configMode.isEmpty() == False # config mode should contain something right now
    qDebug("CONFIG MODE IS " + str(configMode.load()))
    tempSwitcher = videoSwitcher.load()
    if configMode.load():
        # if config mode is true, it is usually safe to assume that clientid contains a direct source id
        tempSwitcher.setSourceToStatus(clientId, status)
        configClient.load().source = clientId # update source of config client each time a source is changed during config
        return
    
    #iterate through list of clients to find the one submitted and hand its source id to the videoswitcher
    for client in clientList:
        if client.id == clientId:
            tempSwitcher.setSourceToStatus(client.source, status)
            return
            
    qDebug("CLIENT NOT FOUND")
    return

# instruct client to switch to status and turn tally light on if existent
def switchTally(sourceId, status):
    if configMode.load():
        return # ignore request in config mode as the source is not assigned to a client yet
    for client in clientList:
        if client.source == sourceId:
            client.setTally(status)
            qDebug("CLIENT FOUND - PREPARING TALLY REQUEST")
            return
        
    qDebug("SOURCE NOT FOUND")
    return

def updateRemoteShotlists():
    for client in clientList:
        client.updateShotList(shotList)
        
def addShot():
    pass

def delShot():
    pass

def moveShot():
    pass 

def getStreamUrl():
    assert videoSwitcher != None
    videoSwitcher.getStreamUrl()
    # this should not be called during eval anyways, as the streamurl is piped to the client during configuration

def saveStreamUrl(url):
    qDebug("SERVER::SAVING STREAM_URL")
    if not streamUrl.isList():
        streamUrl.store(url)
        qDebug("SERVER::STREAMURL STORED AS " + url)
    else:
        qDebug("SERVER::STREAMURL IS LIST - SOMETHING IS WRONG HERE")
        
def storeSourcelist(srcList):
    qDebug("STORING SOURCELIST IN MEMORY - " + str(srcList))
    sourceList.store(srcList) 
    
def deregisterClient(clientId):
    pass
    
def printData(data):
    qDebug(data)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    configMode.store(False) # initially set configmode to false
    
    # packet containers of data, as workaround for pythons bitchyness with globals
    #store the director node info for the old school tally variant 
    directorNode = Container()
    videoSwitcher = Container()
    configClient = Container()
        
    rqstHandler = RequestHandler()

    connectSignals()

    server = QTcpServer()
    server.newConnection.connect(initHandling)
    server.listen(QHostAddress.Any, 3771)
    
    app.exec()