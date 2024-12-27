from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    created_issues = relationship('Issue', back_populates='creator', foreign_keys='Issue.creator_id')
    assigned_issues = relationship('Issue', back_populates='assignee', foreign_keys='Issue.assignee_id')

class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(50), default='Medium')  # Low, Medium, High
    status = Column(String(50), default='Open')      # Open, In Progress, Resolved, Closed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # 新增字段
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    cause_analysis = Column(Text, nullable=True)
    measure_definition = Column(Text, nullable=True)
    measure_deadline = Column(Date, nullable=True)

    # 关联用户
    creator_id = Column(Integer, ForeignKey('users.id'))
    assignee_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User', back_populates='created_issues', foreign_keys=[creator_id])
    assignee = relationship('User', back_populates='assigned_issues', foreign_keys=[assignee_id])

# 初始化数据库
def init_db(db_path='sqlite:///issues.db'):
    engine = create_engine(db_path, echo=False)
    Base.metadata.create_all(engine)
    return engine

# 创建会话
def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
