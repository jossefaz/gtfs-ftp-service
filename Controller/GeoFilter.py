# -*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
from utils.path import *
import os
import logging
from registry.controller import registry
from utils.builders import buildFtpFeederFile, ftp_feeder_file


class GeoFilter(baseClass) :

    __slots__ = ["AOI", "registry", "file_path", "logger", "filterType", "id_result_hash"]

    def __init__(self, filter_name, dir, filename, geometry, filter_type):
        self.logger = logging.getLogger(__name__)
        self.registry = registry[self.__class__.__name__]
        self.AOI = self.registry.get('AOI').get(filter_name, None)
        self.current = self.registry.get('geometry').get(geometry, None)
        self.filterType = self.registry.get('geoAction').get(filter_type, None)
        self.file_path = os.path.join(GetParentDir(os.path.dirname(__file__)), dir, filename)
        self.id_result_hash = []

    def exec(self, arg=None, cb=None):
        try :
            if self.AOI is None :
                raise ValueError("the filter you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('geoMask').keys())))
            if self.current is None :
                raise ValueError("the filter you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('geometry').keys())))
            if self.filterType is None :
                raise ValueError("the action you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('geoAction').keys())))
            self.AOI = self.AOI()
            result, id_list =  self.current(self.file_path,self. AOI, self.filterType)
            self.id_result_hash = id_list
            if cb is not None:
                calback = self.registry.get('callbacks').get(cb, None)
                if calback is None :
                    self.logger.warning('the callback {} was not found in the registry, please check mispelling'.format(calback))
                    return result
                if cb == 'feedData' :
                    return self.feedData(calback, arg, result)
            return result



        except ValueError as e:
            self.logger.error(e)

        except Exception as e :
            self.logger.error(str(e))



    def feedData(self, cb, arg, hungry_data_struct):
        tables = arg.get('TABLES', None)
        if tables is not None :

            for table in tables :
                table_config = buildFtpFeederFile(table)
                if table_config is None :
                    self.logger.error('a problem occured when trying to convert config parameters to ftp_feed_file')
                    return None
                feed_file = os.path.join(GetParentDir(os.path.dirname(__file__)), table_config.PATH, table_config.NAME)

                feeder = cb(feed_file, self.id_result_hash, table_config.JOIN_FIELD, table_config.FOOD_FIELDS)
                feeder.exec(hungry_data_struct)
        else :
            self.logger.error('feedData callback called but no TABLES attribute was found')

