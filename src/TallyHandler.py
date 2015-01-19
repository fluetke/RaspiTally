'''
Created on 11.01.2015

@author: Florian
'''
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal
#import RPi.GPIO as GPIO # grab raspberry gpio api

class TallyHandler(QObject):
    '''
    This takes care of lighting up the tally light device connected to the raspberry
    '''
    
    # setup the gpio-pin-numbers
    TALLY_LIVE_PIN = 38 # GPIO20
    TALLY_PREVIEW_PIN = 37 # GPIO26 
        
    # setup the signals
    tallyStateChanged = pyqtSignal()
    tallyError = pyqtSignal()
    
    def __init__(self, parent=None):
        '''
        initialize the gpio board
        '''
        super(TallyHandler, self).__init__(parent)
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(self.TALLY_LIVE_PIN, GPIO.OUT)
        #GPIO.setup(self.TALLY_PREVIEW_PIN, GPIO.OUT)
    
    
    def setState(self,state="off"):
        pass
#         if state == "preview":
#             GPIO.output(self.TALLY_LIVE_PIN, GPIO.LOW)
#             GPIO.output(self.TALLY_PREVIEW_PIN, GPIO.HIGH)
#         elif state == "live":
#             GPIO.output(self.TALLY_PREVIEW_PIN, GPIO.LOW)
#             GPIO.output(self.TALLY_LIVE_PIN,GPIO.HIGH)
#         elif state == "off":
#             GPIO.output(self.TALLY_LIVE_PIN, GPIO.LOW)
#             GPIO.output(self.TALLY_PREVIEW_PIN, GPIO.LOW)
#         elif state == "emergency":
#             GPIO.output(self.TALLY_LIVE_PIN,GPIO.HIGH)
#             GPIO.output(self.TALLY_PREVIEW_PIN, GPIO.HIGH) 
#         return True