import win32pipe, win32file
import win32file
import os
import sys
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))
from core.common import NAMED_PIPE_PATH
fileHandle = win32file.CreateFile(NAMED_PIPE_PATH,
                              win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                              0, None,
                              win32file.OPEN_EXISTING,
                              0, None)
data = win32file.WriteFile(fileHandle, "1|f|f|f|ff\n")
