# -*- coding: UTF-8 -*-
from utils.path import *
import os
import logging
from registry.DAO import REGISTRY




class DAO() :

    __slots__ = [ "logger","registry", "indexfield","filterType", "query", "file_path", "fields", "field_map_index", "field_dict"]

    def __init__(self, connection_parameters, query=None):
        self.logger = logging.getLogger(__name__)
        self.registry = REGISTRY
        self.params = connection_parameters
        self.query = query

    def exec(self, args):
        connector = self.registry.get(self.params.get('TECH'))
        if connector :
            instance = connector(self.params.get('INSTANCE'))
            instance.connect()




