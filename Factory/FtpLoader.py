import os
from ftplib import FTP


class Ftp:

    def __init__(self, hostname, filename=None, port=21):
        ftp = FTP()
        try:
            ftp.connect(hostname, port)
        except:
            raise Exception('\n\nConnection failed: {}: {}'.format(hostname, str(port)))
        try:
            ftp.login()
            self.start = ftp.pwd()
        except:  # ftplib.error_perm
            raise Exception('Connection to {} failed'.format(hostname))

        self.ftp = ftp
        self.hostname = hostname
        self.filename = filename
    def ls(self):
        return self.ftp.nlst()

    def get(self, file):
        return self.ftp.retrbinary('RETR ' + file, open('%s/%s' % (self.hostname, file), 'wb').write)

    def cwd(self, file):
        return self.ftp.cwd(file)

    def pwd(self):
        return self.ftp.pwd()

    def download(self):
        pass