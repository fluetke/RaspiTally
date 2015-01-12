'''
Created on 09.01.2015

@author: Florian
'''
from PyQt4.QtGui import QWidget, QPalette


class VideoWidget(QWidget):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(VideoWidget, self).__init__(parent)
        self.setFixedSize(320,200)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color:black;")