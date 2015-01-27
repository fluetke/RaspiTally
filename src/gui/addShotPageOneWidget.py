'''
Created on 19.01.2015

@author: Florian
'''
from PyQt4.QtGui import QGridLayout, QLabel, QPushButton, QPixmap, QIcon,\
    QButtonGroup, QVBoxLayout, QWidget
from PyQt4.Qt import QHBoxLayout
from PyQt4.QtCore import QObject

class PageOneWidget(QWidget):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(PageOneWidget, self).__init__(parent)
        self.selectorLayout = QGridLayout()
        self.pageLabel = QLabel("Select Shotsize")
        self.checkableButtonGroup = QButtonGroup()
        self.checkableButtonGroup.setExclusive(True)
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.pageLabel)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.selectorLayout)
        self.mainLayout.addStretch()
        
        self.setLayout(self.mainLayout)
        
    def populateShotTypes(self, typeList):
        iteratr = 0
        for shotType in typeList:
            shotTypeSelector = QPushButton()
            shotTypeSelector.setCheckable(True)
            shotTypeSelectorPikto = QPixmap("gui/img/" + shotType + ".png")
            if shotTypeSelectorPikto == None:
                print("NOTHING WORKS")
            shotTypeSelector.setIcon(QIcon(shotTypeSelectorPikto))
            shotTypeSelector.resize(shotTypeSelectorPikto.size())
            #print(shotTypeSelectorPikto.rect().width())
            shotTypeSelector.setIconSize(shotTypeSelectorPikto.rect().size())
            self.checkableButtonGroup.addButton(shotTypeSelector)
            self.selectorLayout.addWidget(shotTypeSelector, iteratr / 4, iteratr%4)
            iteratr += 1