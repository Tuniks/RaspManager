from ftplib import FTP
import ftplib


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
            # for obj in self.objList:
            #     if obj['name'] == dirName and obj['isDir']:
            #         return

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