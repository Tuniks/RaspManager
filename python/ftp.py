from FtpClass import FtpConnection
from multiprocessing.pool import ThreadPool


def upload(file):
    ftp = FtpConnection()
    ftp.connect("iuricostermani.tk")
    ftp.login("meeseeks","lookatme")
    f = open(file,'rb')
    ftp.storbinary('STOR %s' %file, f)
    f.close()
    ftp.quit()

files = ["test","test1","test2","test3","test4"]

pool = ThreadPool(3)
pool.map(upload, files)
