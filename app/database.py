import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

Base = declarative_base()
engine = create_engine(os.getenv('SQL_CONNSTR'))
Session = sessionmaker(bind=engine)
db_session = Session()

def init_db():
    from . import models
    Base.metadata.create_all(engine)

def remove_db():
    from . import models
    models.ConsumeItem.__table__.drop()
    models.ConsumePlan.__table__.drop()
    models.ConsumeType.__table__.drop()
