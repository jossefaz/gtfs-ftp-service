import sqlalchemy as db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, instrumentation
from sqlalchemy import MetaData, Table, func, and_, or_, not_



if __name__ == '__main__' :


        engine = db.create_engine("mysql+pymysql://root:dev123@localhost:3306/sde")

        Base = automap_base()
        Base.prepare(engine, reflect=True)
        print(Base.classes.keys())


        '''SELECT ALL'''
        # query = session.query(table_list['motroutes']).limit(3)
        # for i in query :
        #     print(i.route_id)
        '''FILTER BY'''
        # table = metadata.tables['motroutes']
        # res = session.query(table).filter_by(route_id=1).first()
        # print(count)
        '''FILTER'''
        # table = metadata.tables['motroutes']
        # res = session.query(table).filter(table.c.route_id==1).first()
        # print(count)
        '''LIKE'''
        # table = metadata.tables['motroutes']
        # res = session.query(table).filter(table.c.route_id.like('%1%'))
        # for route in res :
        #     print(route)
        '''CONJUNCTION'''
        # table = metadata.tables['motroutes']
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






