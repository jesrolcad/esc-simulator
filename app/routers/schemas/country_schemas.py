from typing import List
from pydantic import BaseModel
from pydantic.fields import Field
from app.routers.schemas.api_schemas import SchemaId
from app.routers.schemas.song_schemas import SongWithoutCountryCeremoniesVotings


class  BaseCountry(BaseModel):
    name: str = Field(..., description="Country name", example="Spain")
    code: str = Field(..., description="Country code", example="ESP")

class CountryDataResponse(BaseCountry, SchemaId):
    songs: List[SongWithoutCountryCeremoniesVotings] = []

class CountryWithoutSongsVotingsDataResponse(BaseCountry, SchemaId):
    pass

class CountryCreateRequest(BaseCountry):
    pass