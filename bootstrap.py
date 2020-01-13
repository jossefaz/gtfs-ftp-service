#-*- coding: UTF-8 -*-
from Configuration.config import Config
import logging
from loggers.boot import setupLogging
from Factory.FtpLoader import FtpLoader

setupLogging()
logger = logging.getLogger(__name__)
logger.info("testInfo")
logger.debug("testDebug")
logger.warning("testWarning")
logger.error("testError")

if __name__ == '__main__' :

    config = Config()
    ftpconnect = FtpLoader(config.get_property("URL")[0].get("MOT"))
    print(config.get_property('FILES'))

    print(list)

