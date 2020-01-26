# -*- coding: UTF-8 -*-
from utils.path import *
import os
import logging
from Model.DAL import DAL




class DAO() :

    __slots__ = [ "logger","registry", "params","query", "instance", "data_to_insert"]

    def __init__(self, connection_parameters, query=None):
        self.logger = logging.getLogger(__name__)
        self.params = connection_parameters
        self.query = query
        self.instance = None
        self.data_to_insert = None

    def exec(self, args):
        connector = DAL(self.params.get('INSTANCE'))
        if connector :
            if args :
                self.data_to_insert = args
            self.instance = connector.connect()
            action = getattr(self, self.params.get('ACTION'))
            action()



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
                insert_query = """INSERT INTO {tablename} ({columns}, geom) VALUES ({values},ST_GeomFromText('{geom}', 4326))""".format(
                    tablename=self.params.get('TABLE'),
                    columns=', '.join(valuesDict['attr']._fields),
                    values=", ".join("'{0}'".format(v.replace("'", "_")) for v in list(valuesDict['attr'])),
                    geom=valuesDict['geom'].wkt
                )

                self.instance.cursor.execute(insert_query)
            except Exception as e :
                print(str(e))
                continue
        self.instance.connection.commit()





