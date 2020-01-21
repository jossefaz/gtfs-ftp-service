# -*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
from utils.path import *
import os
import logging
from registry.controller import registry
from utils.builders import buildFtpFeederFile, ftp_feeder_file


class AlphaFilter(baseClass) :

    __slots__ = [ "logger","registry", "filterType", "query", "file_path"]

    def __init__(self, table_config=None, id_hash=None, table_ref=None, filter_type="by_id", sql_query=None):
        self.logger = logging.getLogger(__name__)
        self.registry = registry[self.__class__.__name__]
        self.filterType = self.registry.get('filter').get(filter_type, None)
        self.query = sql_query if sql_query is not None else id_hash
        self.file_path = os.path.join(GetParentDir(os.path.dirname(__file__)), table_config.PATH, table_config.NAME) if table_config is not None else None


    def exec(self, arg=None, cbs=None):
        if cbs is None:
            cbs = []
        try :
            if self.filterType is None :
                raise ValueError("the action you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('filter').keys())))
            table_ref, id_result_hash =  self.filterType(self.file_path, self.query)
            if len(cbs) > 0:
                self.runPipeline(cbs, id_result_hash, table_ref)
            return table_ref
        except ValueError as e:
            self.logger.error(e)
        except Exception as e :
            self.logger.error(str(e))

    def runPipeline(self, cbs, id_result_hash, table_ref):
        for cb in cbs:
            callback = self.registry.get('callbacks').get(cb.get('NAME'), None)
            if callback is None:
                self.logger.warning(
                    'the callback {} was not found in the registry, please check mispelling'.format(callback))
            elif callback.get('parameter') == 'tables':
                self.loopTable(callback.get('factory'), cb.get('TABLES', None), table_ref)
            else:
                factory = callback.get('factory')(id_result_hash, table_ref)
                factory.exec()


    def loopTable(self, cb, tables,id_result_hash, table_ref):
        if tables is not None :
            for table in tables :
                table_config = buildFtpFeederFile(table)
                if table_config is None :
                    self.logger.error('a problem occured when trying to convert config parameters to ftp_feed_file')
                    return None
                factory = cb(table_config, id_result_hash, table_ref)
                factory.exec()
        else :
            self.logger.error('feedData callback called but no TABLES attribute was found')

