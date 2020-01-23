import pyodbc
from Template.BaseClass import Dal

class SqlServerDB():
    __metaclass__ = Dal
    def __init__(self, server, dbname, user, password):
        self.server = server
        self.database = dbname
        self.username = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pyodbc.connect("DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s"
                                         % (self.server, self.database, self.username, self.password))
        self.cursor = self.connection.cursor()