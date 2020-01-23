
# -*- coding: utf-8 -*-
from Configuration.Config import Config

class DAL() :

    def __init__(self, Instance_Name):
        self.instance_name = Instance_Name
        self.connection = None

    def connect(self):
        config = self.getConfig()
        connector = getattr(self, config.get('TECH'))(config)
        return connector

    def getConfig(self) :
        return Config().get_property('DB').get(self.instance_name)

    def MS_SQL(self, config):
        try :
            from Model.connector.MS_SQL import SqlServerDB
        except ImportError as e :
            print("Cannot get SQL server connector : " + str(e))
            return None
        conn = SqlServerDB(config.get('SERVER'), config.get('INSTANCE'), config.get('USER'), config.get('PSWD'))
        conn.connect()
        return conn

    def MYSQL(self, config):
        try :
            from Model.connector.MySQL import MySQLDB
        except ImportError as e :
            print("Cannot get SQL server connector : " + str(e))
            return None
        conn = MySQLDB(config.get('USER'),  config.get('PSWD'), config.get('DB'), config.get('HOST'), config.get('PORT'))
        conn.connect()
        return conn

    def POSTGRESQL(self, config) :
        try :
            from Model.connector.PostGreSQL import PGDB
        except ImportError as e :
            print("Cannot get SQL server connector : " + str(e))
            return None
        conn = PGDB(config.get('USER'),  config.get('PSWD'), config.get('DB'), config.get('HOST'), config.get('PORT'))
        conn.connect()
        return conn









if __name__ == '__main__' :
    pass


        # engine = db.create_engine("mysql+pymysql://root:dev123@localhost:3306/sde")
        #
        # Base = automap_base()
        # Base.prepare(engine, reflect=True)
        # print(Base.classes.keys())


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






