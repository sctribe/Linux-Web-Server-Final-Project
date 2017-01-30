import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))

class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)

    @property
    def serialize(self):
        #returns object data in easily serializeable format
        return {
            'id' : self.id,
            'name' : self.name,
            'user_id' : self.user_id
        }

class Songs(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key = True)
    name =Column(String(100), nullable = False)
    album = Column(String(100))
    artist = Column(String(35))
    year = Column(Integer(4))
    length = Column(String(6))
    genre_id = Column(Integer,ForeignKey('genre.id'))
    genre = relationship(Genre, cascade = "all, delete-orphan", single_parent = True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)

    @property
    def serialize(self):
        #returns object data in easily serializeable format
        return {
            'id' : self.id,
            'name' : self.name,
            'album' : self.album,
            'artist' : self.artist,
            'year' : self.year,
            'length' : self.length,
            'user_id' : self.user_id
        }


engine = create_engine('sqlite:///musicgenreswithusers.db')
Base.metadata.create_all(engine)