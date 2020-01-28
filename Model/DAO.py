# -*- coding: UTF-8 -*-
from utils.path import *
import os
import logging
from Model.DAL import DAL
from utils.geometry import transformWKT
from registry.DAO import REGISTRY
from Configuration.Config import Config





class DAO() :

    __slots__ = [ "logger","registry", "params","query", "instance", "data_to_insert", "sqls"]

    def __init__(self, connection_parameters, query=None):
        self.logger = logging.getLogger(__name__)
        self.params = connection_parameters
        self.sqls = Config().get_property('SQL').get(self.params.get('INSTANCE'))
        self.query = query
        self.instance = None
        self.data_to_insert = None

    def exec(self, args):
        connector = DAL(self.params.get('INSTANCE'))
        if connector :
            if args :
                self.data_to_insert = args
            self.instance = connector.connect()
            self.callbackQueries(self.params.get('BEFORE'))
            main = getattr(self, self.params.get('MAIN'))
            main()
            self.callbackQueries(self.params.get('AFTER'))

    def callbackQueries(self, queries):
        if queries :
            for q in queries:
                if isinstance(q, str):
                    query = self.sqls.get(q)
                    self.executeQuery(query)
                elif isinstance(q, dict):
                    query = self.sqls.get(q.get('NAME'))
                    self.executeQuery(query, q.get('PARAMETERS'))
    def executeQuery(self, query, params=None):
        if params :
            query = query.format(*params)
        self.instance.cursor.execute(query)
        self.instance.connection.commit()


    def insert(self):
        for key, listvalues in self.data_to_insert.items() :
            for valuesDict in listvalues:
                ins_qry = "INSERT INTO {tablename} ({columns}) VALUES {values};".format(
                    tablename=self.params.get('TABLE'),
                    columns=', '.join(valuesDict.keys()),
                    values=tuple(valuesDict.values())
                )
                self.instance.cursor.execute(ins_qry)

        self.instance.connection.commit()

    def insertGeo(self):
        data_to_insert = self.data_to_insert['result'] if 'result' in self.data_to_insert else self.data_to_insert

        for key, valuesDict in data_to_insert.items():
            try:
                insert_query = self.get_insert_query(self.instance.SRID != '4326', self.instance.IS_SDE, valuesDict)
                self.instance.cursor.execute(insert_query)
            except Exception as e :
                print(str(e))
                continue
        self.instance.connection.commit()

    def get_insert_query(self, needToConvert, is_sde, data):

        geom = data['geom'].wkt
        if needToConvert :
            geom = transformWKT(data['geom'], REGISTRY['SRID'].get(str(self.instance.SRID)), 'wgs84' )
        if is_sde :
            objid = self.instance.getLastObjectID(self.params.get('TABLE'))
            return self.sqls.get('INSERT').format(
                tablename=self.params.get('TABLE'),
                columns=', '.join(data['attr']._fields),
                values=", ".join("'{0}'".format(v.replace("'", "_")) for v in list(data['attr'])),
                geom=geom,
                OBJECTID=objid,
                srid=self.instance.SRID
            )
        return self.sqls.get('INSERT').format(
                    tablename=self.params.get('TABLE'),
                    columns=', '.join(data['attr']._fields),
                    values=", ".join("'{0}'".format(v.replace("'", "_")) for v in list(data['attr'])),
                    geom=geom,
                    srid=self.instance.SRID
                )











