# -*- coding: UTF-8 -*-
from utils.path import *
import os
import logging
from registry import REGISTRY



class DAO() :

    __slots__ = [ "logger","registry", "indexfield","filterType", "query", "file_path", "fields", "field_map_index", "field_dict"]

    def __init__(self, table_config=None, id_hash=None, filter_type="by_id", sql_query=None, directory=None, filename=None):
        self.logger = logging.getLogger(__name__)
        self.registry = REGISTRY
        self.filterType = self.registry.get('filter').get(filter_type, None)
        self.query = sql_query if sql_query is not None else id_hash[1] if isinstance(id_hash, tuple) else id_hash
        self.file_path = os.path.join(GetParentDir(os.path.dirname(__file__)), table_config.PATH, table_config.NAME) if table_config is not None else os.path.join(GetParentDir(os.path.dirname(__file__)), directory, filename)
        self.fields = table_config.FOOD_FIELDS if table_config is not None else None
        self.field_map_index = []
        self.field_dict = {}
        self.indexfield = table_config.JOIN_FIELD if table_config is not None else None



