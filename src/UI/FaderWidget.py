from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class FaderWidget(QWidget):
    def __init__(self,parent=None):
        super(FaderWidget,self).__init__(parent)

        if parent:
            self.startColor=parent.palette().window().color()
        else:
            self.startColor=Qt.White

        self.currentAlpha=0
        self.duration=1000

        self.timer=QTimer(self)
        self.connect(self.timer,SIGNAL("timeout()"),self.update)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(parent.size())

    def start(self):
        self.currentAlpha=255
        self.timer.start(100)
        self.show()

    def paintEvent(self,event):
        semiTransparentColor=self.startColor
        semiTransparentColor.setAlpha(self.currentAlpha)
        painter=QPainter(self)
        painter.fillRect(self.rect(),semiTransparentColor)
        self.currentAlpha-=(255*self.timer.interval()/self.duration)

        if self.currentAlpha<=0:
            self.timer.stop()
            self.close()
