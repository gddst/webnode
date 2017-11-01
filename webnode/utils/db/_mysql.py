import traceback

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.session import sessionmaker

from resbot.common.configuration import Configuration


class MysqlManager(object):
        
    
    DBEngine = None
    DBSession = None
    dbSession = None
    
    TableBase = declarative_base()
    __TESTSERVICE_ENGINE = None
    __TESTSERVICE_SESSION = None

    MYSQL_ENGINE_SPEC = 'mysql+mysqldb://{0}:{1}@{2}/{3}?charset=utf8'

    @staticmethod
    def initial( user , password , host ,  instance ):
        MysqlManager.DBEngine = create_engine(
            ( MysqlManager.MYSQL_ENGINE_SPEC.format(user, password, host, instance) ), 
            pool_recycle = 14400 , echo = False 
        )
        MysqlManager.DBSession = sessionmaker( MysqlManager.DBEngine )

    @staticmethod
    def get_testservice_engine():        

        if MysqlManager.__TESTSERVICE_ENGINE == None:
            conf = Configuration.load_section( 'database' )
            user     = conf['user'] 
            password = conf['password'] 
            endpoint = "{}:{}".format(conf['host'], conf['port'])
            instance = conf['instance']
            MysqlManager.__TESTSERVICE_ENGINE = MysqlManager.DBEngine = create_engine( 
                MysqlManager.MYSQL_ENGINE_SPEC.format(user, password, endpoint, instance), 
                pool_recycle = 14400 , echo = False 
            )            
        return MysqlManager.__TESTSERVICE_ENGINE
    

    @staticmethod
    def get_testservice_session():
        if MysqlManager.__TESTSERVICE_SESSION == None:
            MysqlManager.__TESTSERVICE_SESSION = sessionmaker( 
                bind = MysqlManager.get_testservice_engine(),
                expire_on_commit=False
            )
            
        return MysqlManager.__TESTSERVICE_SESSION()

    @staticmethod
    def getDBEngine( engine_spec , is_echo ):
        return create_engine( engine_spec , pool_recycle = 14400 , echo = is_echo )

    @staticmethod
    def getTableBase():
        if MysqlManager.TableBase==None:
            MysqlManager.TableBase = declarative_base()
        return MysqlManager.TableBase    
    
    @staticmethod
    def query_all(query, db_session, try_time=2):

        for i in range(try_time):
            try:
                return query.all()
            except:
                print traceback.print_exc()
                db_session.rollback()