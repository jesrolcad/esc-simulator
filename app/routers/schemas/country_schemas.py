from pydantic import BaseModel
from app.routers.schemas.base_schemas import SchemaId

class  BaseCountry(BaseModel):
    name: str
    code: str

class CountryWithoutSongsVotingsDataResponse(BaseCountry, SchemaId):
    pass

class CountryCreateRequest(BaseCountry):
    pass