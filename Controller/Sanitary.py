import logging
from urllib import request

from Controller.FtpLoader import FtpLoader
from Store.main import Store
from Model.DAL import DAL
from utils.builders import InterfaceBuilder
class Sanitary() :
    def __init__(self, config):
        self.config = config
        self.error_messages = config.get_property('Error_Message').get('Sanitary')
        self.logger =  logging.getLogger(__name__)

    def checkDBConnection(self):
        allDB = self.config.get_property('DB')
        if not len(allDB) > 0 :
            logging.warning(self.error_messages.get('DB').get('ANY_DB_FOUND'))
        for db, db_config in self.config.get_property('DB').items() :
            mandatory = db_config.get('MANDATORY')
            connector = DAL(db)
            try :
                connector.connect()
            except Exception as e :
                if mandatory :
                    self.logger.error(self.error_messages.get('DB').get('CONNECTION_FAILED').format(db, str(e)))
                    return False
                else :
                    self.logger.warning(self.error_messages.get('DB').get('CONNECTION_FAILED').format(db, str(e)))
                    continue
        return True
    def checkNetworkConnection(self, host='http://google.com'):
        try:
            request.urlopen(host)
            return True
        except:
            self.logger.error(self.error_messages.get('INTERNET_CONNECTION_FAILED'))
            return False

    def checkStoreConnection(self):
        try:
            store = Store()
        except :
            self.logger.error(self.error_messages.get('STORE_FAILED'))
            return False
        return store

    def checkFTPCOnnection(self):
        urls = self.config.get_property("URL")
        not_Valid_url = []
        for domain in urls:
            for dom, url in domain.items():
                download_dir = self.config.get_property("WS").get("DOWNLOAD").get(dom)
                ftp = FtpLoader(url, outDir=download_dir)
                try :
                    ftp.connect()
                except Exception as e :
                    not_Valid_url.append(url)
        if len(not_Valid_url) > 0 :
            self.logger.warning(self.error_messages.get('FTP_URLS_INVALID').format(', '.join(not_Valid_url)))
        return not_Valid_url

    def checkPipeLineFile(self, urls):
        for domain in urls:
            for dom, url in domain.items():
                dict_files = self.config.get_property("FILES").get(dom)
                if dict_files is not None:
                    for file, props in dict_files.items():
                        for f in props:
                            fType = f.get('ITYPE')
                            if fType is not None:
                                try :
                                    fileConfig = InterfaceBuilder(f, fType)
                                except TypeError as e :
                                    self.logger.error('the pipeline file config is not builded as expected : missed the key {}'.format(str(e).split(':')[1]))
                                    return False
                                except Exception as e :
                                    self.logger.error('the pipeline file config is not builded as expected : {}'.format(str(e)))
                                    return False

        return True




