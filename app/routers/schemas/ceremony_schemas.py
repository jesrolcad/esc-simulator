from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import Field
from app.routers.schemas.base_schemas import SchemaId
from app.routers.schemas.event_schemas import EventWithoutCeremoniesDataResponse

class BaseCeremonyType(BaseModel):
    name: str = Field(..., description="Ceremony type name", example="Semifinal 1")
    code: str = Field(..., description="Ceremony type code", example="SF1")

class CeremonyTypeDataResponse(BaseCeremonyType, SchemaId):
    pass

class BaseCeremony(BaseModel):
    date: datetime = Field(..., description="Ceremony date", example="2023-05-13")
    ceremony_type: CeremonyTypeDataResponse
    event: EventWithoutCeremoniesDataResponse


class CeremonyWithoutSongsVotingsDataResponse(BaseCeremony, SchemaId):
    pass


