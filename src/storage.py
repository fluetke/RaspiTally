'''
Created on 07.01.2015

@author: Florian
'''
from PyQt4.QtCore import QObject, QMutex

class Container(QObject):
    '''
    classdocs
    '''

    empty = True
    datenpaket = None
    listMode = False

    def __init__(self, listmode=False):
        '''
        Constructor
        '''
        QObject.__init__(self)
        if listmode:
            datenpaket = list()
            
    
    def store(self, data):
        QMutex().lock()
        self.listMode = False
        self.empty = False
        self.datenpaket = data
        
    def load(self):
        return self.datenpaket
    
    def append(self, data):
        self.empty = False
        if self.listmode:
            self.datenpaket.append(data)
            
    def isList(self):
        return self.listmode
    
    def isEmpty(self):
        return self.empty