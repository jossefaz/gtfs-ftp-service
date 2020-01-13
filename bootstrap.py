#-*- coding: UTF-8 -*-
from Configuration.config import Config
import logging
from loggers.boot import setupLogging
from Factory.FtpLoader import FtpLoader



if __name__ == '__main__' :

    setupLogging()
    logger = logging.getLogger(__name__)

    config = Config()
    urls = config.get_property("URL")
    for domain in urls :
        for dom, url in domain.items() :
            print(url)
            ftp = FtpLoader(url)
            ftp.connect()
