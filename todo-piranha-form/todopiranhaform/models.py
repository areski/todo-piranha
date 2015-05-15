from sqlalchemy import (
    Column,
    Index,
    Integer,
    Boolean,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class TaskModel(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    taskname = Column(Text)
    status = Column(Boolean)

Index('task_index', TaskModel.taskname, unique=True, mysql_length=255)
