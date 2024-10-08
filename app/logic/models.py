from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel

class Song(BaseModel):
    id: int = None
    title: str
    artist: str
    belongs_to_host_country: bool
    jury_potential_score: Literal[1,2,3,4,5,6,7,8,9,10]
    televote_potential_score: Literal[1,2,3,4,5,6,7,8,9,10]
    event: 'Event' = None
    country: 'Country' = None
    ceremonies: List['Ceremony'] = []
    votings: List['Voting'] = []

class Event(BaseModel):
    id: int = None
    year: int = None
    slogan: str = None
    host_city: str = None
    arena: str = None
    ceremonies: List['Ceremony'] = []


class Country(BaseModel):
    id: int = None
    name: str = None
    code: str = None
    songs: List[Song] =  []
    votings: List['Voting'] = []


class CeremonyType(BaseModel):
    id: int = None
    name: str
    code: str = None


class Ceremony(BaseModel):
    id: int = None
    date: datetime = None
    ceremony_type: CeremonyType
    event: Event = None
    songs: List[Song] = []
    votings: List['Voting'] = []


class VotingType(BaseModel):
    id: int = None
    name: str

class Voting(BaseModel):
    id: int = None
    score: Literal[1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
    voting_type: VotingType
    ceremony: Ceremony = None
    song: Song
    country: Country

class Participant(BaseModel):
    country_id: int
    song_id: int
    participant_info: str

class ParticipantResult(Participant):
    total_score: int
    jury_score: int
    televote_score: int

class SimulationCeremonyResult(BaseModel):
    ceremony_id: int
    ceremony_type: CeremonyType
    results: List[ParticipantResult] = []

class SimulationSong(BaseModel):
    song_id: int
    country_id: int
    jury_potential_score: int
    televote_potential_score: int

    