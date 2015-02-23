'''
Created on 25.01.2015

@author: Florian
'''
from PyQt4.QtCore import QObject, qDebug
from DataWrangler import ListData
from PyQt4.Qt import pyqtSignal
from network.nodes import TallyClient, TallySwitcher


class ConfigHandler(QObject):
    '''
    takes care of configuring the clients and managing of configuration wait lists
    '''

    # establish signals
    confActive = pyqtSignal(object) #TallyNode(client)
    confInactive = pyqtSignal() 
    switcherReady = pyqtSignal(object) #TallySwitcher(switcher)
    clientReady = pyqtSignal(object) #TallyClient(client)
    clientRemoved = pyqtSignal(str) # str(id)
    directorReady = pyqtSignal(object) #TallyClient(director)
    newRequest = pyqtSignal(object) # forward all signals/messages from connected clients
    
    clientsHandled = 0 # increments with each client handled in this 

    def __init__(self, parent=None):
        '''
        construct a new configHandler instance for handling newly connected clients
        '''
        super(ConfigHandler, self).__init__(parent)
        
        #setup waiting list for clients to be configured
        self.queue = ListData(self)
        self.sources = ListData(self) #list of sources for configuration
        
        self.idToSource = dict()
        self.configMode = False # set config mode to default
        self.currentCandidate = None # client being configured
        self.currentSource = None # currently live source
        self.videoUrl = None # url of videostream
        
        #connect signals and slots
        self.sources.dataChanged.connect(self.runConfig)
        self.queue.dataChanged.connect(self.runConfig)
        
        
    def checkRequirements(self):
        ''' 
        checks if the necessary data for configuration is available and 
        the configuration is not running - returns true when ready
        '''
        qDebug("ConfigHandler::checking Requirements - SourcesList is full: " + str(not self.sources.isEmpty()) + " Queue has entries: " + str(not self.queue.isEmpty()))
        if not self.configMode:
            if self.sources.isEmpty() or self.queue.isEmpty():
                return False
            
            if self.currentCandidate == None:
                return True
            else: 
                qDebug("ConfigHandler::Warning: ConfigClient is not empty, despite configMode being False")
                return False
        else:
            return False
            
    
    def runConfig(self):
        '''
        run configuration:
           * checks if the requirements are met(unassigned clients and sources available)
           * grabs a client from the list of clients 
           * sends the necessary information to the client
           * finally sets the configMode flag and signals to the other classes 
        that configuration has begun for client x 
        '''
        
        if self.checkRequirements():
            qDebug("ConfigHandler::Config started, REQUIREMENTS FULLFILLED")
            self.configMode = True
        
            self.currentCandidate = self.queue.remItem(0)
     
            self.currentCandidate.sendRequest.connect(self.newRequest) #connect requests to this classes-signal as relay
            self.currentCandidate.storeSourceList(self.sources.getSubitems(0)) # generate sourcelist for this feature
            qDebug("ConfigHandler::Starting config mode")
            self.currentCandidate.startConfigurationMode()
            self.confActive.emit(self.currentCandidate)
        elif not self.configMode: 
            qDebug("ConfigHandler::REQUIREMENTS NOT MET")
            self.confInactive.emit()
            
    
    def registerClient(self, _type, address, _id=None):
        ''' registerClient:
        * accepts register-signals from a requesthandler
        * tests for special types of clients(director and videomixer)
        * checks if client is already known, if so instructs server to remove client
        * emits signal for the appropriate client type 
        '''
        if _type == "videoMixer":
            tmpClient = TallySwitcher(address[0], address[1], self)
            tmpClient.sendRequest.connect(self.newRequest)
            self.switcherReady.emit(tmpClient)
            return
        
        elif _type == "director":
            tmpClient = TallyClient(address[0], address[1], self)
            tmpClient.c_type = _type
            tmpClient.sendRequest.connect(self.newRequest)
            self.directorReady.emit(tmpClient)
            return

        else:
            print("TEST_REGOSTER CLINET")
            if _id in self.idToSource:
                self.deregisterClient(_id)
            tmpClient = TallyClient(address[0],address[1], self)
            tmpClient._id = "CAM_" + str(self.clientsHandled)
            self.queue.addItem(tmpClient) # add client to config waiting list
            qDebug("ConfigHandler::Config busy - client added to queue")
            self.clientsHandled += 1

        
    def updateSelectedSource(self, source):
        ''' 
        stores the currently selected source_id
        in self.currentSource, for later use by configEnd 
        '''
        if self.configMode == True:
            self.currentSource = source
            
    
    def finalizeConfiguration(self):
        ''' 
        sets the source of the current configuration candidate to the stored value
        tells the client to leave configuration mode and what his new id is.
        also makes the client known to the rest of the world, by emitting it in a signal
        then resets the configuration mode flag and candidate variable to allow another round of 
        configuration to start 
        '''
        self.currentCandidate.source = self.currentSource
        self.currentCandidate.endConfigurationMode(self.currentCandidate._id)
    
        self.clientReady.emit(self.currentCandidate)
        print("ConfigHandler::Adding client to dictonary: ID -" + str(self.currentCandidate._id) + "source ---" + str(self.currentCandidate.source))
        self.idToSource[self.currentCandidate._id] = self.currentCandidate.source #FIXME: try this and see if there are problem with non-existing keys
        
        #cleanup and reset for new round
        self.configMode = False
        for source in self.sources.data: #remove assigned source from sourcelist
            if source[0] == self.currentCandidate.source:
                self.currentCandidate = None # a little bit of trickery here, currentCandidate has to be None before a new config can trigger
                try:
                    toBeRemoved = self.sources.data.index(source)
                    self.sources.remItem(toBeRemoved)
                except ValueError:
                    qDebug("ConfigHandler::The selected dataset does not exists in self.sources")
                return
        
    
    def deregisterClient(self, clientID):
        '''
        deregister a connected client and return the source token to the pool
        '''
        source = None
        try:
            source = self.idToSource.pop(clientID)
        except KeyError:
            qDebug("ConfigHandler::ClientID for deregistration unknown, ignoring")
        finally:
            if source != None:
                self.sources.addItem(source) # remove source from dictionary and re-add it to sourcelist
            self.clientRemoved.emit(clientID)
            
        return True