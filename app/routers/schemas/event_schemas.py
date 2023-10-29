from typing import List
from datetime import date
from pydantic import Field
from pydantic import BaseModel
from app.routers.schemas.base_schemas import BaseId, BaseEvent
from app.routers.schemas.common_schemas import CeremonyWithoutEventDataResponse


class EventDataResponse(BaseEvent, BaseId): 
    ceremonies: List[CeremonyWithoutEventDataResponse] = []

class EventDataResponseList(BaseModel):
    events: List[EventDataResponse]

class EventRequest(BaseEvent):
    grand_final_date: date = Field(..., json_schema_extra={"description":"Grand Final ceremony date", "example":"2020-05-16"})