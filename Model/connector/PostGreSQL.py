import psycopg2
from Template.BaseClass import singleton
from utils.control import skip_nones


class PGDB() :

    __metaclass__ = singleton

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
        self.connection = psycopg2.connect(
            host=self.host,
            user=self.username,
            password=self.password ,
            dbname=self.database
        )
        self.cursor = self.connection.cursor()

if __name__ == '__main__' :
    pass
    # con = PGDB('louis6', 'dev123', 'mot', 'localhost')
    # con.connect()
    # con.cursor.execute('CREATE TABLE testGeo')
