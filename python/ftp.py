from FtpClass import FtpConnection


ftp = FtpConnection()
ftp.connect("iuricostermani.tk")
ftp.login("meeseeks","lookatme")
#ftp.cwd("/home/admin")

#ftp.upload("test")

ftp.exclude("test")
ftp.get_file_names(ftp.pwd())
for x in ftp.names:
    print(x)

ftp.close()
#file = open(filename, 'wb')

#ftp.retrbinary('RETR %s' % filename, file.write)
#file.close()
#files = []

#files = ftp.nlst()

#for f in files:
#    print(f)