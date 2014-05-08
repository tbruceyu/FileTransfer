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

    def createLogWindow(self):
        groupBox = QtGui.QGroupBox("Logs")
        self.LogView = QtGui.QTextEdit()
        self.LogView.setEnabled(False)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.LogView)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox
    def createRightWindow(self):
        groupBox = QtGui.QGroupBox()
        settingWidget = QtGui.QWidget()
        rightLayout = QtGui.QVBoxLayout()
        self.runSettingLayout = QtGui.QVBoxLayout()
        self.runSettingLayout.setMargin(0)
        self.Checkboxes = {'pop' : QtGui.QCheckBox(),
                          'backup' : QtGui.QCheckBox(),
                          }
        self.Checkboxes['pop'].setChecked(transfer.RUN_CONFIG['pop'])
        self.Checkboxes['backup'].setChecked(transfer.RUN_CONFIG['backup'])
        self.runSettingLayout.addWidget(self.Checkboxes['pop'])
        self.runSettingLayout.addWidget(self.Checkboxes['backup'])
        settingWidget.setLayout(self.runSettingLayout)
        
        actionWidget = QtGui.QWidget()
        self.actionLayout = QtGui.QHBoxLayout()
        self.actionLayout.setMargin(0)
        self.RunButton = QtGui.QPushButton()
        self.RunButton.setObjectName('ActionButton')
        self.actionLayout.addWidget(self.RunButton)
        self.StopButton = QtGui.QPushButton()
        self.StopButton.setObjectName('ActionButton')
        self.actionLayout.addWidget(self.StopButton)
        actionWidget.setLayout(self.actionLayout)
        functionWidget = self.createFunctionButton()
        rightLayout.setAlignment(QtCore.Qt.AlignTop)
        rightLayout.setMargin(20)
        rightLayout.setSpacing(10)
        #rightLayout.addStretch(1)
        rightLayout.addWidget(functionWidget)
        rightLayout.addWidget(settingWidget)
        rightLayout.addWidget(actionWidget)
        groupBox.setLayout(rightLayout)
        return groupBox
    def setUI(self):
        #palette =  QtGui.QPalette();
        #palette.setColor(QtGui.QPalette.Background, QtGui.QColor(192,253,123))
        #palette.setBrush(QPalette::Background, QBrush(QPixmap(":/background.png")));
        #self.setPalette(palette)
        #splitter = QtGui.QSplitter(self)
        self.createActions()
        self.createTrayIcon()
        qss_file = open('../../styles/common.qss').read()
        self.setStyleSheet(qss_file)
        self.setFixedSize(400, 400)
        mainLayout = QtGui.QVBoxLayout()
        topWidget = QtGui.QWidget()
        topLayout = QtGui.QHBoxLayout()
        logWidget = self.createLogWindow()

        threadWidget = self.createThreadWidget()
        rightWidget = self.createRightWindow()
        topLayout.addWidget(threadWidget)
        topLayout.addWidget(rightWidget)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        topWidget.setLayout(topLayout)
        mainLayout.addWidget(topWidget)
        mainLayout.addWidget(logWidget)
        self.setLayout(mainLayout)
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
        groupBox = QtGui.QGroupBox("Thread pools")
        temp = {}
        temp['layout'] = QtGui.QGridLayout()
        temp['layout'].setSpacing(10)
        for i in range(3):
            temp['lable'] = QtGui.QLabel("Thread %d"%(i+1))
            temp['layout'].addWidget(temp['lable'], i, 0)
            temp['status'] = QtGui.QLabel("Free...")
            temp['layout'].addWidget(temp['status'], i, 1)
        groupBox.setLayout(temp['layout'])
        return groupBox
    def createFunctionButton(self):
        groupBox = QtGui.QGroupBox()
        layout = QtGui.QGridLayout()
        self.settingButton = QtGui.QPushButton()
        self.settingButton.setObjectName("settingButton")
        self.settingButton.setText("Settings")
        self.settingButton.setStyleSheet("QPushButton { background: rgb(59, 138, 113);border:none;padding: 3px;} \
                                            QPushButton:hover {background: rgb(165, 165, 113);}")
        self.historyButton = QtGui.QPushButton()
        self.historyButton.setObjectName("settingButton")
        self.historyButton.setText("History")
        self.historyButton.setStyleSheet("QPushButton { background: rgb(59, 138, 113);} \
                                            QPushButton:hover {background: rgb(165, 165, 113);}")
        layout.addWidget(self.settingButton, 0, 0)
        layout.addWidget(self.historyButton, 0, 1)
        groupBox.setLayout(layout)
        groupBox.setStyleSheet("QGroupBox{ border: 0px groove grey; border-radius:5px;border-style: outset;}")
        return groupBox