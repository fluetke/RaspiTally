'''
Created on 05.01.2015

@author: Florian
'''
from PyQt4.QtCore import pyqtSignal, QObject, qDebug
import json



class RequestHandler(QObject):
    '''
    classdocs
    '''

    #TODO: Add more specific typedefs
    #signals
    dataProcessed = pyqtSignal()
    regClient = pyqtSignal(str,object,str)
    deregClient = pyqtSignal(object)
    configStart = pyqtSignal()
    configEnd = pyqtSignal(object)
    stateRequest = pyqtSignal(object,object)
    tallyRequest = pyqtSignal(object,object)
    newClientlist = pyqtSignal(list)
    newShotlist = pyqtSignal(list)
    newSourcelist = pyqtSignal(list)
    sourceListRequest = pyqtSignal()
    newShot = pyqtSignal(object,int)
    delShot = pyqtSignal(int)
    movShot = pyqtSignal(int, int)
    streamRequest = pyqtSignal(object)
    streamAnswer = pyqtSignal(object)
    nextShotRequest = pyqtSignal()

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(RequestHandler, self).__init__(parent)
        
    def processData(self, data):
        if data != None:
            data_ordered = data.split(':')
        else: 
            #qDebug("NO DATA RECEIVED, EXITING")
            return
        
        #Server methods here
        #register a client
        if data_ordered[0] == "REGISTER":
            qDebug("CLIENT ASKS FOR REGISTRATION")
            if len(data_ordered) != 5:
                qDebug("MALFORMED REQUEST")
                return
            
            # structuring data in a more readable manner 
            # for better understanding
            clientId = data_ordered[1]
            clientType = data_ordered[2] #TODO: Replace with type enum to normalize data early on
            clientIp = data_ordered[3]
            clientPort = int(data_ordered[4])
            clientAddress = (clientIp, clientPort) #pack client network address tuple
            qDebug("REQUEST_HNDL::EMITTING SIGNAL REGCLIENT")
            # emit new client signal containing all information needed by the clientregistration method
            self.regClient.emit(clientType, clientAddress, clientId)
            
        elif data_ordered[0] == "DEREGISTER":
            qDebug("CLIENT DEREGISTERING")
            if len(data_ordered) != 2:
                qDebug("MALFORMED REQUEST")
                #TODO ADD SOMETHING TO NOTIFY CLIENT
                return
            
            clientId = data_ordered[1]
             
            # grabbing clientId and emitting signal for deregistration
            self.deregClient.emit(clientId)
            
        elif data_ordered[0] == "CONFIG_STARTED":
            qDebug("REQUEST_HANDLER::CONFIG STARTED")
            qDebug("ARGUMENT_LENGTH = " + str(len(data_ordered)))
            
            self.configStart.emit()
            
            
            
        elif data_ordered[0] == "CONFIG_DONE":
            clientId = None
            if len(data_ordered) == 2:
                clientId = data_ordered[1]
            
            self.configEnd.emit(clientId)
            
        elif data_ordered[0] == "SET_SOURCE":
            if len(data_ordered) < 3:
                qDebug("MALFORMED REQUEST - SOURCEID AND/OR STATUS MISSING")
                return
            
            clientId = data_ordered[1]
            clientStatus = data_ordered[2]
            
            self.stateRequest.emit(clientId, clientStatus)
            
        elif data_ordered[0] == "SET_TALLY":
            if len(data_ordered) < 3:
                qDebug("MALFORMED REQUEST - CLIENTID AND/OR STATUS MISSING")
                return
            
            tallyId = data_ordered[1]
            tallyStatus = data_ordered[2]
            
            self.tallyRequest.emit(tallyId, tallyStatus)
            
        elif data_ordered[0] == "UPDATE_CLIENTLIST":
            if len(data_ordered) <2:
                qDebug("MALFORMED REQUEST - CLIENTLIST MISSING")
                return 
            if len(data_ordered) > 2:
                qDebug("jsonD CLIENTLIST CONTAINS MULTIPLE DIVIDER CHARACTERS - JOINING")
                
            clientList = json.loads(data_ordered[1])
            qDebug("EMITTING SIGNAL NEWCLIENTLIST")
            #emit the new sourcelist signal containing the uptodate sourcelist received from the videomixer           
            self.newClientlist.emit(clientList)
            
        elif data_ordered[0] == "UPDATE_SHOTLIST":
            if len(data_ordered) <2:
                qDebug("MALFORMED REQUEST - SHOTLIST MISSING")
                return 
            if len(data_ordered) > 2:
                qDebug("jsonD SHOTLIST CONTAINS MULTIPLE DIVIDER CHARACTERS - JOINING")
                
            shotList = json.loads(data_ordered[1])
            
            #emit the new sourcelist signal containing the uptodate sourcelist received from the videomixer           
            self.newShotlist.emit(shotList)
            
        #receive a new sourcelist from a video switcher    
        elif data_ordered[0] == "UPDATE_SOURCELIST":
            qDebug("RECEIVING SOURCELIST FROM VIDEOMIXER")
            if len(data_ordered) > 2:
                qDebug("JSONed SOURCELIST CONTAINS MULTIPLE DIVIDER CHARACTERS - JOINING")
                
            sourceList = json.loads((data_ordered[1]))
            
            #emit the new sourcelist signal containing the uptodate sourcelist received from the videomixer           
            self.newSourcelist.emit(sourceList)
            print("EMITTING NEW SOURCELIST: " + str(sourceList))
            
            
        elif data_ordered[0] == "GET_SOURCELIST":
            qDebug("SOURCELIST REQUEST FROM SERVER")
            if len(data_ordered) > 1:
                qDebug("MALFORMED REQUEST SOURCELIST")
            
            #emit the new sourcelist signal containing the uptodate sourcelist received from the videomixer           
            self.sourceListRequest.emit()
        
        elif data_ordered[0] == "ADD_SHOT": 
            if len(data_ordered) > 3: 
                qDebug("JSOND SHOT CONTAINS MULTIPLE DIVIDER CHARACTERS - JOINING")
            if len(data_ordered) < 3:
                qDebug("MALFORMED REQUEST - SHOT OR POSITION MISSING")
                return
            
            shot = json.loads(data_ordered[1])
            position = int(data_ordered[2])
            
            self.newShot.emit(shot, position)
            
        elif data_ordered[0] == "DEL_SHOT":
            if len(data_ordered) != 2:
                qDebug("MALFORMED REQUEST - LENGTH")
                return
            
            shotId = int(data_ordered[1])
            
            self.delShot.emit(shotId)
            
        elif data_ordered[0] == "MOVE_SHOT":
            if len(data_ordered) != 3:
                qDebug("MALFORMED REQUEST - LENGTH")
                return
            
            shotId = int(data_ordered[1])
            newShotPos = int(data_ordered[2])
            
            self.movShot.emit(shotId, newShotPos)
    
        elif data_ordered[0] == "STORE_SOURCELIST":
            if len(data_ordered) > 2:
                qDebug("REQUEST_HNDL:: MALFORMED REQUEST - LENGTH")
            sourceJson = data_ordered[1]
            sourceList = json.loads(sourceJson)
            
            qDebug("REQUEST_HNDL::EMITTING STORE_SOURCELIST SIGNAL")
            self.newSourcelist.emit(sourceList)
    
        elif data_ordered[0] == "GET_STREAM_URL":
            qDebug("REQUEST_HNDL::STREAM_URL REQUEST WITH LENGTH " + str(len(data_ordered)) + " RECEIVED")
            if len(data_ordered) != 2:
                qDebug("MALFORMED REQUEST - CLIENT ID MISSING")
                return
            
            clientId = data_ordered[1]
            
            qDebug("REQUEST_HNDL::EMITTING STREAM REQUEST SIGNAL")
            self.streamRequest.emit(clientId)
        
        elif data_ordered[0] == "SET_STREAM_URL":
            streamUrl = ""
            if len(data_ordered) < 2: #TODO: change test for stream url validity
                qDebug("MALFORMED REQUEST - STREAM_URL MISSING")
                return
            else:
                print(data[len(data_ordered[0])+1:])
                streamUrl=data[len(data_ordered[0])+1:]
#           
            self.streamAnswer.emit(streamUrl)
            
        elif data_ordered[0] == "NEXT_SHOT":
            self.nextShotRequest.emit()
            
        else:
            qDebug("UNKNOWN REQUEST: " + str(data_ordered))
            return
        
            