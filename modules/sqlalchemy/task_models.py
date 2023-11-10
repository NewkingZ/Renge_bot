# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Integer, String, text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Server(Base):
    __tablename__ = 'servers'
    __table_args__ = {'schema': 'nugget_bucket'}

    id_server = Column(BigInteger, primary_key=True)
    server_name = Column(String(128), nullable=False)
    announcement_channel = Column(BigInteger, nullable=False)
    announcement_time = Column(BigInteger, nullable=False, server_default=text("0"))
    task_role = Column(BigInteger, nullable=False, server_default=text("0"))


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'nugget_bucket'}

    id = Column(BigInteger, primary_key=True)
    id_server = Column(BigInteger, nullable=False)
    task_name = Column(String(128), nullable=False)
    id_author = Column(BigInteger, nullable=False, server_default=text("0"))
    id_last_user = Column(BigInteger, nullable=False, server_default=text("0"))
    id_current_user = Column(BigInteger, nullable=False, server_default=text("0"))
    completed = Column(Boolean, nullable=False, server_default=text("false"))
    interval_days = Column(Integer, nullable=False, server_default=text("1"))
    duration = Column(Integer, nullable=False, server_default=text("0"))
    deadline = Column(Integer, nullable=False, server_default=text("7"))
    valid_users = Column(String(128), nullable=False)
    date_last_issued = Column(DateTime, nullable=False)


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'nugget_bucket'}

    id_user = Column(BigInteger, primary_key=True)
    experience = Column(BigInteger, nullable=False, server_default=text("0"))
