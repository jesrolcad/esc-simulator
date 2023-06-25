from typing import List
from pydantic import BaseModel
from app.logic.models import song, voting

class Country(BaseModel):
    id: int
    name: str
    code: str
    songs: List[song.Song]
    votings: List[voting.Voting]