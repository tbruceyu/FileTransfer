import sys
import os
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))
from UI.DeamonWindow import DeamonWindow
from PyQt4 import QtGui
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = DeamonWindow()
    window.show()
    sys.exit(app.exec_())