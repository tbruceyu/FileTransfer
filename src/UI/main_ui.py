# -*- coding: utf-8 -*-
# main entry
import sys
import os
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))
from PyQt4 import QtCore, QtGui
from core import transfer
from UI.classwizard import ConfigWizard
from UI.MainWindow import MainWindow
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    if not transfer.init_config():
        wizard = ConfigWizard()
        wizard.show()
    else:
        mainWindow = MainWindow()
        mainWindow.show()
    sys.exit(app.exec_())
