#-*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
from utils.path import *
import os
import logging
from Controller.registry import reg_controller


class GeoFilter(baseClass) :
    __slots__ = ["AOI", "registry", "file_path", "logger", "filterType"]

    def __init__(self, filter_name, dir, filename, geometry, filter_type):
        self.logger = logging.getLogger(__name__)
        self.registry = reg_controller[self.__class__.__name__]
        self.AOI = self.registry.get('AOI').get(filter_name, None) #TODO : rename mask to areaofinterest
        self.current = self.registry.get('geometry').get(geometry, None)
        self.filterType = self.registry.get('geoAction').get(filter_type, None)
        self.file_path = os.path.join(GetParentDir(os.path.dirname(__file__)), dir, filename)

    def exec(self, arg=None, cb=None):
        try :
            if self.AOI is None :
                raise ValueError("the filter you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('geoMask').keys())))
            if self.current is None :
                raise ValueError("the filter you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('geometry').keys())))
            if self.filterType is None :
                raise ValueError("the action you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('geoAction').keys())))
            self.AOI = self.AOI()
            result =  self.current(self.file_path,self. AOI, self.filterType)
            if (cb is not None) :
                result = cb(result)
            return result


        except ValueError as e:
            self.logger.error(e)

        except Exception as e :
            self.logger.error(str(e))



