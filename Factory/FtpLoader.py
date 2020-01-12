import os
from ftplib import FTP


class FtpLoader:

    __slots__ = ['hostname', 'port', 'filename', 'ftp', 'root']

    def __init__(self, hostname, filename=None, port=21):

        self.hostname = hostname
        self.port = port
        self.filename = filename

    def connect(self):
        ftp = FTP()
        try:
            ftp.connect(self.hostname, self.port)
        except Exception as e:
            message = 'Connection failed: {}: {}'.format(self.hostname, str(self.port))
            raise Exception(str(e))
        try:
            ftp.login()
            self.ftp = ftp
            self.root = ftp.pwd()


        except:  # ftplib.error_perm
            raise Exception('Connection to {} failed'.format(self.hostname))


    def get(self, file):
        return self.ftp.retrbinary('RETR ' + file, open('%s/%s' % (self.hostname, file), 'wb').write)

    def cwd(self, file):
        return self.ftp.cwd(file)

    def download(self):
        pass