from typing import Literal
from pydantic import BaseModel
from app.logic.models import ceremony, song, country


class VotingType(BaseModel):
    id: int
    name: str
    code: str

class Voting(BaseModel):
    id: int
    score: Literal[1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
    voting_type: VotingType
    ceremony: ceremony.Ceremony
    song: song.Song
    country: country.Country






