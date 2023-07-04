from pydantic import BaseModel
from app.routers.schemas.base_schemas import SchemaId

class BaseEvent(BaseModel):
    year: int
    slogan: str
    host_city: str
    arena: str

class EventWithoutCeremoniesDataResponse(BaseEvent, SchemaId):
    pass