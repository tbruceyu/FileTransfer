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
COMPRESS_TOOL="C:\\Program Files\\7-Zip\\7z.exe"
USER_NAME = getpass.getuser()
COMPRESS_TEMP_DIR = "D:\\Users\\"+USER_NAME+"\\compress_temp"
DEFAULT_COMPRESS_TEMP_DIR = COMPRESS_TEMP_DIR
SHARE_FOLDER = "//c3-se-terminal3/Shared_Folder"
FILE_MULTIPLE = 12
EXECUTE_COMMAND = ""
TEAMS = ['Marine', 'Outdoor', 'Platform_Support', 'PND']
HOME_DIR = os.path.expanduser("~")
CONFIG_FILE = os.path.join(HOME_DIR, "file_transfer.conf")
class copy_thread(threading.Thread):
    def __init__(self, source_file, dest_file):
        threading.Thread.__init__(self, name="copy_thread")
        self.source_file = source_file
        self.dest_file = dest_file
    def run(self):
        copy_file(self.source_file, self.dest_file)
        os.remove(self.source_file)

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
def copy_file(source_file, dest_file):
    print source_file + " ----> " + dest_file + "\n"
    file_size = os.path.getsize(source_file)/1024
    start = time.clock()
    shutil.copy(source_file, dest_file)
    elapsed = (time.clock() - start)
    print "Time used for copy "+dest_file+": %f"%elapsed + ", Speed:%f"%(file_size/elapsed)+"kb/s\n"

def compress_file(source_file, dest_file):
    start = time.clock()
    file_size = GetPathSize(source_file)
    if file_size == 0:
        print "You input a null file or folder, exit..."
        os.system("pause")
        exit(1)
    part_size = file_size/FILE_MULTIPLE
    #command = '"C:\\Program Files\\7-Zip\\7z" a -tzip -v%d "'%part_size+dest_file+'\" "'+source_file+'"'
    command = '"'+COMPRESS_TOOL+'" a -mx9 -t7z -v%d "'%part_size+dest_file+'\" "'+source_file+'"'
    print command
    ps = subprocess.Popen(command)
    ps.wait()
    elapsed = (time.clock() - start)
    print "Time used for compress "+dest_file+": %f"%elapsed + ", Speed:%f"%(file_size/1024/elapsed)+"kb/s\n"
def get_file_list(dir, rand_name):
    file_list = []
    for file in os.listdir(dir):
        if (file.startswith(rand_name)):
            print file
            file_list.append(file)
    return file_list
def get_sharefolder_temp():
    temp_folders = []
    real_temp_path = ""
    for team_name in TEAMS :
        team_path = os.path.join(SHARE_FOLDER, team_name)
        team_members = os.listdir(team_path)
        for name in team_members:
            if USER_NAME.lower().find(name.lower()) != -1 :
                temp_folders.append(os.path.join(team_path, name))
    n = 0
    if len(temp_folders) != 1:
        print "Choose what folder is yours"
        for i in range(0, len(temp_folders)):
            print "%d : %s"%(i+1, temp_folders[i])
        n=raw_input('input: ')
        while not n.isdigit() or int(n) > len(temp_folders):
            n = raw_input("invalid input, please try again: ")
        n = int(n)
    path = temp_folders[n-1]
    return path
def multi_thread_send(COMPRESS_TEMP_DIR, dest_name):
    i = 0
    file_list = get_file_list(COMPRESS_TEMP_DIR, dest_name)
    threads = range(0, len(file_list))
    for file in file_list:
        threads[i] = copy_thread(os.path.join(COMPRESS_TEMP_DIR, file), os.path.join(SHARE_FOLDER, dest_name))
        threads[i].setDaemon(True)
        threads[i].start()
        i += 1
    while 1:
        alive = False
        for i in range(0, len(file_list)):
            alive = alive or threads[i].isAlive()
        if not alive:
            break
        time.sleep(1)
def write_signal_file(time_name, file_name):
    try:
        fp = open(os.path.join(os.path.join(SHARE_FOLDER, time_name), time_name+".sig"), "w")
        cf = ConfigParser.ConfigParser()
        cf.add_section("information")
        cf.set("information", "file_name", file_name)
        if EXECUTE_COMMAND!= "":
            cf.set("information", "execute_command", EXECUTE_COMMAND)
        cf.write(fp)
        fp.close()
    except IOError:
        print "Can't create signal file!"

def make_file_dir(file_name):
    if not os.path.exists(os.path.join(SHARE_FOLDER, file_name)):
        try:
            os.makedirs(os.path.join(SHARE_FOLDER, file_name))
        except IOError:
            print "can't create the file's folder!"
            os.system("pause")
            exit(1)
def init():
    if not os.path.exists(COMPRESS_TEMP_DIR):
        try:
            os.makedirs(COMPRESS_TEMP_DIR)
        except os.error:
            print "Can't create the temp compress folder:" + COMPRESS_TEMP_DIR + ", Please set another one"
            clean()
            os.system("pause")
            exit(1)
    if not os.path.exists(SHARE_FOLDER):
        try:
            os.makedirs(SHARE_FOLDER)
        except os.error:
            print "Can't create the share folder:"+SHARE_FOLDER+" temp directory!"
            clean()
            os.system("pause")
            exit(1)
def clean():
    print "delete config file..."
    os.remove(CONFIG_FILE)
def init_config():
    global COMPRESS_TEMP_DIR
    global SHARE_FOLDER
    global CONFIG_FILE
    global COMPRESS_TOOL
    global DEFAULT_COMPRESS_TEMP_DIR

    while True:
        cf = ConfigParser.ConfigParser()
        if not os.path.exists(CONFIG_FILE):
            # init 7z tool
            if not os.path.isfile(COMPRESS_TOOL):
                COMPRESS_TOOL = "C:\\Program Files (x86)\\7-Zip\\7z.exe"
            if not os.path.isfile(COMPRESS_TOOL):
                print "can't find 7z.exe in 'C:\\Program Files\\7-Zip\\' and 'C:\\Program Files (x86)\\7-Zip\\'"
                COMPRESS_TOOL = raw_input("please input your 7z.exe path:")
            cf.add_section("dir_config")
            TEMP_COMPRESS_TEMP_DIR = DEFAULT_COMPRESS_TEMP_DIR
            SHARE_FOLDER = get_sharefolder_temp()
            SHARE_FOLDER = os.path.join(SHARE_FOLDER, "file_transfer_temp")
            if TEMP_COMPRESS_TEMP_DIR.strip() != '':
                COMPRESS_TEMP_DIR = TEMP_COMPRESS_TEMP_DIR
            COMPRESS_TEMP_DIR = COMPRESS_TEMP_DIR.strip('"')
            COMPRESS_TEMP_DIR = COMPRESS_TEMP_DIR.strip('\'')
            SHARE_FOLDER = SHARE_FOLDER.strip('"')
            SHARE_FOLDER = SHARE_FOLDER.strip('\'')
            cf.set("dir_config", "COMPRESS_TEMP_DIR", COMPRESS_TEMP_DIR)
            cf.set("dir_config", "SHARE_FOLDER", SHARE_FOLDER)
            cf.set("dir_config", "COMPRESS_TOOL", COMPRESS_TOOL)
            fp = open(CONFIG_FILE, "w")
            cf.write(fp)
            fp.close()
            break
        else:
            try :
                cf.read(CONFIG_FILE)
                COMPRESS_TEMP_DIR = cf.get("dir_config", "COMPRESS_TEMP_DIR")
                SHARE_FOLDER = cf.get("dir_config", "SHARE_FOLDER")
                COMPRESS_TOOL = cf.get("dir_config", "COMPRESS_TOOL")
                break
            except ConfigParser.Error:
                print "Config file parse error!"
                clean()
    print "*******************************************************************************"
    print "The compress temp folder is:"+COMPRESS_TEMP_DIR
    print "The share_folder temp folder is:"+SHARE_FOLDER
    print "If you want to modify these folders, Please edit config file:"+CONFIG_FILE
    print "*******************************************************************************"
def start():
    global FILE_MULTIPLE
    global EXECUTE_COMMAND
    source_file = ""
    cmd_psr = OptionParser(usage="usage:%prog [options] filepath")
    cmd_psr.add_option("-m", "--multiple", 
                    action = "store",
                    type = "int",
                    dest = "multiple",
                    help = "The file multiple"
                    )
    cmd_psr.add_option("-e", "--execute",
                    action = "store",
                    type = "string",
                    dest = "execute_command",
                    help = "The execute hook command after transfer"
                    )
    (options, args) = cmd_psr.parse_args()
    if options.multiple:
        FILE_MULTIPLE = options.multiple
    if options.execute_command:
        EXECUTE_COMMAND = options.execute_command
    init_config()
    init()
    if len(args) != 0:
        source_file = args[0]
    else:
        source_file = raw_input("Please input your file or folder to be sent:")
    if not os.path.exists(source_file):
        print "File not exist...."
        exit(1)
    print "compressing file..."
    file_name = os.path.basename(source_file)
    time_name = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
    compress_file(source_file, os.path.join(COMPRESS_TEMP_DIR, time_name))
    make_file_dir(time_name)
    multi_thread_send(COMPRESS_TEMP_DIR, time_name)
    write_signal_file(time_name, file_name)
    print "END!!"
if __name__=='__main__':
    start()