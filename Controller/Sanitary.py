import logging
from urllib import request

from sqlalchemy import inspect

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
        Callbacks = []
        for domain in urls:
            for dom, url in domain.items():
                dict_files = self.config.get_property("FILES").get(dom)
                if dict_files is not None:
                    for file, props in dict_files.items():
                        for f in props:
                            fType = f.get('ITYPE')
                            if fType is not None:
                                fileConfig = self.checkInterfaceBuilder(f, fType)
                                if 'CB' in f:
                                    Callbacks.append([f.get('CB'), f.get('FIELDS')])
        return self.checkCallBack(Callbacks)

    def checkCallBack(self, cbMainlist):
        dbCallbacks = []


        for cblist in cbMainlist :
            callbacks = cblist[0]
            fields = cblist[1]
            for cb in callbacks :
                fType = cb.get('ITYPE')
                if fType is not None:
                    fileConfig = self.checkInterfaceBuilder(cb, fType)
                    if fType == 'TABLES':
                        for table in fileConfig.TABLES :
                            fsubType = table.get('ITYPE')
                            if fsubType is not None:
                                fileConfig = self.checkInterfaceBuilder(table, fsubType)
                                if 'CB' in table:
                                    for tablecb in fileConfig.CB :
                                        fcbType = tablecb.get('ITYPE')
                                        fileConfig = self.checkInterfaceBuilder(tablecb, fcbType)
                                        if fileConfig.ITYPE == 'DB' :
                                            dbCallbacks.append([tablecb, table.get('FIELDS')])

                    if fType == 'DB' :
                        fileConfig = self.checkInterfaceBuilder(cb, fType)
                        dbCallbacks.append([cb, fields])
        return self.checkDBCallback(dbCallbacks)

    def checkDBCallback(self, cblist):
        current_instance = None
        engine = None
        inspector = None
        all_tables = []
        schema = None
        allDB = self.config.get_property('DB')
        def createDbEngine(instance_name) :
            connector = DAL(instance_name)
            connection = connector.connect()
            return connection.create_engine()
        for cb in cblist :
            if cb[0].get('INSTANCE') != current_instance :

                engine = createDbEngine(cb[0].get('INSTANCE'))
                current_instance = cb[0].get('INSTANCE')
                inspector = inspect(engine)
                schema = allDB.get(cb[0].get('INSTANCE')).get('SCHEMA')
                all_tables = inspector.get_table_names(schema)
            try :
                table_index = all_tables.index(cb[0].get('TABLE'))
            except ValueError as e :
                self.logger.error('The table {} is not present in the Databae {} please check config file'.format(cb[0].get('TABLE'), cb[0].get('INSTANCE')))
                return False
            all_columns = [c['name'] for c in inspector.get_columns(cb[0].get('TABLE'), schema)]
            for column in cb[1]:
                if column not in all_columns :
                    if column.endswith("id") and current_instance.endswith("GEO") :
                        continue
                    self.logger.error("The Column {} does not exist in the current table {}".format(column, cb[0].get('TABLE')))
                    return False
        return True

    def checkInterfaceBuilder(self, struct, type):
        try:
            fileConfig = InterfaceBuilder(struct, type)
        except TypeError as e:
            self.logger.error('the pipeline file config is not builded as expected : missed the key {}'.format(
                str(e).split(':')[1]))
            return False
        except Exception as e:
            self.logger.error('the pipeline file config is not builded as expected : {}'.format(str(e)))
            return False
        return fileConfig




