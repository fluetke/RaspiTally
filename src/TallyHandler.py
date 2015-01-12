'''
Created on 11.01.2015

@author: Florian
'''
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal


class TallyHandler(QObject):
    '''
    This takes care of lighting up the tally light device connected to the raspberry
    '''

    tallyStateChanged = pyqtSignal()
    tallyError = pyqtSignal()
    
    def __init__(self, parent=None):
        '''
        initialize the handler
        '''
        super(TallyHandler, self).__init__(parent)
        pass
    
    #TODO: Implement GPIO handling here
    def setState(self,state="OFF"):
        pass
#         if state == "PREVIEW":
#             GPIO.setEnabled(previewGPIO)
#             GPIO.setDisabled(liveGPIO)
#         if state == "LIVE":
#             GPIO.setEnabled(liveGPIO)
#             GPIO.setDisabled(previewGPIO)
#         if state == "OFF":
#             GPIO.setDisabled(liveGPIO)
#             GPIO.setDisabled(previewGPIO)
#         if state == "EMERGENCY":
#             GPIO.setEnabled(liveGPIO)
#             GPIO.setEnabled(previewGPIO)
#             
#         return True