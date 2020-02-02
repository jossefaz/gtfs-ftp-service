# -*- coding: UTF-8 -*-
import urllib

from utils.path import *
import os
import json
import logging
from Model.DAL import DAL
from utils.geometry import transformWKT
from registry.DAO import REGISTRY
from utils.control import printProgressBar, count_nested_dict
import time
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool






class DAO() :

    __slots__ = [ "logger","registry", "params","query", "instance", "data_to_insert", "sqls"]

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
            self.callbackQueries(self.params.get('BEFORE'))
            self.executeMain()
            self.callbackQueries(self.params.get('AFTER'))

    def callbackQueries(self, queries):
        if queries :
            for q in queries:
                if isinstance(q, str):
                    query = self.instance.sql.get(q)
                    self.executeQuery(query)
                elif isinstance(q, dict):
                    query = self.instance.sql.get(q.get('NAME'))
                    self.executeQuery(query, q.get('PARAMETERS'))
    def executeQuery(self, query, params=None):
        if params :
            query = query.format(*params)
        self.instance.cursor.execute(query)
        self.instance.connection.commit()

    def executeMain(self):
        for q in self.params.get('MAIN'):
            if isinstance(q, str):
                main = getattr(self, q)
                main()
            elif isinstance(q, dict):
                sqlFunc = getattr(self, q.get('NAME'))
                sqlFunc(config=q.get('PARAMETERS'))


    def updateWithDF(self, *args, **kwargs):
        config = kwargs.get('config')
        new_df = pd.read_sql_query(self.instance.sql.get(config.get('SQL')), self.instance.connection)
        print(len(new_df))


    def updateAll(self, *args, **kwargs):
        config = kwargs.get('config')
        l = len(self.data_to_insert['ids'].get(config.get('ID_FIELD')))
        progressIndex = 0
        progress_prefix = 'Data Update Progress:'
        progress_suffix = 'Updated in DB'
        printProgressBar(0, l, prefix=progress_prefix, suffix=progress_suffix, length=50)
        firstSQL = config.get('SQL')
        if firstSQL :
            firstSQL = self.instance.sql.get(firstSQL)
        where =  config.get('WHERE')
        FIELD_TO_UPDATE = config.get('FIELD_TO_UPDATE')
        ids_to_update = self.data_to_insert['ids'] if 'ids' in self.data_to_insert else self.data_to_insert

        for id in ids_to_update.get(config.get('ID_FIELD')) :
            sql = ''
            getTempResSQL = firstSQL.format(id)

            self.instance.cursor.execute(getTempResSQL)
            value = None
            for row in self.instance.cursor.fetchall():
                 value = row[0] if row[0] is not None else ''
            sql = '''UPDATE {} SET {}  = \'{}\' WHERE {} = {}'''.format(self.params.get('TABLE'), FIELD_TO_UPDATE, value, config.get('ID_FIELD'), id)
            if where :
                sql = sql + ' AND ' + where
            self.instance.cursor.execute(sql)
            progressIndex += 1
            printProgressBar(progressIndex, l, prefix=progress_prefix, suffix=progress_suffix, length=50)
        self.instance.connection.commit()






    def insert(self):
        engine = self.instance.create_engine()
        data_to_insert = self.data_to_insert['result'] if 'result' in self.data_to_insert else self.data_to_insert
        @event.listens_for(engine, 'before_cursor_execute')
        def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
            if executemany:
                cursor.fast_executemany = True
        df = pd.DataFrame(data_to_insert)
        try :
            df.to_sql(name=self.params.get('TABLE'),
                      con=engine,
                      index=False,
                      if_exists='replace',
                      schema="dbo"
                      )
        except Exception as e :
            self.logger.error(str(e))
        print("Alphanumeric Data inserted")

        # l = len(data_to_insert)
        # progressIndex = 0
        # progress_prefix = 'Data Insert Progress:'
        # progress_suffix = 'Inserted to DB'
        # printProgressBar(0, l, prefix=progress_prefix, suffix=progress_suffix, length=50)
        #
        #
        # for key, listvalues in data_to_insert.items() :
        #     for valuesDict in listvalues:
        #         for key, val in valuesDict.items() :
        #             try:
        #                 valuesDict[key] = int(val)
        #             except:
        #                 try :
        #
        #                     valuesDict[key] = val.replace("'", '"')
        #                 except :
        #                     continue
        #
        #         try :
        #
        #             ins_qry = "INSERT INTO {tablename} ({columns}) VALUES {values}".format(
        #                 tablename=self.params.get('TABLE'),
        #                 columns=', '.join(valuesDict.keys()),
        #                 values=tuple(valuesDict.values())
        #             )
        #             self.instance.cursor.execute(ins_qry)
        #
        #         except:
        #             try :
        #                 ins_qry = "INSERT INTO {tablename} ({columns}) VALUES {values}".format(
        #                     tablename=self.params.get('TABLE'),
        #                     columns=', '.join(valuesDict.keys()),
        #                     values=tuple(json.dumps(s, ensure_ascii=False) for s in valuesDict.values())
        #                 )
        #                 self.instance.cursor.execute(ins_qry)
        #             except Exception as e :
        #                 print(str(e))
        #                 continue
        #     progressIndex += 1
        #     printProgressBar(progressIndex, l, prefix=progress_prefix, suffix=progress_suffix, length=50)
        #     time.sleep(0.1)
        #     self.instance.connection.commit()

    def insertGeo(self):
        data_to_insert = self.data_to_insert['result'] if 'result' in self.data_to_insert else self.data_to_insert
        l = len(data_to_insert)
        progressIndex = 0
        progress_prefix = 'Data Insert Progress:'
        progress_suffix = 'Inserted to DB'
        printProgressBar(0, l, prefix=progress_prefix, suffix=progress_suffix, length=50)

        for valuesDict in data_to_insert:
            try:
                insert_query = self.get_insert_query(self.instance.SRID != '4326', self.instance.IS_SDE, valuesDict)
                self.instance.cursor.execute(insert_query)
                progressIndex +=1
                printProgressBar(progressIndex, l, prefix=progress_prefix, suffix=progress_suffix, length=50)
                time.sleep(0.1)
            except Exception as e :
                print(str(e))
                continue
        self.instance.connection.commit()

    def get_insert_query(self, needToConvert, is_sde, data):

        geom = data.GEOM.wkt
        columns = [f for f in data._fields if f not in 'GEOM']
        values = ["'{0}'".format(v.replace("'", "_")) for v in list(data) if isinstance(v, str)]
        if needToConvert :
            geom = transformWKT(data.GEOM, REGISTRY['SRID'].get(str(self.instance.SRID)), 'wgs84' )
        if is_sde :
            objid = self.instance.getLastObjectID(self.params.get('TABLE'))
            return self.instance.sql.get('INSERT').format(
                tablename=self.params.get('TABLE'),
                columns=', '.join(columns),
                values=", ".join(values),
                geom=geom,
                OBJECTID=objid,
                srid=self.instance.SRID
            )
        return self.instance.sql.get('INSERT').format(
                    tablename=self.params.get('TABLE'),
                    columns=', '.join(data._fields),
                    values=", ".join("'{0}'".format(v.replace("'", "_")) for v in list(data)),
                    geom=geom,
                    srid=self.instance.SRID
                )











