from PyQt4.QtGui import *
from PyQt4.QtCore import *

from core import transferPC, common
from UI.FaderWidget import FaderWidget
class MainConfigurePage(QDialog):
    def __init__(self,parent=None):
        super(MainConfigurePage,self).__init__(parent)
        self.setWindowTitle(self.tr("Preferences"))

        mainSplitter=QSplitter(Qt.Horizontal)
        mainSplitter.setOpaqueResize(True)

        self.listWidget=QListWidget(mainSplitter)
        self.listWidget.insertItem(0,self.tr("General"))
        self.listWidget.insertItem(1,self.tr("Hook commands"))
        self.listWidget.insertItem(2,self.tr("Console"))

        frame=QFrame(mainSplitter)
        splitterHandle = mainSplitter.handle(1)
        splitterHandle.setDisabled(True)
        self.stack=QStackedWidget()
        mainSplitter.setStretchFactor(0, 4)
        mainSplitter.setStretchFactor(1, 8)
        self.stack.setFrameStyle(QFrame.Panel|QFrame.Raised)

        pathInfo=PathInfoPage()
        contact=HookConfigPage()
        self.stack.addWidget(pathInfo)
        self.stack.addWidget(contact)

        amendPushButton=QPushButton(self.tr("Save"))
        closePushButton=QPushButton(self.tr("Cancel"))

        buttonLayout=QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(amendPushButton)
        buttonLayout.addWidget(closePushButton)

        mainLayout=QVBoxLayout(frame)
        mainLayout.setMargin(10)
        mainLayout.setSpacing(6)
        mainLayout.addWidget(self.stack)
        mainLayout.addLayout(buttonLayout)

        self.connect(self.listWidget,SIGNAL("currentRowChanged(int)"),self.stack,SLOT("setCurrentIndex(int)"))
        self.connect(closePushButton,SIGNAL("clicked()"),self,SLOT("close()"))

        layout=QHBoxLayout(self)
        layout.addWidget(mainSplitter)
        self.setLayout(layout)
        #-----------------------
        self.faderWidget=None
        self.connect(self.listWidget,SIGNAL("currentItemChanged(QListWidgetItem,QListWidgetItem"),
                     self.changePage)
        self.connect(self.stack,SIGNAL("currentChanged(int)"),self.fadeInWidget)
    def changePage(self,current,previous):
        if not current:
            current=previous
        self.stack.setCurrentWidget(current)
    def fadeInWidget(self,index):
        self.faderWidget=FaderWidget(self.stack.widget(index))
        self.faderWidget.start()

class HookConfigPage(QWidget):
    def __init__(self,parent=None):
        super(HookConfigPage,self).__init__(parent)
        self.createGUI()
    def createGUI(self):
        self.table = QTableWidget(0, 2)
        #self.table.setSelectionBehavior(QAbstractItemView.SelectItems)
        #self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(["FileName", "Command"])
        #self.table.verticalHeader().setVisible(False)
        self.table.resize(400, 300)
        self.table.resizeColumnToContents(0)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        data = {'name':"dsfl", 'date' : "dslfkj"}
        self.addRow(data)
        layout = QGridLayout()
        layout.addWidget(self.table, 0, 0)
        self.setLayout(layout)

        self.setWindowTitle("File history")
    def addRow(self, data):
        index = self.table.rowCount()
        self.table.insertRow(index)
        self.table.setItem(index, 0, QTableWidgetItem(data['name']))
        self.table.setItem(index, 1, QTableWidgetItem(data['date']))


class PathInfoPage(QDialog):
    def __init__(self, parent=None):
        super(PathInfoPage, self).__init__(parent)
        self.setWindowTitle("Configuration")
        self.compressPathLable = QLabel("7z.exe path:")
        self.compressPathLable.setFixedSize(80, 20)
        self.compressPathComboBox = self.createComboBox(common.get7zPath())
        self.compressPathComboBox.setFixedSize(300, 20)
        self.compressPathLable.setBuddy(self.compressPathComboBox)
        self.compressButton = QPushButton("...")
        self.compressButton.setFixedSize(30, 20)
        self.compressButton.clicked.connect(self.set7zPath)
        self.shareFolderLable = QLabel("Share folder:")
        self.shareFolderComboBox = self.createComboBox(common.getSharefolders())
        self.shareFolderButton = QPushButton("...")
        self.shareFolderButton.setFixedSize(30, 20)
        self.shareFolderButton.clicked.connect(self.setShareFolder)
        self.shareFolderLable.setBuddy(self.shareFolderComboBox)
        
        self.distFolderLable = QLabel("Dist folder:")
        self.distFolderComboBox = self.createComboBox(transferPC.getDistPath())
        self.distFolderButton = QPushButton("...")
        self.distFolderButton.setFixedSize(30, 20)
        self.distFolderButton.clicked.connect(self.setDistFolder)
        self.distFolderLable.setBuddy(self.distFolderComboBox)
        self.startupCheckBox = QCheckBox("Startup when powerup")
        self.startupCheckBox.setChecked(True)
        self.startupCheckBox.toggled.connect(self.startupToggled)

        #self.registerField('7z.exe*', self.compressPathComboBox)
        layout = QGridLayout()
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
#        if not self.firstRun:
#            self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
#            self.buttonBox.accepted.connect(self.accept)
#            self.buttonBox.rejected.connect(self.reject)
#            layout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.setLayout(layout)
    def createComboBox(self, path_list=[]):
        comboBox = QComboBox()
        comboBox.setEditable(False)
        for path in path_list:
            comboBox.addItem(path)
        comboBox.setSizePolicy(QSizePolicy.Expanding,
                QSizePolicy.Preferred)
        return comboBox
    def set7zPath(self):
        filename = QFileDialog.getOpenFileName(self,
                "set7zPath",
                self.compressPathComboBox.currentText(),
                "Executable (7z.exe)", None, QFileDialog.Options()
                )
        filename = filename.replace('/', '\\')
        if filename:
            self.compressPathComboBox.insertItem(0, filename)
            self.compressPathComboBox.setCurrentIndex(0)
    def setShareFolder(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                "setShareFolder",
                self.shareFolderComboBox.currentText(), options)
        if directory:
            self.shareFolderComboBox.insertItem(0, directory)
            self.shareFolderComboBox.setCurrentIndex(0)
    def setDistFolder(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
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
            super(PathInfoPage, self).accept()
        else:
            QMessageBox.critical(self, "Config Invalid!",
                    "Please check the configuration items and try again!! ")
class ConfigInfoWizardPage(QWizardPage, PathInfoPage):
    def __init__(self, parent=None):
        super(ConfigInfoWizardPage, self).__init__(parent)
        self.setTitle("Configuration")
        self.setSubTitle("This is your first time run this tool. "
                "Please complete the following configration")
    def show(self):
        self.configPage.show()