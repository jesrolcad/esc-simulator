from typing import List
from pydantic import BaseModel
from app.logic.models import song, voting

class Country(BaseModel):
    id: int = 0
    name: str = None
    code: str = None
    songs: List[song.Song] =  []
    votings: List[voting.Voting] = []