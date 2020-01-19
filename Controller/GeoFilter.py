#-*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
from utils.path import *
import os
import logging
from Controller.registry import reg_controller


class GeoFilter(baseClass) :
    __slots__ = ["geoMask", "registry", "file_path", "logger", "filterType"]

    def __init__(self, filtername, dir, filename, geometry, filtertype):
        self.logger = logging.getLogger(__name__)
        self.registry = reg_controller[self.__class__.__name__]
        self.geoMask = self.registry.get('geoMask').get(filtername, None)
        self.current = self.registry.get('geometry').get(geometry, None)
        self.filterType = self.registry.get('geoAction').get(filtertype, None)
        self.file_path = os.path.join(GetParentDir(os.path.dirname(__file__)), dir, filename)



    def exec(self):
        try :
            if self.geoMask is None :
                raise ValueError("the filter you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('geoMask').keys())))
            if self.current is None :
                raise ValueError("the filter you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('geometry').keys())))
            if self.filterType is None :
                raise ValueError("the action you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('geoAction').keys())))
            self.geoMask = self.geoMask()
            return self.current(self.file_path,self. geoMask, self.filterType)



        except ValueError as e:
            self.logger.error(e)

        except Exception as e :
            self.logger.error(str(e))


        pass

if __name__ == '__main__' :
    test = GeoFilter('JERUSALEM', 'download/israel-public-transportation', 'shapes.txt', 'line', 'within')
    test.exec()


