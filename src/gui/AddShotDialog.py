'''
Created on 11.01.2015

@author: Florian
'''
from PyQt4.Qt import QDialog
from PyQt4.QtGui import QPushButton, QPixmap

class AddShotDialog(QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        super(AddShotDialog, self).__init__(parent)
        shotTypes = list("closeup", "wide", "overtheshoulder", "medium")
        okBtn = QPushButton()
        cancelBtn = QPushButton()
        
        for shotType in shotTypes:
            #shotIcon = QLabel("")
            shotimage = QPixmap("img/Closeup.png") 
            shotButton = QPushButton(shotimage)
            