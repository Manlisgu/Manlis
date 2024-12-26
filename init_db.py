from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(50), default='Medium')  # Low, Medium, High
    status = Column(String(50), default='Open')      # Open, In Progress, Resolved, Closed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# 初始化数据库
def init_db(db_path='sqlite:///issues.db'):
    engine = create_engine(db_path, echo=False)
    Base.metadata.create_all(engine)
    return engine

# 创建会话
def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
