#-*- coding: UTF-8 -*-
from Configuration.config import Config
from Factory.FtpLoader import FtpLoader
if __name__ == '__main__' :

    config = Config()
    ftpload = FtpLoader(config.get_property('URL').get('MOT'))
    ftpload.connect()
    list = ftpload.ftp_date_one(config.get_property('FILES').get('TRANSPORTATION'))
    print(list)

