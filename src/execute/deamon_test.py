import mmap
import os.path
fd = 0
mmapFile = "D:\\User\\xia.mmap"
if os.path.isfile(mmapFile):
    print "is file!"
try :
    mmap_fp = open(mmapFile, 'r')
    fd = mmap.mmap(mmap_fp.fileno(), 1024, access=mmap.ACCESS_READ)
except Exception as e:
    print "heheh"+str(e)

str = '1|f|f|f|ff\n'
fd.write(str)
