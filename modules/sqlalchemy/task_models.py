# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Server(Base):
    __tablename__ = 'servers'
    __table_args__ = {'schema': 'nugget_bucket'}

    id_server = Column(BigInteger, primary_key=True)
    announcement_channel = Column(BigInteger, nullable=False)
    announcement_time = Column(BigInteger, nullable=False, server_default=text("0"))


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'nugget_bucket'}

    id_server = Column(BigInteger, nullable=False)
    id = Column(BigInteger, primary_key=True)
    task_name = Column(String(128), nullable=False)
    interval_days = Column(Integer, nullable=False, server_default=text("1"))
    id_author = Column(String(128), nullable=False)
    id_last_user = Column(String(128), nullable=False)
    id_current_user = Column(String(128), nullable=False)
    completed = Column(Boolean, nullable=False, server_default=text("false"))
    duration = Column(Integer, nullable=False, server_default=text("0"))
    deadline = Column(Integer, nullable=False, server_default=text("7"))
    valid_users = Column(String(128), nullable=False)


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'nugget_bucket'}

    id_user = Column(BigInteger, primary_key=True)
    experience = Column(BigInteger, nullable=False, server_default=text("0"))
