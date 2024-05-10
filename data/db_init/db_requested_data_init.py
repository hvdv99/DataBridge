from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RequestedDataInit(Base):
    """
    The class for the requested data table in the database. This table is for keeping track of the made requests
    """
    __tablename__ = 'requested_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String)
    email = Column(String)
    subject = Column(String)
    sql_code = Column(String)
    columns = Column(String)
    date_created = Column(Date, default=datetime.today())
    date_accepted_or_rejected = Column()
    delivered_bool = Column(Integer, default=0)
    comments = Column(String)


engine = create_engine('sqlite:///../PostNL_Requested_Data.sqlite')
Base.metadata.create_all(engine)  # Create tables

DBSession = sessionmaker(bind=engine)

session = DBSession()
