'''
Created on 20.01.2015

@author: Florian
'''

# pyqt imports
from PyQt4.QtCore import qDebug, QObject, pyqtSignal
# special appleHandling
#from applescript import AppleScript, ScriptError


class WirecastConnector(QObject):
    '''
    This class handles the applescripts needed to run actions in Wirecast,
    '''

    sourcesReady = pyqtSignal(list)
    sourceSet = pyqtSignal(str, str)

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(WirecastConnector, self).__init__(parent)
       # self.sourceListScript = AppleScript("appleScript/getListOfSources.scpt")
       # self.setStatusScript = AppleScript("appleScript/setShotStatus.scpt")
        
    # set source to state using the applescript handler for wirecast
    def setSource(self, source, state):
        #qDebug("SWITCHING " + str(source) + " TO STATE " + str(state))
        #try:
         #   pass
            #self.setStatusScript.call("setStatus", source, state)
        #except ScriptError:
        #    qDebug("An error occured: ScriptError")
         #   return False
        #finally:
         #   self.sourceSet.emit(source, state)
        return True
    
    # grab the sources from wirecast and return them as list to the caller object
    def getSources(self):
        #try:
            #sources = self.sourceListScript.run()
        sources = [["CAM1", "OFF"], ["CAM2", "OFF"], ["CAM3", "OFF"], ["CAM4", "OFF"]]
        self.sourcesReady.emit(sources)
#         except ScriptError:
#             qDebug("Grabbing SourcesList returned an error: ScriptError")
#             return False
        #except:
         #   return False