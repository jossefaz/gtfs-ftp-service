import sqlalchemy as db
from sqlalchemy.ext.automap import automap_base

# -*- coding: utf-8 -*-
from Configuration.Config import Config
import pyodbc
import mysql
from utils.control import skip_nones

class Dal(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Dal, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



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

class MySQLDB() :
    @skip_nones
    def __init__(self, user, password, dbname, host='127.0.0.1', port=3306):
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


def SQLServerConnector(Instance_Name):
    config = Config.get('DB').get(Instance_Name)
    conn = SqlServerDB(config.get('SERVER'), config.get('INSTANCE'), config.get('USER'), config.get('PSWD'))
    conn.connect()
    return conn

def MySQLConnector(Instance_Name):
    config = Config.get('DB').get(Instance_Name)
    conn = MySQLDB(config.get('USER'),  config.get('PSWD'), config.get('DB'), config.get('HOST'), config.get('PORT'))
    conn.connect()
    return conn








if __name__ == '__main__' :


        engine = db.create_engine("mysql+pymysql://root:dev123@localhost:3306/sde")

        Base = automap_base()
        Base.prepare(engine, reflect=True)
        print(Base.classes.keys())


        '''SELECT ALL'''
        # query = session.query(table_list['motroutes')).limit(3)
        # for i in query :
        #     print(i.route_id)
        '''FILTER BY'''
        # table = metadata.tables['motroutes')
        # res = session.query(table).filter_by(route_id=1).first()
        # print(count)
        '''FILTER'''
        # table = metadata.tables['motroutes')
        # res = session.query(table).filter(table.c.route_id==1).first()
        # print(count)
        '''LIKE'''
        # table = metadata.tables['motroutes')
        # res = session.query(table).filter(table.c.route_id.like('%1%'))
        # for route in res :
        #     print(route)
        '''CONJUNCTION'''
        # table = metadata.tables['motroutes')
        # res = session.query(table).filter(and_(
        #                                   table.c.route_id.between(5, 50),
        #                                     table.c.route_long_name.contains('מרכזית')
        # )
        # )
        # for route in res :
        #     print(route)
        '''UPDATE'''
        # table = Base.classes.motroutes
        # session = sessionmaker(bind=engine)()
        # res = session.query(table).filter(and_(
        #                                   table.route_id.between(5, 50),
        #                                     table.route_long_name.contains('מרכזית')
        # )
        # )
        # for route in res :
        #     route.route_long_name = "INVALID"
        # session.flush()
        # res = session.query(table).filter(and_(
        #                                   table.route_id.between(5, 50),
        #                                     table.route_long_name.contains('INVALID')
        # )
        # )
        # for route in res :
        #     print(route.route_long_name)






