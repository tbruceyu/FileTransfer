import os
import getpass
Version=2.0
#define protocal
SIGNAL_FILE_SUFFIX = '.sig'
SIGNAL_FILE_NAME = 'file_name'
SIGNAL_EXECUTE_COMMAND = 'execute_command'
USER_NAME = getpass.getuser()
HOME_DIR = os.path.expanduser("~")
SHARE_FOLDER = "F:\\ShareFolder"
TEAMS = ['Marine', 'Outdoor', 'Platform_Support', 'PND']
THREAD_NUM = 3
USER_DIR = 'D:\\User\\'
# Server port private
COMPRESS_TEMP_DIR = USER_DIR + USER_NAME + '\\compress_temp'

MMAP_FILE = 'D:\\User\\' + USER_NAME + 'mmap_file'

def getSharefolder():
    temp_folders = []
    for team_name in TEAMS :
        team_path = os.path.join(SHARE_FOLDER, team_name)
        try:
            team_members = os.listdir(team_path)
        except:
            continue
        for name in team_members:
            if USER_NAME.lower().find(name.lower()) != -1 :
                temp_folders.append(os.path.join(team_path, name))
    return temp_folders
def get7zPath(single = False):
    path = []
    temp = 'C:\\Program Files (x86)\\7-Zip\\7z.exe'
    if os.path.isfile(temp):
        path.append(temp)
    temp = 'C:\\Program Files\\7-Zip\\7z.exe'
    if os.path.isfile(temp):
        path.append(temp)
    if single == True:
        return path[0]
    if len(path) == 0:
        return None
    return path