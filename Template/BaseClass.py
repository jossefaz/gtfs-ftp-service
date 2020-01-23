from Template.abstract_abc import ABCMeta, abstract_attribute
from abc import  abstractmethod



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


class Dal(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Dal, cls).__call__(*args, **kwargs)
        return cls._instances[cls]




