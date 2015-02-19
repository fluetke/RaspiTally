'''
Created on 19.02.2015

@author: Florian
'''
from PyQt4.Qt import QObject

class TallyMessage(QObject):
    '''
    simple message container for tallyCommunication
    '''

    def __init__(self, sender, receipient, body):
        '''
        initiates simple message container for tallyCommunication
        '''
        
        self.payload = body
        self.recv = receipient
        self.sender = sender
        
    