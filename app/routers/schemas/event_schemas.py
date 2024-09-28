from typing import List
from datetime import date
from pydantic import Field
from pydantic import BaseModel
import strawberry
from app.routers.schemas.base_schemas import BaseEventQL, BaseId, BaseEvent
from app.routers.schemas.common_schemas import CeremonyWithoutEventDataResponse


class EventDataResponse(BaseEvent, BaseId): 
    ceremonies: List[CeremonyWithoutEventDataResponse] = []

class EventDataResponseList(BaseModel):
    events: List[EventDataResponse]

class CreateEventRequest(BaseEvent):
    grand_final_date: date = Field(..., json_schema_extra={"description":"Grand Final ceremony date", "example":"2020-05-16"})

class UpdateEventRequest(BaseModel):
    slogan: str = Field(None, json_schema_extra={"description":"Event slogan", "example":"All Aboard!"}, min_length=1, max_length=50)
    host_city: str = Field(None, json_schema_extra={"description":"Event host city", "example":"Lisbon"}, min_length=1, max_length=50)
    arena: str = Field(None, json_schema_extra={"description":"Event arena", "example":"Altice Arena"}, min_length=1, max_length=50)

@strawberry.input
class CreateEventRequestQL(BaseEventQL):
    grand_final_date: date

@strawberry.input
class UpdateEventRequestQL(BaseEventQL):
    pass