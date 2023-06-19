from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

SongCeremony = Table('song_ceremony', Base.metadata, Column("song_ceremony_id", Integer), Column("song_id", Integer, ForeignKey('song.id')), 
Column("ceremony_id", Integer, ForeignKey('ceremony.id')))

class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    code = Column(String(5), nullable=False)
    songs = relationship("Song", back_populates="country")
    votings = relationship("Voting", back_populates="country")

class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('country.id'))
    event_id = Column(Integer, ForeignKey('event.id'))
    title = Column(String(50), nullable=False)
    artist = Column(String(50), nullable=False)
    belongs_to_host_country = Column(Boolean, nullable=False)
    jury_potential_score = Column(Integer, nullable=False)
    televote_potential_score = Column(Integer, nullable=False)
    event = relationship("Event", uselist=False)
    country = relationship("Country", back_populates="songs", uselist=False)
    ceremonies = relationship("Ceremony", secondary=SongCeremony, back_populates="songs")
    votings = relationship("Voting", back_populates="song")

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
    ceremony_type = relationship("CeremonyType", back_populates="ceremonies", uselist=False)
    songs = relationship("Song", secondary=SongCeremony, back_populates="ceremonies")
    votings = relationship("Voting", back_populates="ceremony")

class CeremonyType(Base):
    __tablename__ = 'ceremony_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    code = Column(String(5), nullable=False)
    ceremonies = relationship("Ceremony", back_populates="ceremony_type")

class Voting(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("country.id"))
    song_id = Column(Integer, ForeignKey("song.id"))
    ceremony_id = Column(Integer, ForeignKey("ceremony.id"))
    score_type_id = Column(Integer, ForeignKey("score_type.id"))
    score = Column(Integer, nullable=False)
    country = relationship("Country", back_populates="votings", uselist=False)
    song = relationship("Song", back_populates="votings", uselist=False)
    ceremony = relationship("Ceremony", back_populates="votings", uselist=False)
    score_type = relationship("ScoreType", uselist=False)
    

class ScoreType(Base):
    __tablename__ = 'score_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
