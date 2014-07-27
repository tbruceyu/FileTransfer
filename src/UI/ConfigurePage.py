from PyQt4 import QtCore, QtGui
from core import transferPC, common

class ConfigInfoPage(QtGui.QDialog):
    def __init__(self, first, parent=None):
        super(ConfigInfoPage, self).__init__(parent)
        self.setWindowTitle("Configuration")
        self.compressPathLable = QtGui.QLabel("7z.exe path:")
        self.compressPathLable.setFixedSize(80, 20)
        self.compressPathComboBox = self.createComboBox(common.get7zPath())
        self.compressPathComboBox.setFixedSize(300, 20)
        self.compressPathLable.setBuddy(self.compressPathComboBox)
        self.compressButton = QtGui.QPushButton("...")
        self.compressButton.setFixedSize(30, 20)
        self.compressButton.clicked.connect(self.set7zPath)
        self.shareFolderLable = QtGui.QLabel("Share folder:")
        self.shareFolderComboBox = self.createComboBox(common.getSharefolders())
        self.shareFolderButton = QtGui.QPushButton("...")
        self.shareFolderButton.setFixedSize(30, 20)
        self.shareFolderButton.clicked.connect(self.setShareFolder)
        self.shareFolderLable.setBuddy(self.shareFolderComboBox)
        
        self.distFolderLable = QtGui.QLabel("Dist folder:")
        self.distFolderComboBox = self.createComboBox(transferPC.getDistPath())
        self.distFolderButton = QtGui.QPushButton("...")
        self.distFolderButton.setFixedSize(30, 20)
        self.distFolderButton.clicked.connect(self.setDistFolder)
        self.distFolderLable.setBuddy(self.distFolderComboBox)
        self.startupCheckBox = QtGui.QCheckBox("Startup when powerup")
        self.startupCheckBox.setChecked(True)
        self.startupCheckBox.toggled.connect(self.startupToggled)

        #self.registerField('7z.exe*', self.compressPathComboBox)
        layout = QtGui.QGridLayout()
        layout.setColumnStretch(3,1)
        layout.addWidget(self.compressPathLable, 0, 0)
        layout.addWidget(self.compressPathComboBox, 0, 1)
        layout.addWidget(self.compressButton, 0, 2)
        layout.addWidget(self.shareFolderLable, 1, 0)
        layout.addWidget(self.shareFolderComboBox, 1, 1)
        layout.addWidget(self.shareFolderButton, 1, 2)
        layout.addWidget(self.distFolderLable, 2, 0)
        layout.addWidget(self.distFolderComboBox, 2, 1)
        layout.addWidget(self.distFolderButton, 2, 2)
        layout.addWidget(self.startupCheckBox, 4, 0, 1, 2)
        if not first:
            self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)
            layout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.setLayout(layout)
    def createComboBox(self, path_list=[]):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(False)
        for path in path_list:
            comboBox.addItem(path)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Preferred)
        return comboBox
    def set7zPath(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,
                "set7zPath",
                self.compressPathComboBox.currentText(),
                "Executable (7z.exe)", None, QtGui.QFileDialog.Options()
                )
        filename = filename.replace('/', '\\')
        if filename:
            self.compressPathComboBox.insertItem(0, filename)
            self.compressPathComboBox.setCurrentIndex(0)
    def setShareFolder(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                "setShareFolder",
                self.shareFolderComboBox.currentText(), options)
        if directory:
            self.shareFolderComboBox.insertItem(0, directory)
            self.shareFolderComboBox.setCurrentIndex(0)
    def setDistFolder(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                "setShareFolder",
                self.distFolderComboBox.currentText(), options)
        if directory:
            self.distFolderComboBox.insertItem(0, directory)
            self.distFolderComboBox.setCurrentIndex(0)
    def startupToggled(self, visible):
        print visible
    def get7zPath(self):
        return self.compressPathComboBox.currentText()
    def getShareFolder(self):
        return self.shareFolderComboBox.currentText()
    def getDistPath(self):
        return self.distFolderComboBox.currentText()
    def isStartup(self):
        return self.startupCheckBox.isChecked()
    def accept(self):
        config={}
        config['7zpath'] = self.get7zPath()
        config['sharefolder'] = self.getShareFolder()
        config['distpath'] = self.getDistPath()
        config['startup'] = self.isStartup()
        config['sw_version'] = common.Version;
        if transferPC.checkConfigValid(config) :
            transferPC.saveConfig(config)
            super(ConfigInfoPage, self).accept()
        else:
            QtGui.QMessageBox.critical(self, "Config Invalid!",
                    "Please check the configuration items and try again!! ")
class ConfigInfoWizardPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        super(ConfigInfoWizardPage, self).__init__(parent)
        self.configPage = ConfigInfoPage(self, True)
        self.setTitle("Configuration")
        self.setSubTitle("This is your first time run this tool. "
                "Please complete the following configration")