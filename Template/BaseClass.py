from Template.abstract_abc import ABCMeta, abstract_attribute
from abc import  abstractmethod




class baseClass(metaclass=ABCMeta):

    @abstract_attribute
    def logger(self):
        pass
    @abstractmethod
    def exec(self, arg):
        pass




