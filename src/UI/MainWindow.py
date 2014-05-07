from PyQt4 import QtCore, QtGui, Qt
from core import transfer, utils
from core.transfer import WorkThread
from UI.ConfigurePage import ConfigInfoPage
from UI.HistoryPage import HistoryPageWindow
DEBUG_TAG = "MainWindow"
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
class MainWindow(QtGui.QFrame):
    def __init__(self):
        super(MainWindow, self).__init__()
        transfer.init()
        self.setUI()

    def setUI(self):
        palette =  QtGui.QPalette();
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(192,253,123))
        #palette.setBrush(QPalette::Background, QBrush(QPixmap(":/background.png")));
        self.setPalette(palette)
        #splitter = QtGui.QSplitter(self)
        self.createActions()
        self.createTrayIcon()
        qss_file = open('../../styles/common.qss').read()
        self.setStyleSheet(qss_file)
        self.setFixedSize(250, 400)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.mainWindowWidget = QtGui.QWidget(self)
        self.mainWindowWidget.setGeometry(QtCore.QRect(0, 0, 250, 400))
        self.mainWindowLayout = QtGui.QVBoxLayout(self.mainWindowWidget)
        self.runSettingWidget = QtGui.QWidget(self.mainWindowWidget)
        self.runSettingWidget.setGeometry(QtCore.QRect(50, 30, 160, 80))
        self.runSettingLayout = QtGui.QVBoxLayout(self.runSettingWidget)
        self.runSettingLayout.setMargin(0)
        self.Checkboxes = {'pop' : QtGui.QCheckBox(self.runSettingWidget),
                          'backup' : QtGui.QCheckBox(self.runSettingWidget),
                          }
        self.Checkboxes['pop'].setChecked(transfer.RUN_CONFIG['pop'])
        self.Checkboxes['backup'].setChecked(transfer.RUN_CONFIG['backup'])
        self.runSettingLayout.addWidget(self.Checkboxes['pop'])
        self.runSettingLayout.addWidget(self.Checkboxes['backup'])
        self.horizontalLayoutWidget = QtGui.QWidget(self.mainWindowWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 130, 161, 51))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.RunButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.RunButton)
        self.StopButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.StopButton)
        self.createThreadWidget()
        self.settingButton = QtGui.QPushButton(self.mainWindowWidget)
        self.settingButton.setText("Settings")
        self.settingButton.setStyleSheet("QPushButton { background: rgb(59, 138, 113);} \
                                            QPushButton:hover {background: rgb(165, 165, 113);}")
        self.settingButton.setGeometry(QtCore.QRect(10, 300, 100, 30))
        self.historyButton = QtGui.QPushButton(self.mainWindowWidget)
        self.historyButton.setText("History")
        self.historyButton.setStyleSheet("QPushButton { background: rgb(59, 138, 113);} \
                                            QPushButton:hover {background: rgb(165, 165, 113);}")
        self.historyButton.setGeometry(QtCore.QRect(150, 300, 100, 30))
#        splitter.addWidget(self.mainWindowWidget)
#        splitter.addWidget(self.listwidget)
#        splitter.setOrientation(QtCore.Qt.Horizontal)
        self.retranslateUi(self)
        #QtCore.QObject.connect(self.RunButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.RunButtonClicked)
        QtCore.QMetaObject.connectSlotsByName(self)
#        icon = QtGui.QIcon('../../images/bad.svg')
#        self.trayIcon.setIcon(icon)
        self.setIconByState(utils.STOPPED)
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.iconActivated)
        self.RunButton.clicked.connect(self.RunButtonClick)
        self.StopButton.clicked.connect(self.StopButtonClick)
        self.settingButton.clicked.connect(self.settingButtonClick)
        self.historyButton.clicked.connect(self.historyButtonClick)
        self.StopButton.setEnabled(False)
        self.Checkboxes['pop'].toggled.connect(self.PopCheckboxToggle)
        self.Checkboxes['backup'].toggled.connect(self.BackupCheckboxToggle)
    def setIconByState(self, state):
        if state == utils.STOPPED:
            icon = QtGui.QIcon('../../images/bad.svg')
        elif state == utils.WAITING:
            icon = QtGui.QIcon('../../images/heart.svg')
        elif state == utils.WATCHING:
            icon = QtGui.QIcon('../../images/trash.svg')
        elif state == utils.WORKING:
            icon = QtGui.QIcon('../../images/trash.svg')
        self.trayIcon.setIcon(icon)
    def SuccessStartedSlot(self):
        self.RunButton.setEnabled(False)
        self.StopButton.setEnabled(True)
        for key in self.Checkboxes:
            self.Checkboxes[key].setEnabled(False)
    def PromptSlot(self, type = 0, string=None):
        if type == utils.INFO:
            QtGui.QMessageBox.information(self, string, "hdfsldfj")
        elif type == utils.WARNING:
            QtGui.QMessageBox.warning(self, string)
        elif type == utils.ERROR:
            QtGui.QMessageBox.critical(self, string)
        else:
            utils.Log.e(DEBUG_TAG, "PromptSlot(), type error!")
    def UpdateWorkState(self, type):
        self.setIconByState(type)
    def RunButtonClick(self):
        self.WorkThread = WorkThread(0, 0)
        self.WorkThread.signalStartSucceed.connect(self.SuccessStartedSlot)
        self.WorkThread.signalPromptMsg[int, str].connect(self.PromptSlot)
        self.WorkThread.signalWorkState[int].connect(self.UpdateWorkState)
        self.WorkThread.start()
    def StopButtonClick(self):
        self.WorkThread.stop()
        for key in self.Checkboxes:
            self.Checkboxes[key].setEnabled(True)
        self.RunButton.setEnabled(True)
        self.StopButton.setEnabled(False)
    def settingButtonClick(self):
        self.configPage = ConfigInfoPage(False)
        self.configPage.exec_()
    def historyButtonClick(self):
        self.historyPage = HistoryPageWindow()
        self.historyPage.show()
    def PopCheckboxToggle(self, visible):
        transfer.set_run_config('pop', visible)
    def BackupCheckboxToggle(self, visible):
        transfer.set_run_config('backup', visible)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.Checkboxes['pop'].setText(_translate("Dialog", "Pop Window", None))
        self.Checkboxes['backup'].setText(_translate("Dialog", "Backup Mode", None))
        self.RunButton.setText(_translate("Dialog", "Run", None))
        self.StopButton.setText(_translate("Dialog", "Stop", None))
    def setVisible(self, visible):
        self.minimizeAction.setEnabled(visible)
        self.maximizeAction.setEnabled(not self.isMaximized())
        self.restoreAction.setEnabled(self.isMaximized() or not visible)
        super(MainWindow, self).setVisible(visible)

    def closeEvent(self, event):
        if self.trayIcon.isVisible():
#            QtGui.QMessageBox.information(self, "Systray",
#                    "The program will keep running in the system tray. To "
#                    "terminate the program, choose <b>Quit</b> in the "
#                    "context menu of the system tray entry.")
            self.setVisible(False)
            event.ignore()
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange and self.isMinimized():
            self.setWindowFlags(QtCore.Qt.Tool)
            super(MainWindow, self).setVisible(False)
            event.ignore()
        if event.type() == QtCore.QEvent.WindowStateChange and self.isWindow():
            self.setWindowFlags(QtCore.Qt.Window)
    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.showNormal()

    def showMessage(self):
        icon = QtGui.QSystemTrayIcon.MessageIcon(
                self.typeComboBox.itemData(self.typeComboBox.currentIndex()))
        self.trayIcon.showMessage(self.titleEdit.text(),
                self.bodyEdit.toPlainText(), icon,
                self.durationSpinBox.value() * 1000)

    def messageClicked(self):
        QtGui.QMessageBox.information(None, "Systray",
                "Sorry, I already gave what help I could.\nMaybe you should "
                "try asking a human?")


    def createActions(self):
        self.minimizeAction = QtGui.QAction("Mi&nimize", self,
                triggered=self.hide)

        self.maximizeAction = QtGui.QAction("Ma&ximize", self,
                triggered=self.showMaximized)

        self.restoreAction = QtGui.QAction("&Restore", self,
                triggered=self.showNormal)

        self.quitAction = QtGui.QAction("&Quit", self,
                triggered=QtGui.qApp.quit)

    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
    def createThreadWidget(self):
        self.threadWidget = []
        temp = {}
        temp['widget'] = QtGui.QWidget(self)
        temp['widget'].setGeometry(QtCore.QRect(50, 180, 161, 70))
        temp['layout'] = QtGui.QGridLayout(temp['widget'])
        temp['layout'].setSpacing(10)
        for i in range(3):
            temp['lable'] = QtGui.QLabel("Thread %d"%(i+1))
            temp['layout'].addWidget(temp['lable'], i, 0)
            temp['status'] = QtGui.QLabel("Free...")
            temp['layout'].addWidget(temp['status'], i, 1)
            self.threadWidget.append(temp)
    def createFunctionButton(self):
        self.threadWidget = []
        temp = {}
        temp['widget'] = QtGui.QWidget(self)
        temp['widget'].setGeometry(QtCore.QRect(50, 180, 180, 300))
        temp['layout'] = QtGui.QGridLayout(temp['widget'])
        temp['layout'].setSpacing(10)
        temp['lable'] = QtGui.QLabel("Setting")
        self.threadWidget.append(temp)
