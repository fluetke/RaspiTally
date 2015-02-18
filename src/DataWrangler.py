'''
Created on 25.01.2015

@author: Florian
'''
from PyQt4.QtCore import pyqtSignal, QObject, QMutex, qDebug

class ListData(QObject):
    '''
    storage of listdata and handling with qtsignals is the main purpose of this class
    '''

    dataChanged = pyqtSignal(list)
    

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(ListData, self).__init__(parent)
        
        # define lists for storing data
        self.data = list()
                
        #add mutexes for threadsafety
        #self.dataMutex = QMutex()
        
    def updateData(self, data):
        # update stored version accordingly
        print("STORING DATA, LOCKING MUTEX")
        #self.dataMutex.lock()
        print("DATA DATA DATA")
        self.data = data
        self.dataChanged.emit(self.data)
        #self.dataMutex.unlock()
    
    '''add item to list at pos 
       - pos defaults to -1, the end of a list'''
    def addItem(self,item, pos=-1):
        #self.dataMutex.lock()
        self.data.insert(pos, item)
        qDebug("Emitting Signal Data changed")
        self.dataChanged.emit(self.data)
        #self.dataMutex.unlock()
        
    def remItem(self, pos):
       # 
        #self.dataMutex.lock()
        item = self.data.pop(pos)
        self.dataChanged.emit(self.data)
        #self.dataMutex.unlock()
        return item
        
    def movItem(self, _from, _to):
        #self.dataMutex.lock()
        item = self.data.pop(_from)
        self.data.insert(_to, item)
        self.dataChanged.emit(self.data)
        #self.dataMutex.unlock()        
        
    def itemAt(self, pos):
        if pos < len(self.data):
         #   self.dataMutex.lock()
            return self.data[pos]
          #  self.dataMutex.unlock()
        else:
            print("INDEX OUT OF BOUNDS")
            #TODO: emit error signal here
            
    def remove(self, item):
        try:
            self.data.remove(item)
        except ValueError:
            print("Item with ID: " + item._id + " not in List: " + str(self.data))
        finally:
            self.dataChanged.emit(self.data)
        
    def length(self):
        return len(self.data)
    
    def isEmpty(self):
        return False if len(self.data)>0 else True
    
    def getSubitems(self, indx):
        subs = list()
        
        if indx < len(self.data):
           # self.dataMutex.lock()
            for item in self.data:
                subs.append(item[indx])
           # self.dataMutex.unlock()
        return subs