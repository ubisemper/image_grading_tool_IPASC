from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    user = Column(String)
    grade = Column(Integer)
    graded_time = Column(DateTime, default=datetime.datetime.utcnow)

class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_all(self):
        Base.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()
    
    def add_file(self, filename):
        session = self.create_session()
        new_file = File(filename=filename)
        session.add(new_file)
        session.commit()

    def add_grade(self, filename, user, grade):
        session = self.create_session()
        new_grade = Grade(filename=filename, user=user, grade=grade)
        session.add(new_grade)
        session.commit()