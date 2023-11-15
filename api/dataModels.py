from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True)
    foldername = Column(String)
    images = relationship("Image", back_populates="folder")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)
    folder_id = Column(Integer, ForeignKey("folders.id"))
    folder = relationship("Folder", back_populates="images")


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("images.id"))
    folder_name = Column(String)
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

    def add_folder(self, foldername):
        session = self.create_session()
        new_folder = Folder(foldername=foldername)
        session.add(new_folder)
        session.commit()

    def add_image(self, filename, foldername):
        session = self.create_session()
        folder = session.query(Folder).filter_by(foldername=foldername).first()
        if not folder:
            folder = Folder(foldername=foldername)
            session.add(folder)
            session.commit()
        new_image = Image(filename=filename, folder=folder)
        session.add(new_image)
        session.commit()

    def add_grade(self, image_id, folder_name, grade):
        session = self.create_session()
        new_grade = Grade(image_id=image_id, folder_name=folder_name, grade=grade)
        session.add(new_grade)
        session.commit()
