from Template.abstract_abc import ABCMeta, abstract_attribute
from abc import  abstractmethod
from Store.main import Store
from utils.builders import InterfaceBuilder
import inspect

class baseClass(metaclass=ABCMeta):

    def __init__(self):
        store = Store()
        self.store = store.get_instance()

    @abstract_attribute
    def logger(self):
        pass
    @abstract_attribute
    def registry(self):
        pass
    @abstractmethod
    def exec(self, arg, cb):
        pass

    def runPipeline(self, cbs):
        for cb in cbs:
            callback = self.registry.get('callbacks').get(cb.get('NAME'), None)
            if callback is None:
                self.logger.warning(
                    'the callback {} was not found in the registry, please check mispelling'.format(callback))
            elif cb.get('TABLES'):
                self.loopTable(callback, cb.get('TABLES', None))
            else:
                result = self.runCB(callback, cb)
                self.store.set_result(cb.get('RESULT_NAME'), result)
    def loopTable(self, cb, tables):
        if tables is not None :
            for table in tables :
                table_config = InterfaceBuilder(table, table.get('ITYPE'))
                if table_config is None :
                    self.logger.error('a problem occured when trying to convert config parameters to ftp_feed_file')
                    return None
                result = self.runCB(cb, table_config)
                self.store.set_result(table.get('RESULT_NAME'), result)
                if table.get('CB') :
                    self.runPipeline(table_config.CB)
        else :
            self.logger.error('feedData callback called but no TABLES attribute was found')

    def runCB(self, callback, parameter):
        try:
            store_adress = parameter.LINKED_TO
        except:
            store_adress = parameter.get('LINKED_TO')
        if inspect.isclass(callback):

            factory = callback(parameter, self.store.get_result(store_adress))
            return factory.exec(self.store.get_result(store_adress))
        else:
            return callback(self.store.get_result(store_adress))



class singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]




