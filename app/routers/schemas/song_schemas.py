from typing import Literal, List
from pydantic.fields import Field
from pydantic import BaseModel
from app.routers.schemas.base_schemas import SchemaId
from app.routers.schemas.country_schemas import CountryWithoutSongsVotingsDataResponse
from app.routers.schemas.ceremony_schemas import CeremonyWithoutSongsVotingsDataResponse
from app.routers.schemas.voting_schemas import VotingWithoutCeremonySongCountryDataResponse

class BaseSong(BaseModel):
    title: str = Field(..., description="Song title", example="La, la, la")
    artist: str = Field(..., description="Artist name", example="Massiel")
    belongs_to_host_country: bool = Field(..., description="Whether the song belongs to the host country or not", example=False)
    jury_potential_score: Literal[1,2,3,4,5,6,7,8,9,10] = Field(..., description="Factor to calculate the jury score", example=10)
    televote_potential_score: Literal[1,2,3,4,5,6,7,8,9,10] =  Field(..., description="Factor to calculate the televote score", example=10)

class SongDataResponse(BaseSong, SchemaId):
    country: CountryWithoutSongsVotingsDataResponse
    ceremonies: List[CeremonyWithoutSongsVotingsDataResponse] = []
    votings: List[VotingWithoutCeremonySongCountryDataResponse] = [] 


class SongDataResponseList(BaseModel):
    songs: List[SongDataResponse]


class CreateSongRequest(BaseSong):
    country_id: int = Field(..., description="Country id", example=1)
    event_id: int = Field(..., description="Event id", example=1)