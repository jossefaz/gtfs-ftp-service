from Template.BaseClass import baseClass
from utils.path import *
import threading
import logging
from ftplib import FTP, error_perm

import socket
import time
import os

def setInterval(interval, times = -1):
    def outer_wrap(function):
        def wrap(*args, **kwargs):
            stop = threading.Event()
            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1
            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap

MONITOR_INTERVAL = 30
class FtpLoader(baseClass):

    __slots__ = ['host', 'port', 'ptr', 'max_attempts', 'waiting', 'logger','outDir']

    def __init__(self, host, port=21, outDir = None):
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.ptr = None
        self.max_attempts = 15
        self.waiting = True
        self.cwd = os.getcwd()
        self.outDir = outDir


    def exec(self, dst_filename, cb=None):
        self.downloadFileItem(dst_filename)
        if cb is not None :
            cb()


    def connect(self):
        ftp = FTP()
        ftp.set_debuglevel(0)
        ftp.set_pasv(True)
        self.logger.debug("FTP set to passive mode : ftp://{}".format(self.host))
        try:
            ftp.connect(self.host, self.port)
            self.logger.info("Connected to : ftp://{}".format(self.host))
        except Exception as e:
            message = 'Connection to : ftp://{} failed, checkout the name'.format(self.host)
            self.logger.error(message)
            return False

        try:
            ftp.login()
            self.logger.debug("Logged into : ftp://{}".format(self.host))

        except:  # ftplib.error_perm
            message = 'Authentication to {} failed'.format(self.host)
            self.logger.error(message)
            return False
        ftp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 75)
        ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
        self.ftp = ftp
        return True


    @setInterval(MONITOR_INTERVAL)
    def monitor(self, file):
        if not self.waiting:
            i = file.tell()
            if self.ptr < i:
                self.logger.debug("%d  -  %0.1f Kb/s" % (i, (i - self.ptr) / (1024 * MONITOR_INTERVAL)))
                self.ptr = i
            else:
                self.ftp.close()

    def ls(self, depth=0):
        if depth > 10:
            return ['depth > 10']
        level = {}
        for entry in (path for path in self.ftp.nlst() if path not in ('.', '..')):
            try:
                self.ftp.cwd(entry)
                level[entry] = self.ls(self.ftp, depth + 1)
                self.ftp.cwd('..')
            except error_perm:
                level[entry] = None
        return level
    def getFileSize(self, file):
        return self.ftp.size(file)

    def openDlStream(self, outDir, filePtr, filename):
        try:
            self.connect()
        except:
            self.logger.error("Cannot connect to ftp while attempt to open stream")
            return False
        self.waiting = False
        if outDir is not None:

            downdir = os.path.join(GetParentDir(os.path.dirname(__file__)), outDir)
            os.chdir(downdir)
        res = self.ftp.retrbinary('RETR %s' % filename, filePtr.write) if filePtr.tell() == 0 else \
            self.ftp.retrbinary('RETR %s' % filename, filePtr.write, rest=filePtr.tell())
        os.chdir(self.cwd)
        return res
    def checkIfFileExist(self, fName):
        files_list = self.ls()
        for file, subfiles in files_list.items() :
            if fName == file :
                return True
        return False

    def downloadFileItem(self, dst_filename):

        local_filename = dst_filename
        if self.outDir is not None:
            checkPath = os.path.join(GetParentDir(os.path.dirname(__file__)), self.outDir)
            safeOpen(checkPath)
            local_filename = os.path.join(checkPath, local_filename)
        try:
            conn = self.connect()
        except:
            return False
        if conn:

            if self.checkIfFileExist(dst_filename) :
                with open(local_filename, 'w+b') as filePtr:
                        self.ptr = filePtr.tell()
                        dst_filesize = self.getFileSize(dst_filename)
                        mon = self.monitor(filePtr)
                        downloaded = ''
                        while dst_filesize > filePtr.tell():
                            try:
                                downloaded = self.openDlStream(self.outDir, filePtr, dst_filename)
                                if downloaded is None :
                                    break
                            except:
                                self.max_attempts -= 1
                                if self.max_attempts == 0:
                                    mon.set()
                                    self.logger.exception('')
                                    raise
                                self.waiting = True
                                self.logger.info('waiting 30 sec...')
                                time.sleep(30)
                                self.logger.info('reconnect')

                        if not downloaded.startswith('226 Transfer complete'):
                            self.logger.error('Downloaded file {0} is not full.'.format(dst_filename))
                            # os.remove(local_filename)
                            return None
                        mon.set() #stop monitor
                        self.ftp.close()
                        return True

            else :
                self.logger.error("the file {} does not exist in the FTP server. Check mispelling".format(dst_filename))
                return None



