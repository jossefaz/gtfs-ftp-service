import pyodbc
from Template.BaseClass import singleton

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
        self.connection = None
        self.cursor = None
        self.connectionString = None

    def getLastObjectID(self, table):
        query = 'DECLARE @myval int EXEC sde.next_rowid \'{}\', \'{}\', @myval OUTPUT SELECT @myval "Next RowID";'.format(self.username, table)
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            return row[0]


    def generateConnectionString(self) :
        if self.AD :
            return "DRIVER={SQL Server};SERVER=%s;DATABASE=%s;Trusted_Connection=yes" % (self.server, self.database)
        return "DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (self.server, self.database, self.username, self.password)
    def connect(self):
        self.connectionString = self.generateConnectionString()
        self.connection = pyodbc.connect(self.connectionString)
        self.cursor = self.connection.cursor()