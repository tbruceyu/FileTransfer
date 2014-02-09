import os
import time
import subprocess
import ConfigParser
import getpass
import threading
from optparse import OptionParser

COMPRESS_TOOL="C:\\Program Files\\7-Zip\\7z.exe"
SHARE_FOLDER = "//c3-se-terminal3/Shared_Folder"
LOCAL_DIR = "D:\\file_destination\\"
USER_NAME = getpass.getuser()
HOME_DIR = os.path.expanduser("~")
CONFIG_FILE = os.path.join(HOME_DIR, "file_transfer.conf")
DEFAULT_LOCAL_DIR = LOCAL_DIR
SILENCE = False
BACKUP_MODE = False
TEAMS = ['Marine', 'Outdoor', 'Platform_Support', 'PND']
class signalConf():
    def __init__(self):
        self.file_name = ""
        self.execute_command = ""
class process_thread(threading.Thread):
    def __init__(self, wait_dir):
        threading.Thread.__init__(self, name="process thread")
        self.wait_dir = wait_dir
    def run(self):
        # wait for signal file written
        signal_conf = signalConf()
        signal_conf = wait_for_signal(self.wait_dir)
        # extract file
        target_dir = extract_file(self.wait_dir, signal_conf.file_name)
        if SILENCE == False:
            os.startfile(target_dir)
        execute_command(target_dir, signal_conf)
def execute_command(target_dir, signal_conf):
    if signal_conf.execute_command == "":
        return
    for command in signal_conf.execute_command.split(';'):
        target_file = os.path.join(target_dir, signal_conf.file_name)
        if command.find("%s") != -1:
            command = command % target_file
        print command
        ps = subprocess.Popen(command)
        ps.wait()
def wait_for_signal(dir_name):
    print "wait for signal file....."
    dest_folder = os.path.join(SHARE_FOLDER, dir_name)
    signal_path = os.path.join(dest_folder, dir_name+".sig")
    cf = ConfigParser.ConfigParser()
    signal_conf = signalConf()
    while signal_conf.file_name == "":
        try:
            cf.read(signal_path)
            signal_conf.file_name = cf.get("information", "file_name")
            break
        except ConfigParser.Error:
            time.sleep(2)
    try :
        signal_conf.execute_command = cf.get("information", "execute_command")
    except ConfigParser.Error:
        signal_conf.execute_command = ""
    return signal_conf
def extract_file(sub_file, signal_file_name):
    file_dir = sub_file
    file_name = file_dir+".7z.001"
    if BACKUP_MODE == True:
        local_dir = os.path.join(os.path.join(LOCAL_DIR, signal_file_name+"_"), file_dir)
    else:
        local_dir = LOCAL_DIR
    file_path = os.path.join(os.path.join(SHARE_FOLDER, file_dir), file_name)
    command = '"%s" x -o"'%COMPRESS_TOOL+local_dir+'" "' + file_path + '" -y'
    print command
    ps = subprocess.Popen(command)
    ps.wait()
    print "Complete!!! Please visit '%s'"%local_dir
    return local_dir
def watch_dir():
    old_list = os.listdir(SHARE_FOLDER)
    print "Watching %s"%SHARE_FOLDER
    while 1:
        new_list = os.listdir(SHARE_FOLDER)
        sub_list = list(set(new_list) - set(old_list))
        if len(sub_list) > 0:
            print "Create a daemon thread watching '%s'"%os.path.join(SHARE_FOLDER, sub_list[0])
            thread = process_thread(sub_list[0])
            thread.setDaemon(True)
            thread.start()
            # reset the lists
            old_list = os.listdir(SHARE_FOLDER)
            new_list = old_list
        old_list = new_list
        time.sleep(2)
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
def init_config():
    global SHARE_FOLDER
    global LOCAL_DIR
    global CONFIG_FILE
    global COMPRESS_TOOL
    global DEFAULT_LOCAL_DIR

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
            TEMP_LOCAL_DIR = raw_input("Input local destination folder(default:%s):"%DEFAULT_LOCAL_DIR)
            SHARE_FOLDER = get_sharefolder_temp()
            SHARE_FOLDER = os.path.join(SHARE_FOLDER, "file_transfer_temp")
            if TEMP_LOCAL_DIR.strip() != '':
                LOCAL_DIR = TEMP_LOCAL_DIR
            LOCAL_DIR = LOCAL_DIR.strip('"')
            LOCAL_DIR = LOCAL_DIR.strip('\'')
            SHARE_FOLDER = SHARE_FOLDER.strip('"')
            SHARE_FOLDER = SHARE_FOLDER.strip('\'')
            cf.set("dir_config", "LOCAL_DIR", LOCAL_DIR)
            cf.set("dir_config", "SHARE_FOLDER", SHARE_FOLDER)
            cf.set("dir_config", "COMPRESS_TOOL", COMPRESS_TOOL)
            fp = open(CONFIG_FILE, "w")
            cf.write(fp)
            fp.close()
            break
        else:
            try :
                cf.read(CONFIG_FILE)
                LOCAL_DIR = cf.get("dir_config", "LOCAL_DIR")
                SHARE_FOLDER = cf.get("dir_config", "SHARE_FOLDER")
                COMPRESS_TOOL = cf.get("dir_config", "COMPRESS_TOOL")
                break
            except ConfigParser.Error:
                print "Config file parse error!"
                clean()
    print "*******************************************************************************"
    print "The destination folder is:"+LOCAL_DIR
    print "The share_folder temp folder is:"+SHARE_FOLDER
    print "If you want to modify these folders, Please edit config file:"+CONFIG_FILE
    print "*******************************************************************************"
def init():
    init_config()

    if not os.path.exists(LOCAL_DIR):
        try:
            os.makedirs(LOCAL_DIR)
        except os.error:
            print "Can't create the local folder:" + LOCAL_DIR + ", Please set another one"
            clean()
            os.system("pause")
            exit()
    if not os.path.exists(SHARE_FOLDER):
        try:
            os.makedirs(SHARE_FOLDER)
        except os.error:
            print "Can't create the share folder:"+SHARE_FOLDER+" temp directory!"
            clean()
            os.system("pause")
            exit()
def clean():
    print "delete config file..."
    os.remove(CONFIG_FILE)
def start():
    global SILENCE
    global BACKUP_MODE
    cmd_psr = OptionParser(usage="usage:%prog [options]")
    cmd_psr.add_option("-s", "--silence", 
                    action = "store_true",
                    default=False,
                    dest = "silence",
                    help = "Don't open the directory after extact the file"
                    )
    cmd_psr.add_option("-b", "--backup", 
                    action = "store_true",
                    default=False,
                    dest = "backup",
                    help = "Back up the file in every thansfer"
                    )
    (options, args) = cmd_psr.parse_args()
    if options.silence:
        SILENCE = options.silence
    if options.backup:
        BACKUP_MODE = options.backup
    init()
    try:
        watch_dir()
    except KeyboardInterrupt:
        import sys
        sys.exit()
if __name__=='__main__':
    start()