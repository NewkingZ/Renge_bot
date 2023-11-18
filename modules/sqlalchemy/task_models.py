# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Server(Base):
    __tablename__ = 'servers'
    __table_args__ = {'schema': 'nugget_bucket'}

    id_server = Column(BigInteger, primary_key=True)
    announcement_channel = Column(BigInteger, nullable=False)
    announcement_time = Column(BigInteger, nullable=False, server_default=text("0"))
    server_name = Column(String(128), nullable=False)
    task_role = Column(BigInteger, nullable=False, server_default=text("0"))


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'nugget_bucket'}

    id_user = Column(BigInteger, primary_key=True)
    experience = Column(BigInteger, nullable=False, server_default=text("0"))


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'nugget_bucket'}

    id_server = Column(ForeignKey('nugget_bucket.servers.id_server'), nullable=False)
    id = Column(BigInteger, primary_key=True)
    task_name = Column(String(128), nullable=False)
    interval_days = Column(Integer, nullable=False, server_default=text("1"))
    completed = Column(Boolean, nullable=False, server_default=text("false"))
    duration = Column(Integer, nullable=False, server_default=text("0"))
    deadline = Column(Integer, nullable=False, server_default=text("7"))
    valid_users = Column(String(128), nullable=False)
    id_current_user = Column(ForeignKey('nugget_bucket.users.id_user'), nullable=False, server_default=text("0"))
    id_last_user = Column(ForeignKey('nugget_bucket.users.id_user'), nullable=False, server_default=text("0"))
    id_author = Column(ForeignKey('nugget_bucket.users.id_user'), nullable=False, server_default=text("0"))
    date_last_issued = Column(DateTime, nullable=True)

    user = relationship('User', primaryjoin='Task.id_author == User.id_user')
    user1 = relationship('User', primaryjoin='Task.id_current_user == User.id_user')
    user2 = relationship('User', primaryjoin='Task.id_last_user == User.id_user')
    server = relationship('Server')
