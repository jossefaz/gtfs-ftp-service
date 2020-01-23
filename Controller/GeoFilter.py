# -*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
from utils.path import *
import os
import logging
from registry.GeoFilter import REGISTRY
from utils.builders import buildFtpFeederFile, ftp_feeder_file
import inspect

class GeoFilter(baseClass) :

    __slots__ = ["AOI", "registry", "file_path", "logger", "filterType", "current", "tempResult"]

    def __init__(self, filter_name, directory, filename, geometry, filter_type):
        self.logger = logging.getLogger(__name__)
        self.registry = REGISTRY
        self.AOI = self.registry.get('AOI').get(filter_name, None)
        self.current = self.registry.get('geometry').get(geometry, None)
        self.filterType = self.registry.get('filter').get(filter_type, None)
        self.file_path = os.path.join(GetParentDir(os.path.dirname(__file__)), directory, filename)
        self.tempResult = {}
        self.result = None
        self.jobID = 0


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

    def runPipeline(self, cbs, id_result_hash):
        for cb in cbs:
            callback = self.registry.get('callbacks').get(cb.get('NAME'), None)
            if callback is None:
                self.logger.warning(
                    'the callback {} was not found in the registry, please check mispelling'.format(callback))
            elif cb.get('TABLES'):
                self.tempResult =
                self.loopTable(callback, cb.get('TABLES', None),id_result_hash)
            else:
                self.result = self.runCB(callback, cb, id_result_hash)
    def loopTable(self, cb, tables,id_result_hash):
        if tables is not None :
            for table in tables :
                table_config = buildFtpFeederFile(table)
                if table_config is None :
                    self.logger.error('a problem occured when trying to convert config parameters to ftp_feed_file')
                    return None
                self.result = self.runCB(cb, table_config, id_result_hash)
                if table.get('CB') :
                    self.runPipeline(table.get('CB'), self.result)
        else :
            self.logger.error('feedData callback called but no TABLES attribute was found')

    def runCB(self, callback, parameter, result):
        if inspect.isclass(callback):
            factory = callback(parameter, result)
            return factory.exec(self.result)
        else:
            return callback(self.result)




