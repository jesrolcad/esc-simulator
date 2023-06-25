from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.logic.models import event, song, voting

class CeremonyType(BaseModel):
    id: int
    name: str
    code: str
    ceremonies: List['Ceremony']


class Ceremony(BaseModel):
    id: int
    date: datetime
    ceremony_type: CeremonyType
    event: event.Event
    songs: List[song.Song]
    votings: List[voting.Voting]

