'''
Created on 2014-7-4

@author: yu
'''
from PyQt4 import QtGui
import sys
import resource.resource
from core.ServerDemon import MainTaskThread

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class DeamonWindow(QtGui.QFrame):
    def __init__(self):
        super(DeamonWindow, self).__init__()
        self.setUI()
        self.team = "Platform_Support"
    def setUI(self):
        self.createActions()
        self.createTrayIcon()
        self.setFixedSize(400, 400)
        icon = QtGui.QIcon(':/images/trash.svg')
        self.trayIcon.setIcon(icon)
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.iconActivated)
        self.mainLayout = QtGui.QHBoxLayout()
        self.runButton = QtGui.QPushButton()
        self.runButton.setText(_translate("Dialog", "Start", None))
        self.mainLayout.addWidget(self.runButton);
        self.setLayout(self.mainLayout)
        self.runButton.clicked.connect(self.startButtonClick)
    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
    def createActions(self):
        self.minimizeAction = QtGui.QAction("Mi&nimize", self,
                triggered=self.hide)

        self.maximizeAction = QtGui.QAction("Ma&ximize", self,
                triggered=self.showMaximized)

        self.restoreAction = QtGui.QAction("&Restore", self,
                triggered=self.showNormal)

        self.quitAction = QtGui.QAction("&Quit", self,
                triggered=self.exit)
    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.showNormal()
    def exit(self):
        QtGui.qApp.quit()
        sys.exit(0)
    def closeEvent(self, event):
        if self.trayIcon.isVisible():
#            QtGui.QMessageBox.information(self, "Systray",
#                    "The program will keep running in the system tray. To "
#                    "terminate the program, choose <b>Quit</b> in the "
#                    "context menu of the system tray entry.")
            self.setVisible(False)
            event.ignore()
    def startButtonClick(self):
        self.mainThread = MainTaskThread("Platform_Support")
        self.mainThread.start()