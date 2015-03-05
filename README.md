# !该项目只完成了80%
##FileTransfer
一个用于公司内部的文件传输工具，transfer_PC.py和transfer_SRV.py的升级版本，目的是为了提高从远端服务器传输文件到本地的速度，以及实现一些自动化的功能，比如传输完毕自动选中文件开关，传输完毕后执行一些命令。让我们能够专注于程序开发。
##如何运行
    1. 安装python 2.7版本 https://www.python.org/download/releases/2.7.6/
    2. 安装pyqt4和pywin32(主要用于实现开机启动)
        http://www.riverbankcomputing.com/software/pyqt/download
        http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/
    3. 运行 python src/execute/PC.py (server)
    4. 运行 python src/execute/SRV.py (client)

