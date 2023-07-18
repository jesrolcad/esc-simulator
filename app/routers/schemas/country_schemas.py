from pydantic import BaseModel
from pydantic.fields import Field
from app.routers.schemas.base_schemas import SchemaId

class  BaseCountry(BaseModel):
    name: str = Field(..., description="Country name", example="Spain")
    code: str = Field(..., description="Country code", example="ESP")

class CountryWithoutSongsVotingsDataResponse(BaseCountry, SchemaId):
    pass

class CountryCreateRequest(BaseCountry):
    pass