
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from services.authorization_service.src.config.variables import config
from services.common.errors.error_functions import DatabaseError, InternalServerError

Base = declarative_base()

class PostgresConn:

    _instance = None
    __db_url: str
    session_local: sessionmaker
    engine = None

    def __init__(
        self,
        db_name: str,
        credentials: dict,
        host: str = "localhost",
        port=5432,
    ):
        username = credentials["username"]
        password = credentials["password"]
        self.__db_url = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"

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

db_credentials = {"username": config.DB_USERNAME, "password": config.DB_PASSWORD}
postgres_conn = PostgresConn(
    db_name=config.DB_DATABASE,
    host=config.DB_HOST,
    port=config.DB_PORT,
    credentials=db_credentials,
)
