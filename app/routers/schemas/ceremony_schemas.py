from datetime import datetime
from pydantic import BaseModel
from app.routers.schemas.base_schemas import SchemaId
from app.routers.schemas.event_schemas import EventWithoutCeremoniesDataResponse

class BaseCeremonyType(BaseModel):
    name: str
    code: str

class CeremonyTypeDataResponse(BaseCeremonyType, SchemaId):
    pass

class BaseCeremony(BaseModel):
    date: datetime
    ceremony_type: CeremonyTypeDataResponse
    event: EventWithoutCeremoniesDataResponse


class CeremonyWithoutSongsVotingsDataResponse(BaseCeremony, SchemaId):
    pass


