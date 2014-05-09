import os
import getpass
Version=2.0
#define protocal
SIGNAL_FILE_SUFFIX = '.sig'
SIGNAL_FILE_NAME = 'file_name'
SIGNAL_EXECUTE_COMMAND = 'execute_command'
USER_NAME = getpass.getuser()
HOME_DIR = os.path.expanduser("~")
SHARE_FOLDER = "C:\\Program Files\\7-Zip\\"
TEAMS = ['Marine', 'Outdoor', 'Platform_Support', 'PND']
def getSharefolder():
    return "F:\\ShareFolder"
    temp_folders = []
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