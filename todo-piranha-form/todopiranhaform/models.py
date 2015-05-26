from sqlalchemy import (
    Column,
    Index,
    Integer,
    Boolean,
    Text,
    Unicode,      # <- will provide unicode field,
    # UnicodeText,  # <- will provide unicode text field,
    DateTime      # <- time abstraction field,
    )
from sqlalchemy.ext.declarative import declarative_base
import datetime

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    taskname = Column(Text)
    # status: True=Active, False=Completed
    status = Column(Boolean)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)


Index('task_index', Task.taskname, unique=True, mysql_length=255)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)
