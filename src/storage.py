'''
Created on 07.01.2015

@author: Florian
'''
from PyQt4.QtCore import QObject, QMutex

class Container(QObject):
    '''
    classdocs
    '''

    datenpaket = None
    listMode = False
    storageMutex = QMutex()
    
    def __init__(self, listmode=False):
        '''
        Constructor
        '''
        QObject.__init__(self)
        if listmode:
            datenpaket = list()
            self.listMode = True
    
    def store(self, data):
        self.storageMutex.lock()
        self.listMode = False
        self.datenpaket = data
        self.storageMutex.unlock()
        
    def storeList(self, data):
        self.storageMutex.lock()
        self.listMode = True
        self.datenpaket = data
        self.storageMutex.unlock()
        
    def load(self):
        return self.datenpaket
    
    def append(self, data):
        self.storageMutex.lock()
        if self.listMode:
            self.datenpaket.append(data)
        self.storageMutex.unlock()
            
    def isList(self):
        return self.listMode
    
    def isEmpty(self):
        return (self.datenpaket == None)