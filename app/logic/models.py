from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel

class Song(BaseModel):
    id: int = 0
    title: str
    artist: str
    belongs_to_host_country: bool
    jury_potential_score: Literal[1,2,3,4,5,6,7,8,9,10]
    televote_potential_score: Literal[1,2,3,4,5,6,7,8,9,10]
    event: 'Event'
    country: 'Country'
    ceremonies: List['Ceremony'] = []
    votings: List['Voting'] = []

class Event(BaseModel):
    id: int = 0
    year: int
    slogan: str
    host_city: str
    arena: str
    ceremonies: List['Ceremony'] = []


class Country(BaseModel):
    id: int = 0
    name: str = None
    code: str = None
    songs: List[Song] =  []
    votings: List['Voting'] = []


class CeremonyType(BaseModel):
    id: int = 0
    name: str
    code: str


class Ceremony(BaseModel):
    id: int = 0
    date: datetime
    ceremony_type: CeremonyType
    event: Event
    songs: List[Song] = []
    votings: List['Voting'] = []


class VotingType(BaseModel):
    id: int
    name: str
    code: str

class Voting(BaseModel):
    id: int
    score: Literal[1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
    voting_type: VotingType
    ceremony: Ceremony
    song: Song
    country: Country
