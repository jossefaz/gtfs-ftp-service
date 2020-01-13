import os
from ftplib import FTP
import logging



class FtpLoader:

    __slots__ = ['hostname', 'port', 'ftp', 'logger']

    def __init__(self, hostname, filename=None, port=21):
        self.hostname = hostname
        self.port = port
        self.logger = logging.getLogger(__name__)
        self.logger.info("FTP created")
        self.logger.debug("FTP DEBUG")
        self.logger.warning("FTP WARNING")
        self.logger.critical("FTP Critical")
        self.logger.error("FTP Critical")


    def connect(self):
        ftp = FTP()
        try:
            ftp.connect(self.hostname, self.port)
        except Exception as e:
            message = 'Connection failed: {}: {}'.format(self.hostname, str(self.port))
            self.logger.error(message)
            raise Exception(str(e))
        try:
            ftp.login()
            self.ftp = ftp
        except:  # ftplib.error_perm

            raise Exception('Authentication to {} failed'.format(self.hostname))

    def ftp_date_all(self):
        dir_listing = []
        self.ftp.dir(lambda x: dir_listing.append(x))
        return [(line.split(' ')[0], line.split(' ')[-1]) for line in dir_listing]

    def ftp_date_one(self, filename):
        dir_listing = []
        self.ftp.dir(lambda x: dir_listing.append(x))
        return [(line.split(' ')[0], line.split(' ')[-1]) for line in dir_listing if line.split(' ')[-1] == filename][0]

    def get(self, file):
        return self.ftp.retrbinary('RETR ' + file, open('%s/%s' % (self.hostname, file), 'wb').write)

    def cwd(self, file):
        return self.ftp.cwd(file)

    def download(self):
        pass