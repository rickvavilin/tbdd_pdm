__author__ = 'Aleksandr Vavilin'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import DDL
from . import models


def init_schema(connection_string):
    engine = create_engine(connection_string)
    models.Base.metadata.create_all(engine)
