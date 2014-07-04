import inspect
import ctypes
import threading
import win32api
import win32con
from pprint import pprint 

#define DEBUG types
INFO = 1
WARNING = 2
ERROR = 3
#define work states
STOPPED = 0
WATCHING = 1
WAITING = 2
WORKING = 3

PROGRAM_PATH = ''
class Log():
    @staticmethod
    def e(tag, string):
        print "TAG:"+tag+" content:"+string
    @staticmethod
    def d(tag, string):
        print "d:" + tag + " content:" + string
    @staticmethod
    def v(tag, string):
        print "v:" + string
def setProgramPath(path):
    global PROGRAM_PATH
    PROGRAM_PATH = path
def getProgramPath(path):
    return PROGRAM_PATH
def RunOnStartup(path):
    key =  win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,
                    "Software\Microsoft\Windows\CurrentVersion\Run",
                    0,
                    win32con.KEY_ALL_ACCESS
                    )
    needSet = False
    try:
        currentVal= win32api.RegQueryValueEx(key, 'FileTransferPC')
        if currentVal != path:
            needSet = True
    except:
        needSet = True
    if needSet:
        win32api.RegSetValueEx(key,'FileTransferPC',0,win32con.REG_SZ,'D:\\Program Files\\Console2\\Console.exe')
    win32api.RegCloseKey(key)
def _async_raise(tid, exctype):
    '''Raises an exception in the threads with id tid'''
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class ThreadWithExc(threading.Thread):
    '''A thread class that supports raising exception in the thread from
       another thread.
    '''
    def _get_my_tid(self):
        return self.ident
        

    def raiseExc(self, exctype):
        """Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseExc( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raiseExc( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL : this function is executed in the context of the
        caller thread, to raise an excpetion in the context of the
        thread represented by this instance.
        """
        _async_raise( self._get_my_tid(), exctype )
    def terminate(self):
        """raises SystemExit in the context of the given thread, which should 
        cause the thread to exit silently (unless caught)"""
        self.raiseExc(SystemExit)