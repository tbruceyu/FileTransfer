# -*- coding: utf-8 -*-
# main entry
import sys
import os
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))
from PyQt4 import QtCore, QtGui
from core import transferPC
from core import utils
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
    if hasattr(sys, 'frozen'):
        currentPath = os.path.abspath(sys.argv[0])
    else:
        currentPath = os.path.abspath(os.path.realpath(__file__))
    utils.setProgramPath(currentPath)
    import sys
    app = QtGui.QApplication(sys.argv)
    if not transferPC.init_config():
        wizard = ConfigWizard()
        wizard.show()
    else:
        mainWindow = MainWindow()
        mainWindow.show()
    sys.exit(app.exec_())
