from typing import List
from pydantic import Field
from app.routers.schemas.base_schemas import BaseCountry, BaseId
from app.routers.schemas.common_schemas import SongWithoutCountryCeremoniesVotings

class CountryRequest(BaseCountry):
    pass

class CountryDataResponse(BaseCountry, BaseId):
    songs: List[SongWithoutCountryCeremoniesVotings] = Field([], json_schema_extra={"description":"Country songs"})