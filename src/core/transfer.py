#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The most important operations of files

import os
import time
import subprocess
import ConfigParser
import getpass
import threading
from core.utils import Log
from PyQt4.QtCore import pyqtSignal
from PyQt4 import QtCore
from core import utils, common
import Queue
from pprint import pprint 

DEBUG_TAG = "transfer"
TAG = DEBUG_TAG
SW_CONFIG = {}
RUN_CONFIG = {}
USER_NAME = getpass.getuser()
HOME_DIR = os.path.expanduser("~")
CONFIG_FILE = os.path.join(HOME_DIR, "file_transfer.conf")
TEAMS = ['Marine', 'Outdoor', 'Platform_Support', 'PND']
def getSharefolder():
    return ["C:\\Program Files\\7-Zip\\"]
    temp_folders = []
    real_temp_path = ""
    for team_name in TEAMS :
        team_path = os.path.join(SHARE_FOLDER, team_name)
        team_members = os.listdir(team_path)
        for name in team_members:
            if USER_NAME.lower().find(name.lower()) != -1 :
                temp_folders.append(os.path.join(team_path, name))
    return temp_folders
def get7zPath():
    return ['C:\\']
    path = []
    temp = 'C:\\Program Files (x86)\\7-Zip\\7z.exe'
    if os.path.isfile(temp):
        path.append(temp)
    temp = 'C:\\Program Files\\7-Zip\\7z.exe'
    if os.path.isfile(temp):
        path.append(temp)
    return path
def getDistPath():
    return ['D:\\']
def find_compress_tool():
    # init 7z tool
    if not os.path.isfile(COMPRESS_TOOL):
        COMPRESS_TOOL = "C:\\Program Files (x86)\\7-Zip\\7z.exe"
    if not os.path.isfile(COMPRESS_TOOL):
        print "can't find 7z.exe in 'C:\\Program Files\\7-Zip\\' and 'C:\\Program Files (x86)\\7-Zip\\'"
        COMPRESS_TOOL = raw_input("please input your 7z.exe path:")
def config_file_exist():
    return os.path.exists(CONFIG_FILE)
def set_config(doname, key, value):
    cf = ConfigParser.ConfigParser()
    cf.set("dir_config", "LOCAL_DIR", LOCAL_DIR)
def checkConfigValid(config):
    if not os.path.isfile(config['7zpath']):
        return False
    if not os.path.isdir(config['sharefolder']):
        return False
    if not os.path.isdir(config['distpath']):
        return False
    return True
def saveConfig(config):
    """
    Save the specified configuration dict to the disk file 
    """
    global SW_CONFIG
    cf = ConfigParser.ConfigParser()
    cf.add_section("dir_config")
    cf.set("dir_config", "7zpath", config['7zpath'])
    cf.set("dir_config", "sharefolder", config['sharefolder'])
    cf.set("dir_config", "distpath", config['distpath'])
    cf.add_section("sw_config")
    cf.set("sw_config", "version", config['sw_version'])
    cf.set("sw_config", "startup", config['startup'])
    cf.add_section("run_config")
    cf.set("run_config", "pop", False)
    cf.set("run_config", "backup", False)
    fp = open(CONFIG_FILE, "w")
    cf.write(fp)
    fp.close()
    SW_CONFIG = config
def saveCurrentConfig():
    """
    Save all of the current configurations to the disk file
    """
    cf = ConfigParser.ConfigParser()
    cf.add_section("dir_config")
    cf.set("dir_config", "7zpath", SW_CONFIG['7zpath'])
    cf.set("dir_config", "sharefolder", SW_CONFIG['sharefolder'])
    cf.set("dir_config", "distpath", SW_CONFIG['distpath'])
    cf.add_section("sw_config")
    cf.set("sw_config", "version", SW_CONFIG['sw_version'])
    cf.set("sw_config", "startup", SW_CONFIG['startup'])
    cf.add_section("run_config")
    pprint(RUN_CONFIG)
    cf.set("run_config", "pop", RUN_CONFIG['pop'])
    cf.set("run_config", "backup", RUN_CONFIG['backup'])
    fp = open(CONFIG_FILE, "w")
    cf.write(fp)
    fp.close()
def set_run_config(key, value):
    """
    general run configuration method
    """
    print key
    RUN_CONFIG[key] = value
    pprint(RUN_CONFIG)
def init_config():
    """
    Initiliaze all of the software configurations
    """
    global SHARE_FOLDER
    global LOCAL_DIR
    global CONFIG_FILE
    global COMPRESS_TOOL
    global DEFAULT_LOCAL_DIR
    cf = ConfigParser.ConfigParser()
    try :
        cf.read(CONFIG_FILE)
    except os.errno:
        Log.e(TAG, "Open configuration file error!")
        return False
    try :
        SW_CONFIG['7zpath'] = cf.get("dir_config", "7zpath")
        SW_CONFIG['sharefolder'] = cf.get("dir_config", "sharefolder")
        SW_CONFIG['distpath'] = cf.get("dir_config", "distpath")
        SW_CONFIG['sw_version'] = cf.get("sw_config", "version")
        SW_CONFIG['startup'] = cf.get("sw_config", "startup")
    except ConfigParser.Error:
        Log.e(DEBUG_TAG, "Config file parse error!")
        clean()
        return False
    try :
        RUN_CONFIG['backup'] = (cf.get("run_config", "backup") == "True")
        RUN_CONFIG['pop'] = (cf.get("run_config", "pop") == "True")
    except ConfigParser.Error:
        Log.e(TAG, "no run config in config file!")
        RUN_CONFIG['backup'] = False
        RUN_CONFIG['pop'] = False
    if not os.path.exists(SW_CONFIG['sharefolder']):
        try:
            os.makedirs(SW_CONFIG['sharefolder'])
        except os.error:
            print "Can't create the local folder:" + LOCAL_DIR + ", Please set another one"
            clean()
            exit()
    if not os.path.exists(SW_CONFIG['distpath']):
        try:
            os.makedirs(SW_CONFIG['distpath'])
        except os.error:
            print "Can't create the share folder:" + SHARE_FOLDER + " temp directory!"
            clean()
            os.system("pause")
            exit()
    return True
def init():
    """ 
    Module initiliaze
    """
    init_config()

def clean():
    """ 
    Delete the config file
    """
    Log.d(DEBUG_TAG, "Delete config file...")
    try:
        os.remove(CONFIG_FILE)
    except os.error as e:
        Log.e(DEBUG_TAG, "Delete config file%s error, reason:%s"%(CONFIG_FILE, e))

def start(silence, backup):
    WorkThread(silence, backup)

class HistoryThread(QtCore.QThread):
    """ 
    History page work thread
    """
    signalCallback = pyqtSignal(dict)
    def __init__(self):
        super(HistoryThread, self).__init__(None)
    def run(self):
        self.data = []
        i = 0
        for dir in os.listdir(SW_CONFIG['sharefolder']):
            i = i + 1
            temp = {}
            temp['id'] = i
            temp['name'] = dir
            temp['path'] = os.path.join(SW_CONFIG['sharefolder'], dir)
            temp['date'] = ""
            temp['comment'] = "comment"
            self.data.append(temp)
            self.signalCallback.emit(temp)
class WorkThread(QtCore.QThread):
    """
    Worker thread class
    """
    signalStartSucceed = pyqtSignal() #声明信号
    signalPromptMsg = pyqtSignal([int, str])
    signalWorkState = pyqtSignal(int)
    stopped = False
    runConfig = {'silence' : False, 'backup' : False}
    def __init__(self, silence, backup):
        super(WorkThread, self).__init__(None)
        self.processThreadPool = self.threadPoolWorkThread(3)
        self.silence = silence
        self.backup = backup
    def run(self):
        self.signalStartSucceed.emit()
        saveCurrentConfig()
        #self.signalPromptMsg.emit(1, "hehe")
        self.start_(self.silence, self.backup)
    def start_(self, silence, backup):
        self.runConfig['silence'] = silence
        self.runConfig['backup'] = backup
        self.stopped = False
        try:
            self.watch_dir()
        except KeyboardInterrupt:
            import sys
            sys.exit()
    def watch_dir(self):
        old_list = os.listdir(SW_CONFIG['sharefolder'])
        print "Watching %s" % SW_CONFIG['sharefolder']
        self.signalWorkState.emit(utils.WATCHING)
        while 1 and not self.stopped:
            new_list = os.listdir(SW_CONFIG['sharefolder'])
            sub_list = list(set(new_list) - set(old_list))
            if len(sub_list) > 0:
                print "Create a daemon thread watching '%s'" % os.path.join(SW_CONFIG['sharefolder'], sub_list[0])
                self.processThreadPool.add_job(sub_list[0])
                # reset the lists
                old_list = os.listdir(SW_CONFIG['sharefolder'])
                new_list = old_list
            old_list = new_list
            time.sleep(2)
    def stop(self):
        self.stopped = True
        self.processThreadPool.stop()
        self.signalWorkState.emit(utils.STOPPED)
    class threadPoolWorkThread(threading.Thread):
        """
        The thread pool for waiting/process file
        """
        workQueue = Queue.Queue()
        resultQueue = Queue.Queue()
        def __init__( self, num_of_threads=5):
            threading.Thread.__init__(self, name="threadPoolWorkThread")
            self.threads = []
            self.__createThreadPool( num_of_threads )
            self.start()
        def run(self):
            self.wait_for_complete()
        def __createThreadPool( self, num_of_threads ):
            for i in range( num_of_threads ):
                thread = self.processThread(i+1, self.workQueue)
                self.threads.append(thread)

        def wait_for_complete(self):
            #Check all threads
            Log.d(TAG, "start join thread")
            for thread in self.threads:
                if thread.isAlive(): #if the thread is alive
                    thread.join()
            Log.d(TAG, "end join thread...")
        def add_job( self, wait_path ):
            self.workQueue.put( wait_path )
        def stop(self):
            for thread in self.threads:
                if thread.isAlive():
                    thread.stop()
                    thread.join()
                    print "thread alive: %d"%thread.isAlive()
        class processThread(utils.ThreadWithExc):
            """
            The work thread implementation
            """
            stopped = False
            def __init__(self, number, workQueue):
                self.workQueue = workQueue
                self.number = number
                self.stopped = False
                threading.Thread.__init__(self, name="process thread")
                self.start()
            def run(self):
                print "Thread %d start!!"%self.number
                try:
                    while not self.stopped:
                        # wait for signal file written
                        try:
                            wait_path = self.workQueue.get(timeout = 0.5)
                            signal_conf = self.wait_for_signal(wait_path)
                            # extract file
                            target_dir = self.extract_file(self.wait_dir, signal_conf.file_name)
                            if SW_CONFIG['silence'] == False:
                                os.startfile(target_dir)
                            self.execute_command(target_dir, signal_conf)
                        except Queue.Empty:
                            continue
                except SystemExit:
                    print "hdfsldfjlsdfjlk"
            def execute_command(self, target_dir, signal_conf):
                if signal_conf.execute_command == "":
                    return
                for command in signal_conf.execute_command.split(';'):
                    target_file = os.path.join(target_dir, signal_conf.file_name)
                    if command.find("%s") != -1:
                        command = command % target_file
                    print command
                    ps = subprocess.Popen(command)
                    ps.wait()
            def wait_for_signal(self,dir_name):
                print "wait for signal file....."
                dest_folder = os.path.join(SW_CONFIG['sharefolder'], dir_name)
                signal_path = os.path.join(dest_folder, dir_name + common.SIGNAL_FILE_SUFFIX)
                cf = ConfigParser.ConfigParser()
                signal_conf = {common.SIGNAL_FILE_NAME : None, common.SIGNAL_EXECUTE_COMMAND : None }

                while not self.stopped and signal_conf[common.SIGNAL_FILE_NAME] == None:
                    print signal_conf[common.SIGNAL_FILE_NAME]
                    try:
                        cf.read(signal_path)
                        signal_conf['file_name'] = cf.get("information", "file_name")
                        break
                    except ConfigParser.Error:
                        time.sleep(2)
                if self.stopped:
                    return
                try :
                    signal_conf['execute_command'] = cf.get("information", "execute_command")
                except ConfigParser.Error:
                    signal_conf.execute_command = ""
                return signal_conf
            def extract_file(self, sub_file, signal_file_name):
                file_dir = sub_file
                file_name = file_dir + ".7z.001"
                if SW_CONFIG['backup'] == True:
                    local_dir = os.path.join(os.path.join(SW_CONFIG['distpath'], signal_file_name + "_"), file_dir)
                else:
                    local_dir = LOCAL_DIR
                file_path = os.path.join(os.path.join(SW_CONFIG['sharefolder'], file_dir), file_name)
                command = '"%s" x -o"' % SW_CONFIG['7zpath'] + local_dir + '" "' + file_path + '" -y'
                print command
                ps = subprocess.Popen(command)
                ps.wait()
                print "Complete!!! Please visit '%s'" % local_dir
                return local_dir
            def stop(self):
                self.stopped = True
