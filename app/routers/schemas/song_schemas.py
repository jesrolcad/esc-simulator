from typing import List
from pydantic.fields import Field
from pydantic import BaseModel
from app.routers.schemas.base_schemas import BaseId, BaseSong
from app.routers.schemas.common_schemas import CountryWithoutSongsVotingsDataResponse, CeremonyWithoutSongsVotingsDataResponse, VotingWithoutCeremonySongCountryDataResponse

class SongDataResponse(BaseSong, BaseId):
    country: CountryWithoutSongsVotingsDataResponse
    ceremonies: List[CeremonyWithoutSongsVotingsDataResponse] = []
    votings: List[VotingWithoutCeremonySongCountryDataResponse] = [] 


class SongDataResponseList(BaseModel):
    songs: List[SongDataResponse]


class SongRequest(BaseSong):
    country_id: int = Field(..., json_schema_extra={"description": "Country id", "example": 1})
    event_id: int = Field(..., json_schema_extra={"description":"Event id", "example":1})
