from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser

class DBInstance(object):
    
    def __init__(self, conf):
        config=ConfigParser()
        config.read(conf)
                
        conn_stat='mysql+mysqldb://{user}:{password}@{host}/{instance}?charset=utf8'.format(
            user=config.get('mysql', 'user'),
            password=config.get('mysql', 'password'),
            host=config.get('mysql', 'host'),
            instance=config.get('mysql', 'instance')
        )
        self.__db_engine = create_engine(conn_stat, pool_recycle=14400, echo=False)
        self.__session_maker= sessionmaker( self.__db_engine )
        self.table_base=declarative_base()
        
    @property
    def session(self):
        return self.__session_maker()
            
    @property
    def Table(self):
        return self.table_base
    
    def create_tables(self):
        self.table_base.metadata.create_all(self.__db_engine)
    
    def query(self,table, **filter):
        new_session=self.__session_maker()
        try:
            print(filter)
            return new_session.query(table).filter_by(**filter).all()
        finally:
            if new_session:
                new_session.close()

    def add_obj(self, obj):
        new_session=self.__session_maker()
        try:
            new_session.add(obj)
            new_session.commit()
        finally:
            if new_session:
                new_session.close()
                
    def update_obj(self, table, obj, **filter):
        pass


    def delete_obj(self, table, **filter):
        new_session=self.__session_maker()
        try:
            obj=new_session.query(table).filter_by(**filter).first()
            new_session.delete(obj)
            new_session.commit()
        finally:
            if new_session:
                new_session.close()
     
        
        