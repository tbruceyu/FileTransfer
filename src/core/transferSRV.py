import os
import shutil
import threading
import hashlib
import time
import datetime
import string
import subprocess
import ConfigParser
import getpass
import sys
from optparse import OptionParser
from core import common, utils
from core.utils import Log
import stat
from shutil import SpecialFileError
TAG = 'transferSRV'
BLOCK_SIZE = 16*1024
THREAD_NUM = 4
SW_CONFIG = {}
PC_CONFIG = {}
CONFIG_FILE = os.path.join(common.HOME_DIR, 'file_transfer.conf')

class copy_thread(threading.Thread):
    offset = 0
    totalBlock = 0
    doneBlock = 0
    def __init__(self, source_file, offset, size, dest_file):
        threading.Thread.__init__(self, name='copy_thread')
        self.source_file = source_file
        self.dest_file = dest_file
        self.offset = offset
        self.totalBlock = size
    def _samefile(self, src, dst):
        return (os.path.normcase(os.path.abspath(src)) ==
                os.path.normcase(os.path.abspath(dst)))
    def copyfileobj(self, fsrc, fdst):
        """copy data from file-like object fsrc to file-like object fdst"""
        while self.doneBlock < self.totalBlock:
            buf = fsrc.read(BLOCK_SIZE)
            if not buf:
                break
            time.sleep(0.01)
            fdst.write(buf)
            self.doneBlock = self.doneBlock + 1
    def _copy_file(self):
        print self.source_file + ' ----> ' + self.dest_file + '\n'
        file_size = os.path.getsize(self.source_file) / 1024
        start = time.clock()
        if not os.path.isfile(self.source_file):
            return False
        """Copy data from src to dst"""
        if self._samefile(self.source_file, self.dest_file):
            raise EnvironmentError("`%s` and `%s` are the same file" % (self.source_file, self.dest_file))
        for fn in [self.source_file, self.dest_file]:
            try:
                st = os.stat(fn)
            except OSError:
                # File most likely does not exist
                pass
            else:
                # XXX What about other special files? (sockets, devices...)
                if stat.S_ISFIFO(st.st_mode):
                    raise SpecialFileError("`%s` is a named pipe" % fn)
    
        with open(self.source_file, 'rb') as fsrc:
            print "offset:%d, totalBlock:%d"%(self.offset, self.totalBlock)
            fsrc.seek(self.offset*BLOCK_SIZE, (self.offset + self.totalBlock)*BLOCK_SIZE)
            with open(self.dest_file, 'wb') as fdst:
                fdst.seek(self.offset*BLOCK_SIZE, (self.offset + self.totalBlock)*BLOCK_SIZE)
                self.copyfileobj(fsrc, fdst)
        elapsed = (time.clock() - start)
        print 'Time used for copy ' + self.dest_file + ': %f' % elapsed + ', Speed:%f' % (file_size / elapsed) + 'kb/s\n'

    def run(self):
        self._copy_file()
        #os.remove(self.source_file)
    def getdoneBlock(self):
        return self.doneBlock

def GetPathSize(strPath):
    if not os.path.exists(strPath):
        return 0;

    if os.path.isfile(strPath):
        return os.path.getsize(strPath);

    nTotalSize = 0;
    for strRoot, lsDir, lsFiles in os.walk(strPath):
        #get child directory size
        for strDir in lsDir:
            nTotalSize = nTotalSize + GetPathSize(os.path.join(strRoot, strDir));

        #for child file size
        for strFile in lsFiles:
            nTotalSize = nTotalSize + os.path.getsize(os.path.join(strRoot, strFile));
    return nTotalSize

def compress_file(source_file, dest_file):
    start = time.clock()
    file_size = GetPathSize(source_file)
    if file_size == 0:
        print 'You input a null file or folder, exit...'
        os.system('pause')
        exit(1)
    #command = ''C:\\Program Files\\7-Zip\\7z' a -tzip -v%d ''%part_size+dest_file+'\' ''+source_file+'''
    command = '"'+SW_CONFIG['7zpath']+'" a -tzip "'+dest_file+'\" "'+source_file+'"'
    print command
    ps = subprocess.Popen(command)
    ps.wait()
    elapsed = (time.clock() - start)
    utils.Log.d(TAG, 'Time used for compress ' + dest_file + ': %f' % elapsed + ', Speed:%f' % (file_size / 1024 / elapsed) + 'kb/s\n')
def get_file_list(dir, rand_name):
    file_list = []
    for file in os.listdir(dir):
        if (file.startswith(rand_name)):
            print file
            file_list.append(file)
    return file_list
def multi_thread_send(source_file, dest_path):
    i = 0
    threadNum = THREAD_NUM
    file_size = GetPathSize(source_file)
    if file_size < 4*BLOCK_SIZE:
        threadNum = 1
    threads = range(0, threadNum)
    fileBlock = os.path.getsize(source_file)/BLOCK_SIZE
    partBlock = fileBlock/4
    offsetBlock = 0
    #first three threads transaction
    if threadNum > 1:
        for i in range(0, len(threads)):
            dest_temp = "%s"%(os.path.join(dest_path, os.path.basename(source_file)))
            tempBlockLen = partBlock
            if i == (len(threads) - 1):
                tempBlockLen = fileBlock - offsetBlock + 1
            threads[i] = copy_thread(source_file, offsetBlock, tempBlockLen, dest_temp)
            offsetBlock += tempBlockLen
            threads[i].setDaemon(True)
            threads[i].start()
    else:
        dest_temp = "%s"%(os.path.join(dest_path, os.path.basename(source_file)))
        threads[i] = copy_thread(source_file, offsetBlock, fileBlock - offsetBlock + 1, dest_temp)
        threads[i].setDaemon(True)
        threads[i].start()
    while True:
        copyBlock = 0
        alive = False
        for i in range(0, len(threads)):
            copyBlock = copyBlock + threads[i].getdoneBlock()
            alive = alive or threads[i].isAlive()
        if not alive:
            break
        time.sleep(0.1)
        #print the percent
        if fileBlock > 0:
            sys.stdout.write("\r%d%%" %((copyBlock*100/fileBlock)))
def write_signal_file(time_name, file_name):
    try:
        fp = open(os.path.join(os.path.join(SW_CONFIG['sharefolder'], time_name), time_name + '.sig'), 'w')
        cf = ConfigParser.ConfigParser()
        cf.add_section('information')
        cf.set('information', 'file_name', file_name)
        if SW_CONFIG['exec_command'] != None:
            cf.set('information', 'execute_command', SW_CONFIG['exec_command'])
        cf.write(fp)
        fp.close()
    except IOError:
        print "Can't create signal file!"

def make_file_dir(file_name):
    if not os.path.exists(os.path.join(SW_CONFIG['sharefolder'], file_name)):
        try:
            os.makedirs(os.path.join(SW_CONFIG['sharefolder'], file_name))
        except IOError:
            print "can't create the file's folder!"
            os.system('pause')
            exit(1)
def init():
    if not os.path.exists(SW_CONFIG['compress_dir']):
        try:
            os.makedirs(SW_CONFIG['compress_dir'])
        except os.error:
            print "Can't create the temp compress folder:" + SW_CONFIG['compress_dir'] + ", Please set another one"
            clean()
            os.system('pause')
            exit(1)
    if not os.path.exists(SW_CONFIG['sharefolder']):
        try:
            os.makedirs(SW_CONFIG['sharefolder'])
        except os.error:
            print "Can't create the share folder:" + SW_CONFIG['sharefolder'] + " temp directory!"
            clean()
            os.system('pause')
            exit(1)
def clean():
    print 'delete config file...'
    os.remove(CONFIG_FILE)
def init_config():
    SW_CONFIG['compress_dir'] = 'D:\\User\\' + common.USER_NAME + '\\compress_temp'
    SW_CONFIG['sharefolder'] = common.getSharefolder()
    SW_CONFIG['7zpath'] = common.get7zPath(True)
    while True:
        cf = ConfigParser.ConfigParser()
        if not os.path.exists(CONFIG_FILE):
            # init 7z tool
            temp = SW_CONFIG['7zpath']
            while not os.path.isfile(temp):
                print "can't find 7z.exe in 'C:\\Program Files\\7-Zip\\' and 'C:\\Program Files (x86)\\7-Zip\\'"
                temp = raw_input('please input your 7z.exe path:')
            SW_CONFIG['7zpath'] = temp
            cf.add_section('dir_config')
            SW_CONFIG['7zpath'] = SW_CONFIG['7zpath'].strip('\'')
            SW_CONFIG['sharefolder'] = SW_CONFIG['sharefolder'].strip('\'')
            cf.set('dir_config', 'compress_dir', SW_CONFIG['compress_dir'])
            cf.set('dir_config', 'sharefolder', SW_CONFIG['sharefolder'])
            cf.set('dir_config', '7zpath', SW_CONFIG['7zpath'])
            fp = open(CONFIG_FILE, 'w')
            cf.write(fp)
            fp.close()
            pcConfigFile = os.path.join(SW_CONFIG['sharefolder'], 'pc.conf')
            #if this share folder never configured, we can't use
            if os.path.isfile(pcConfigFile):
                clean()
                continue
        else:
            try :
                cf.read(CONFIG_FILE)
                SW_CONFIG['compress_dir'] = cf.get('dir_config', 'compress_dir')
                SW_CONFIG['sharefolder'] = cf.get('dir_config', 'sharefolder')
                SW_CONFIG['7zpath'] = cf.get('dir_config', '7zpath')
                break
            except ConfigParser.Error:
                print 'Config file parse error!'
                clean()
def start(file_path, execCommand = None):
    SW_CONFIG['exec_command'] = execCommand
    time_name = time.strftime(os.path.basename(file_path)+" %Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
    compress_file(file_path, os.path.join(SW_CONFIG['compress_dir'], time_name))
    make_file_dir(time_name)
    multi_thread_send(os.path.join(SW_CONFIG['compress_dir'], time_name), os.path.join(SW_CONFIG['sharefolder'], time_name))
    write_signal_file(time_name, os.path.basename(file_path))
    print "END!!"