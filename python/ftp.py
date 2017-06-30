from FtpClass import FtpConnection
from multiprocessing.pool import ThreadPool

server = "iuricostermani.tk"
name = "meeseeks"
passw = "lookatme"
def upload(file, serv, n, p):
    ftp = FtpConnection()
    ftp.connect(serv)
    ftp.login(n,p)
    f = open(file,'rb')
    ftp.storbinary('STOR %s' %file, f)
    f.close()
    ftp.quit()

files = ["test","test1","test2","test3","test4"]
pool = ThreadPool(3)
pool.map(upload, files, server, name, passw)
