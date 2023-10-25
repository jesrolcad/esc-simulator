from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, Table
from sqlalchemy.orm import relationship
from app.db.database import Base

SongCeremony = Table('song_ceremony', Base.metadata, Column("id", Integer, primary_key=True), Column("song_id", Integer, ForeignKey('song.id')), 
Column("ceremony_id", Integer, ForeignKey('ceremony.id')))

class CountryEntity(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    code = Column(String(5), nullable=False)
    songs = relationship("SongEntity", back_populates="country")
    votings = relationship("VotingEntity", back_populates="country")

class SongEntity(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('country.id'))
    event_id = Column(Integer, ForeignKey('event.id'))
    title = Column(String(50), nullable=False)
    artist = Column(String(50), nullable=False)
    belongs_to_host_country = Column(Boolean, nullable=False)
    jury_potential_score = Column(Integer, nullable=False)
    televote_potential_score = Column(Integer, nullable=False)
    event = relationship("EventEntity", uselist=False)
    country = relationship("CountryEntity", back_populates="songs", uselist=False)
    ceremonies = relationship("CeremonyEntity", secondary=SongCeremony, back_populates="songs")
    votings = relationship("VotingEntity", back_populates="song")

class EventEntity(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    slogan = Column(String(50), nullable=False)
    host_city = Column(String(50), nullable=False)
    arena = Column(String(50), nullable=False)
    ceremonies = relationship("CeremonyEntity")

class CeremonyEntity(Base):
    __tablename__ = 'ceremony'
    id = Column(Integer, primary_key=True)
    ceremony_type_id = Column(Integer, ForeignKey("ceremony_type.id"))
    event_id = Column(Integer, ForeignKey("event.id"))
    date = Column(Date, nullable=True)
    event = relationship("EventEntity", back_populates="ceremonies", uselist=False)
    ceremony_type = relationship("CeremonyTypeEntity", back_populates="ceremonies", uselist=False)
    songs = relationship("SongEntity", secondary=SongCeremony, back_populates="ceremonies")
    votings = relationship("VotingEntity", back_populates="ceremony")

class CeremonyTypeEntity(Base):
    __tablename__ = 'ceremony_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    code = Column(String(5), nullable=False)
    ceremonies = relationship("CeremonyEntity", back_populates="ceremony_type")

# Country votes a song in a ceremony of an event, with a specific voting type (jury or televote)
class VotingEntity(Base):
    __tablename__ = 'voting'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("country.id"))
    song_id = Column(Integer, ForeignKey("song.id"))
    ceremony_id = Column(Integer, ForeignKey("ceremony.id"))
    voting_type_id = Column(Integer, ForeignKey("voting_type.id"))
    score = Column(Integer, nullable=False)
    country = relationship("CountryEntity", back_populates="votings", uselist=False)
    song = relationship("SongEntity", back_populates="votings", uselist=False)
    ceremony = relationship("CeremonyEntity", back_populates="votings", uselist=False)
    voting_type = relationship("VotingTypeEntity", uselist=False)
    

class VotingTypeEntity(Base):
    __tablename__ = 'voting_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
