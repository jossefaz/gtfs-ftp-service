import os
from Templates.BaseClass import baseClass
from ftplib import FTP
import logging
import sys




class FtpLoader(baseClass):

    __slots__ = ['hostname', 'port', 'ftp', 'logger']

    def __init__(self, hostname, port=21):
        self.setClassLogger()
        self.hostname = hostname
        self.port = port

    def setClassLogger(self):
        self.logger = logging.getLogger(__name__)

    def connect(self):
        ftp = FTP()
        try:
            ftp.connect(self.hostname, self.port)
            self.logger.info("Connected to : ftp://{}".format(self.hostname))
        except Exception as e:
            message = 'Connection to : ftp://{} failed, check if adress is correct'.format(self.hostname)
            self.logger.error(message)

        try:
            ftp.login()
            self.ftp = ftp
            self.logger.debug("Logged into : ftp://{}".format(self.hostname))
            self.ftp.set_pasv(True)
            self.logger.debug("FTP set to passive mode : ftp://{}".format(self.hostname))
        except:  # ftplib.error_perm
            self.logger.error('Authentication to {} failed'.format(self.hostname))


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