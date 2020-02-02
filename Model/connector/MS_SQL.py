import pyodbc
from Template.BaseClass import singleton
import urllib
from sqlalchemy import create_engine

class SqlServerDB():
    __metaclass__ = singleton
    def __init__(self, *args, **kwargs):
        self.server = kwargs.get('config').get('SERVER')
        self.database = kwargs.get('config').get('INSTANCE')
        self.username = kwargs.get('config').get('USER')
        self.password = kwargs.get('config').get('PSWD')
        self.AD = kwargs.get('config').get('AD')
        self.IS_SDE = kwargs.get('config').get('IS_SDE')
        self.SRID = kwargs.get('config').get('SRID')
        self.sql = kwargs.get('config').get('SQL')
        self.connection = None
        self.cursor = None
        self.driver = 'ODBC Driver 17 for SQL Server'
        self.connectionString = None

    def getLastObjectID(self, table):
        query = 'DECLARE @myval int EXEC sde.next_rowid \'{}\', \'{}\', @myval OUTPUT SELECT @myval "Next RowID";'.format(self.username, table)
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            return row[0]

    def create_engine(self):
        params = urllib.parse.quote_plus(self.connectionString)
        return create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, fast_executemany=True)

    def generateConnectionString(self) :
        if self.AD :
            return "DRIVER=%s;SERVER=%s;DATABASE=%s;Trusted_Connection=yes" % (self.driver, self.server, self.database)
        return "DRIVER=%s;SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (self.driver, self.server, self.database, self.username, self.password)
    def connect(self):
        self.connectionString = self.generateConnectionString()
        self.connection = pyodbc.connect(self.connectionString, autocommit=True)
        self.cursor = self.connection.cursor()
        self.cursor.fast_executemany = True