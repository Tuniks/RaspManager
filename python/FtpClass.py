from ftplib import FTP
import ftplib
from multiprocessing.pool import ThreadPool

class FtpConnection(FTP):

    def __init__(self):
        super().__init__()
        self.objList = []

    def ls(self):
        self.objList = []
        rawlist = []
        self.retrlines("LIST", rawlist.append)

        for i, x in enumerate(rawlist):
            isdir = x[0] == 'd'
            objname = x.rsplit(None, 1)[-1]
            self.objList.append({'name': objname, 'isDir': isdir})

    def cd(self, dirName):
        try:
            self.cwd(dirName)
            self.ls()
        except ftplib.error_perm:
            return

    def download(self, filename):
        file = open(filename, 'wb')
        self.retrbinary('RETR %s' % filename, file.write)
        file.close()

    def upload(self, filename):
        self.storbinary("STOR " + filename, open(filename, 'rb'))

    def exclude(self, filename):
        try:
            self.delete(filename)
        except ftplib.error_perm:
            return

    def uploadMulti(file):
        ftp = FtpConnection()
        ftp.connect("iuricostermani.tk")
        ftp.login("meeseeks","lookatme")
        f = open(file,'rb')
        ftp.storbinary('STOR %s' %file, f)
        f.close()
        ftp.quit()

    def uploadPool(files):
        pool = ThreadPool(len(files))
        pool.map(uploadMulti, files)