# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TaskSetting(Base):
    __tablename__ = 'task_settings'
    __table_args__ = {'schema': 'nugget_bucket'}

    server_id = Column(BigInteger, primary_key=True)
    task_weekday = Column(Integer, nullable=False)
    task_monthly_day = Column(Integer, nullable=False)


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'nugget_bucket'}

    id = Column(BigInteger, nullable=False)
    id_server = Column(BigInteger, nullable=False)
    task_name = Column(String(128), nullable=False)
    interval_days = Column(Integer, nullable=False, server_default=text("1"))
    id_author = Column(BigInteger, primary_key=True)
    id_last_user = Column(BigInteger, nullable=False)
    completed = Column(Boolean, nullable=False, server_default=text("false"))
    id_current_user = Column(BigInteger, nullable=False)
