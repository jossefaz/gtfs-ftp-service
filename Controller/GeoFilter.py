# -*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
from utils.path import *
import os
import logging
from registry.GeoFilter import REGISTRY
from utils.builders import InterfaceBuilder
from Store.main import Store
import inspect

class GeoFilter(baseClass) :

    __slots__ = ["AOI", "registry", "file_path", "logger", "filterType", "current", "fields"]

    def __init__(self, config, DIR):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.registry = REGISTRY
        self.AOI = self.registry.get('AOI').get(config.AOI, None)
        self.current = self.registry.get('geometry').get(config.GEO_TYPE, None)
        self.filterType = self.registry.get('filter').get(config.FILTER_TYPE, None)
        self.fields = config.FIELDS
        self.file_path = os.path.join(GetParentDir(os.path.dirname(__file__)), DIR, config.NAME)
        self.result_name = config.RESULT_NAME


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
            result =  self.current(self.file_path,self. AOI, self.filterType, self.fields)
            self.store.set_result(self.result_name, result)
            if len(cbs) > 0:
                self.runPipeline(cbs)
            return result

        except ValueError as e:
            self.logger.error(e)

        except Exception as e :
            self.logger.error(str(e))






