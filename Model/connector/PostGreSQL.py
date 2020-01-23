import psycopg2
from Template.BaseClass import Dal
from utils.control import skip_nones


class PGDB() :

    __metaclass__ = Dal

    @skip_nones
    def __init__(self, user, password, dbname, host='127.0.0.1', port=5432):
        self.host = host
        self.port = port
        self.username = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.database = dbname

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            passwd=self.password ,
            database=self.database
        )
        self.cursor = self.connection.cursor()