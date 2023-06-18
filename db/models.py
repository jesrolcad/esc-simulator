from sqlalchemy import Column, ForeignKey, Integer, String, Date, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

song_ceremony = Table('song_ceremony', Base.metadata, Column("song_ceremony_id", Integer), Column("song_id", Integer, ForeignKey('song.id')), 
Column("ceremony_id", Integer, ForeignKey('ceremony.id')))

class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    code = Column(String(5), nullable=False)
    songs = relationship("Song")
    votings = relationship("Voting")

class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('country.id'))
    title = Column(String(50), nullable=False)
    artist = Column(String(50), nullable=False)
    jury_potential_score = Column(Integer, nullable=False)
    televote_potential_score = Column(Integer, nullable=False)
    ceremonies = relationship("Ceremony", secondary=song_ceremony, back_populates="songs")
    votes = relationship("Voting")

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    slogan = Column(String(50), nullable=False)
    host_city = Column(String(50), nullable=False)
    arena = Column(String(50), nullable=False)
    ceremonies = relationship("Ceremony")

class Ceremony(Base):
    __tablename__ = 'ceremony'
    id = Column(Integer, primary_key=True)
    ceremony_type_id = Column(Integer, ForeignKey("ceremony_type.id"))
    event_id = Column(Integer, ForeignKey("event.id"))
    date = Column(Date, nullable=True)
    songs = relationship("Song", secondary=song_ceremony, back_populates="ceremonies")
    votings = relationship("Voting")

class CeremonyType(Base):
    __tablename__ = 'ceremony_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    code = Column(String(5), nullable=False)
    ceremonies = relationship("Ceremony")

class Voting(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("country.id"))
    song_id = Column(Integer, ForeignKey("song.id"))
    ceremony_id = Column(Integer, ForeignKey("ceremony.id"))
    score_type = Column(Integer, ForeignKey("score_type.id"))
    score = Column(Integer, nullable=False)

class ScoreType(Base):
    __tablename__ = 'score_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
