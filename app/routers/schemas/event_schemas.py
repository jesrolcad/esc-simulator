from pydantic import BaseModel
from pydantic.fields import Field
from app.routers.schemas.base_schemas import SchemaId

class BaseEvent(BaseModel):
    year: int = Field(..., description="Event year", example=2018)
    slogan: str = Field(..., description="Event slogan", example="All Aboard!")
    host_city: str = Field(..., description="Event host city", example="Lisbon")
    arena: str = Field(..., description="Event arena", example="Altice Arena")

class EventWithoutCeremoniesDataResponse(BaseEvent, SchemaId):
    pass