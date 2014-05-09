import os
import sys
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))
import shutil
from optparse import OptionParser
from core import transferSRV
import time

if __name__=='__main__':
    global FILE_MULTIPLE
    global EXECUTE_COMMAND
    source_file = ""
    cmd_psr = OptionParser(usage="usage:%prog [options] filepath")
    cmd_psr.add_option("-e", "--execute",
                    action = "store",
                    type = "string",
                    dest = "execute_command",
                    help = "The execute hook command after transfer"
                    )
    (options, args) = cmd_psr.parse_args()
    if options.execute_command:
        EXECUTE_COMMAND = options.execute_command
    transferSRV.init_config()
    if len(args) != 0:
        source_file = args[0]
    else:
        source_file = raw_input("Please input your file or folder to be sent:")
    if not os.path.exists(source_file):
        print "File not exist...."
        exit(1)
    transferSRV.start(source_file)
    print "end!"
