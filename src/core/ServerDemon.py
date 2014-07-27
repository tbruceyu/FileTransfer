from PyQt4 import QtCore
import win32pipe, win32file
'''
main task thread. receive the file transfer message from the client of self
'''
from core.common import *
import threading
import mmap
import os
from core import common
MMAP_FOLDER = "D:\\User"
class Message():
    id = 0
    target = ""
    type = ""
    action = ""
    data = ""
class fileStruct():
    md5 = ""
    name = ""
    state = ""
class ClientHandler():
    def __init__(self, clientName):
        # The client name
        self.name = clientName
        # The files for processing
        self.fileMap = {}
    def processMsg(self, message):
        if message.action == "send.start":
            print "send file!"
        elif message.action == "send.progress":
            print "progress"
        elif message.action == "send.success":
            print "success"
class MainTaskThread(QtCore.QThread):
    stopped = False
    def __init__(self, team):
        super(MainTaskThread, self).__init__(None)
        self.clientReadThreads = self.genClientReadThreads(team)
        self.team = team
    def genClientReadThreads(self, team):
        dir = os.path.join(common.SHARE_FOLDER, team)
        threads = {}
        i = 0
        for path in os.listdir(dir):
            print path
            if os.path.isdir(os.path.join(dir, path)):
                user = os.path.basename(path)
                print user
                threads[user] = ClientReadThread(user)
                i = i + 1
        return threads
    def run(self):
        # just reading the file transfer request from the client(self user)
        try:
            self.pipeHandle = win32pipe.CreateNamedPipe(r'\\.\pipe\%s'%common.USER_NAME,
                    win32pipe.PIPE_ACCESS_DUPLEX,
                    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
                    1, 65536, 65536,300,None)
        except Exception as e:
            print e
        win32pipe.ConnectNamedPipe(self.pipeHandle, None)
        for (name, thread) in self.clientReadThreads.items():
            print "start task!"
            thread.start()
        while not self.stopped:
            data = win32file.ReadFile(self.pipeHandle, 4096)
            print data
class ClientReadThread(threading.Thread):
    stopped = False
    def __init__(self, user):
        threading.Thread.__init__(self, name = "ClientReadThread")
        mmapFile = os.path.join(MMAP_FOLDER, user+".mmap")
        # make sure there is a mmap file
        self.mmap_fp = open(mmapFile, 'w+')
        self.__mmap_fd = 0
        try :
            self.__mmap_fd = mmap.mmap(self.mmap_fp.fileno(), 1024, access=mmap.ACCESS_WRITE)
        except Exception as e:
            print "heheh"+str(e)
        self.__clientUser = os.path.splitext(os.path.basename(mmapFile))[0] 
        self.__stopped = False
        self.__handler = ClientHandler(user)
    def __parse(self, stringMessage):
        message = Message()
        messageList = stringMessage.split('|')
        message.id = messageList[0]
        message.target = messageList[1]
        message.type = messageList[2]
        message.action = messageList[3]
        message.data = messageList[4]
    def __validMessage(self, message):
        if message.target.upper() == "ALL":
            return True
        if message.target.upper() == USER_NAME.upper():
            return True
        return False
    def run(self):
        line = ""
        last_line = ""
        while not self.stopped:
            line = self.__mmap_fd.readline()
            if line == last_line:
                continue
            elif line[0] == chr(0):
                print "null!"
                continue
            message = self.__parse(line)
            if self.__validMessage(message):
                print "start process message"
        self.mmap_fp.close()
    def stop(self):
        self.stopped = True










