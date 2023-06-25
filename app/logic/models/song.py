from typing import List, Literal
from pydantic import BaseModel
from app.logic.models import country, ceremony, voting, event

class Song(BaseModel):
    id: int = 0
    title: str
    artist: str
    belongs_to_host_country: bool
    jury_potential_score: Literal[1,2,3,4,5,6,7,8,9,10]
    televote_potential_score: Literal[1,2,3,4,5,6,7,8,9,10]
    event: event.Event
    country: country.Country
    ceremonies: List[ceremony.Ceremony] = []
    votings: List[voting.Voting] = []


