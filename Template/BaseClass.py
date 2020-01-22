from Template.abstract_abc import ABCMeta, abstract_attribute
from abc import  abstractmethod
from utils.builders import buildFtpFeederFile, ftp_feeder_file
import inspect


class baseClass(metaclass=ABCMeta):

    @abstract_attribute
    def logger(self):
        pass
    @abstract_attribute
    def result(self):
        pass
    @abstract_attribute
    def registry(self):
        pass
    @abstractmethod
    def exec(self, arg, cb):
        pass

    def runPipeline(self, cbs, id_result_hash):
        for cb in cbs:
            callback = self.registry.get('callbacks').get(cb.get('NAME'), None)
            if callback is None:
                self.logger.warning(
                    'the callback {} was not found in the registry, please check mispelling'.format(callback))
            elif cb.get('TABLES'):
                self.loopTable(callback, cb.get('TABLES', None),id_result_hash)
            else:
                self.runCB(callback, cb, id_result_hash)
    def loopTable(self, cb, tables,id_result_hash):
        if tables is not None :
            for table in tables :
                table_config = buildFtpFeederFile(table)
                if table_config is None :
                    self.logger.error('a problem occured when trying to convert config parameters to ftp_feed_file')
                    return None
                self.runCB(cb, table_config, id_result_hash)
                if table.get('CB') :
                    self.runPipeline(table.get('CB'), self.result)
        else :
            self.logger.error('feedData callback called but no TABLES attribute was found')

    def runCB(self, callback, parameter, result):
        if inspect.isclass(callback):
            factory = callback(parameter, result)
            self.result = factory.exec(self.result)
        else:
            self.result = callback(self.result)





