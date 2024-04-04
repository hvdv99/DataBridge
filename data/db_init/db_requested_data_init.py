from datetime import datetime, date, time
import os
import pandas as pd
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time, Date, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class RequestedDataInit(Base):
    __tablename__ = 'requested_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String)
    email = Column(String)
    subject = Column(String)
    sql_code = Column(String)
    column_description_dict = Column(String)
    date_created = Column(DateTime, default=datetime.now())
    accepted_bool = Column(Integer, default=0)
    date_accepted_or_rejected = Column(DateTime)
    delivered_bool = Column(Integer, default=0)


engine = create_engine('sqlite:///../PostNL_Requested_Data.sqlite')
Base.metadata.create_all(engine)  # Create tables

DBSession = sessionmaker(bind=engine)
session = DBSession()