#-*- coding: UTF-8 -*-
from Configuration.config import Config
import logging
from loggers.boot import setupLogging
from Factory.FtpLoader import FtpLoader

setupLogging()
logger = logging.getLogger(__name__)

if __name__ == '__main__' :

    config = Config()
    ftp = FtpLoader(config.get_property("URL")[0].get("MOT"))
    ftp.connect()

