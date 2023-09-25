# import sqlalchemy.orm as orm

# from datetime import datetime

from . import database

# from . import models
# from . import schemas


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)


def get_database():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
