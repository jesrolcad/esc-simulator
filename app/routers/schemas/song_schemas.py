from typing import Literal, List
from pydantic import BaseModel
from app.routers.schemas.base_schemas import SchemaId
from app.routers.schemas.country_schemas import CountryWithoutSongsVotingsDataResponse
from app.routers.schemas.ceremony_schemas import CeremonyWithoutSongsVotingsDataResponse
from app.routers.schemas.voting_schemas import VotingWithoutCeremonySongCountryDataResponse

class BaseSong(BaseModel):
    title: str
    artist: str
    belongs_to_host_country: bool
    jury_potential_score: Literal[1,2,3,4,5,6,7,8,9,10]
    televote_potential_score: Literal[1,2,3,4,5,6,7,8,9,10]

class SongDataResponse(BaseSong, SchemaId):
    country: CountryWithoutSongsVotingsDataResponse
    ceremonies: List[CeremonyWithoutSongsVotingsDataResponse] = []
    votings: List[VotingWithoutCeremonySongCountryDataResponse] = [] 
