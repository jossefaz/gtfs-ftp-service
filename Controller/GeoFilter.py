# -*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
from utils.path import *
import os
import logging
from registry.GeoFilter import REGISTRY


class GeoFilter(baseClass) :

    __slots__ = ["AOI", "registry", "file_path", "logger", "filterType", "current"]

    def __init__(self, filter_name, directory, filename, geometry, filter_type):
        self.logger = logging.getLogger(__name__)
        self.registry = REGISTRY
        self.AOI = self.registry.get('AOI').get(filter_name, None)
        self.current = self.registry.get('geometry').get(geometry, None)
        self.filterType = self.registry.get('filter').get(filter_type, None)
        self.file_path = os.path.join(GetParentDir(os.path.dirname(__file__)), directory, filename)
        self.result = None


    def exec(self, arg=None, cbs=None):
        if cbs is None:
            cbs = []
        try :
            if self.AOI is None :
                raise ValueError("the AOI you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('AOI').keys())))
            if self.current is None :
                raise ValueError("the geometry you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('geometry').keys())))
            if self.filterType is None :
                raise ValueError("the filter you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('filter').keys())))
            self.AOI = self.AOI()
            id_result_hash =  self.current(self.file_path,self. AOI, self.filterType)
            if len(cbs) > 0:
                self.runPipeline(cbs, id_result_hash)
            return self.result

        except ValueError as e:
            self.logger.error(e)

        except Exception as e :
            self.logger.error(str(e))



