from ftplib import FTP
import ftplib


class FtpConnection(FTP):

    def __init__(self):
        super().__init__()
        self.types = []
        self.names = []

    def get_types(self, dir):
        i = 0
        self.cwd(dir)
        self.retrlines("LIST", self.types.append)
        for x in self.types:
            self.types[i] = x[0]
            i += 1
        return self.types

    def get_file_names(self, dir):
        self.cwd(dir)
        self.retrlines("LIST", self.names.append)
        for i in range(0, len(self.names)):
            self.names[i] = self.names[i].rsplit(None, 1)[-1]
        return self.names

    def cd(self, dir):
        try:
            self.cwd(dir)
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