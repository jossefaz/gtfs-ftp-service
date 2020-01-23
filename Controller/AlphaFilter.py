# -*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
from utils.path import *
import os
import logging
from registry.AlphaFilter import REGISTRY
from utils.builders import InterfaceBuilder
from utils.alphanum import fieldMapper
import inspect


class AlphaFilter(baseClass) :

    __slots__ = ["logger","registry", "indexfield","filterType", "query", "file_path", "fields", "field_map_index", "field_dict"]

    def __init__(self, table_config=None, id_hash=None, filter_type="by_id", sql_query=None, directory=None, filename=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.registry = REGISTRY
        self.filterType = self.registry.get('filter').get(filter_type, None)
        self.query = sql_query if sql_query is not None else id_hash[1] if isinstance(id_hash, tuple) else id_hash.get('ids')
        self.file_path = os.path.join(GetParentDir(os.path.dirname(__file__)), table_config.PATH, table_config.NAME) if table_config is not None else os.path.join(GetParentDir(os.path.dirname(__file__)), directory, filename)
        self.fields = table_config.FOOD_FIELDS if table_config is not None else None
        self.field_map_index = []
        self.field_dict = {}
        self.indexfield = table_config.JOIN_FIELD if table_config is not None else None
        self.result_name = table_config.RESULT_NAME


    def exec(self, arg=None, cbs=None):
        if cbs is None:
            cbs = []
        self.field_map_index, self.field_dict = fieldMapper(self.file_path, self.fields, self.logger)
        try :
            if self.filterType is None :
                raise ValueError("the action you specified in config.yaml does not exist in the registry, check mispelling. It must be one of these : {}".format(u' , '.join(self.registry.get('filter').keys())))
            result = self.filterType(self.file_path, self.query, self.indexfield, self.logger, self.field_map_index, self.field_dict)
            self.store.set_result(self.result_name, result)
            if len(cbs) > 0:
                self.runPipeline(cbs)
            return result
        except ValueError as e:
            self.logger.error(e)
        except Exception as e :
            self.logger.error(str(e))





