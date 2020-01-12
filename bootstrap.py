#-*- coding: UTF-8 -*-
from Configuration.config import Config
from Factory.FtpLoader import FtpLoader
if __name__ == '__main__' :

    config = Config()
    ftpload = FtpLoader(config.get_property('URL').get('MOT'), config.get_property('FILES').get('TRANSPORTATION') )
    ftpload.connect()
    allFiles = ftpload.ls()
    print(u''.join(allFiles))
    print(config.get_property("WS"))
