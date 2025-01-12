from datetime import datetime

from sqlalchemy import Column, Integer, Date, SmallInteger, DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Human(Base):
    __tablename__ = "human"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Date = Column(Date, default=datetime.date(datetime.now()))
    respondent = Column(Integer, nullable=False)
    Sex = Column(SmallInteger, nullable=False)
    Age = Column(SmallInteger, nullable=False)
    Weight = Column(DOUBLE_PRECISION, nullable=False)
