from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from backend.config.config import config
from backend.utils.errors import InternalServerError, DatabaseError

Base = declarative_base()

class DBConn:

    _instance = None
    __db_url: str
    session_local: sessionmaker
    engine = None

    def __init__(self,):
        self.__db_url = "sqlite:///mydatabase.db"
        
    def setup_server(self):
        engine = create_engine(self.__db_url, connect_args={}, future=True)
        self.engine = engine
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
        self.__create_db_if_not_exists()
        self.__create_all(engine)

    def __create_db_if_not_exists(self):
        try:
            if not database_exists(self.__db_url):
                create_database(self.__db_url)
                print("Database Created Successfully!!")
        except Exception as error:
            raise InternalServerError("There has been a problem in checking the connection for the db.") from error

    def __create_all(self, engine):
        Base.metadata.create_all(bind=engine)

    def get_db_url(self):
        return self.__db_url

    def get_db(self):
        try:
            db = self.session_local()
            return db
        except Exception as error:
            raise DatabaseError("Error while connecting to database!!") from error

    def close_all_connections(self):
        if self.engine is not None:
            self.engine.dispose()

conn = DBConn()
conn.setup_server()
