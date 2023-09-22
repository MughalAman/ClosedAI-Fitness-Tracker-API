import sqlalchemy as sa
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

from ..settings import SETTINGS

SQLALCHEMY_DATABASE_URL = SETTINGS.db_connection_string

engine = sa.create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()
