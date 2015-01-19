'''
Created on 08.01.2015

@author: Florian
'''
from PyQt4.QtGui import QWidget, QPixmap, QLabel, QPushButton, QHBoxLayout,\
    QVBoxLayout, QApplication, QListWidgetItem, QPainter, QColor, qRgb, qRgba,\
    QFont, QPalette, QGridLayout, QSizePolicy
from PyQt4.Qt import qDebug, QPoint
from PyQt4.QtCore import pyqtSignal

class ShotlistItem(QWidget):
    
    delShotAtPos = pyqtSignal(int)
    addShotAtPos = pyqtSignal(int)
    movShotUp = pyqtSignal(int)
    movShotDown = pyqtSignal(int)
    
    def __init__(self, camId, shotType, listPos=None, parent=None):
        super(ShotlistItem, self).__init__(parent)
        
        self.listPos = listPos
        #init widgets used in this widget
        self.shotPicto = QPixmap("gui/img/"+shotType+".png")
        self.shotPictoLbl = QLabel("shotPicto")
        self.moveToFrontBtn = QPushButton("<-")
        self.moveToFrontBtn.setFixedHeight(48)
        self.moveToBackBtn = QPushButton("->")
        self.moveToBackBtn.setFixedHeight(48)
        self.addShotBtn = QPushButton("+")
        self.addShotBtn.setFixedHeight(48)
        self.delShotBtn = QPushButton("-")
        self.delShotBtn.setFixedHeight(48)
        
        #init components
        self.shotPicto = self.putTextOnPreview(self.shotPicto.scaledToHeight(80), camId)
        self.shotPictoLbl.setPixmap(self.shotPicto)
        #self.shotPictoLbl.setFixedHeight(120)
        self.shotPictoLbl.setFixedSize(self.shotPicto.size())
        if self.listPos == 0:
            self.delShotBtn.setDisabled(True)
            self.moveToFrontBtn.setDisabled(True)
        #init layouts
        self.meinLayout = QGridLayout()
        
        #setup new GridLayout
        self.meinLayout.addWidget(self.delShotBtn,0,0,2,3)
        self.meinLayout.addWidget(self.addShotBtn,0,3,2,3)
        #self.shotPictoLbl.setStyleSheet("QLabel { border: 1px solid green; margin: 0; }")
        self.meinLayout.addWidget(self.shotPictoLbl,2,0,3,6)
        self.meinLayout.addWidget(self.moveToFrontBtn,5,0,2,3)
        self.meinLayout.addWidget(self.moveToBackBtn,5,3,2,3)
        self.meinLayout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        
        self.setLayout(self.meinLayout)
            
        #setup fenster
        self.setFixedWidth(self.shotPictoLbl.width()+15)
        #self.setAutoFillBackground(True)
        self.connectSignals()
        #self.setBackgroundRole(QPalette.Base)
        
        # thanks to kalos for this post on http://www.qtforum.org/article/17154/drawing-text-on-a-pixmap.html?s=7bc34fd883a892ea5c33ff54e98163fbcc47a113#post67816, checked 18.01.2015
    def putTextOnPreview(self, pixmap, text):
        paint = QPainter(pixmap)
        paint.begin(pixmap)
        paint.setBrush(QColor(qRgba(0,0,0,1)))
        paint.drawPolygon(QPoint(0,0),QPoint(50,0),QPoint(50,15),QPoint(45,20), QPoint(0,20))
        paint.end()
        paint.begin(pixmap)
        paint.setPen(QColor(qRgb(255,255,255)))
        paint.setFont(QFont("Arial", 9, 200))
        paint.drawText(5,14, text)
        paint.end()
        return pixmap
  
    def connectSignals(self):
        self.moveToFrontBtn.clicked.connect(self.movUp)
        self.moveToBackBtn.clicked.connect(self.movDown)
        self.addShotBtn.clicked.connect(self.addShot)
        self.delShotBtn.clicked.connect(self.delShot)
        
    def addShot(self):
        self.addShotAtPos.emit(self.listPos+1)
        
    def delShot(self):
        self.delShotAtPos.emit(self.listPos)
        
    def movUp(self):
        self.movShotUp.emit(self.listPos)
        
    def movDown(self):
        self.movShotDown.emit(self.listPos)
    