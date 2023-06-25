from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.logic.models import event, song, voting

class CeremonyType(BaseModel):
    id: int = 0
    name: str
    code: str


class Ceremony(BaseModel):
    id: int = 0
    date: datetime
    ceremony_type: CeremonyType
    event: event.Event
    songs: List[song.Song] = []
    votings: List[voting.Voting] = []

