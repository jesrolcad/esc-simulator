from typing import List
from pydantic import BaseModel
from app.routers.schemas.base_schemas import BaseId, BaseEvent
from app.routers.schemas.common_schemas import CeremonyWithoutEventDataResponse


class EventDataResponse(BaseEvent, BaseId): 
    ceremonies: List[CeremonyWithoutEventDataResponse] = []

class EventDataResponseList(BaseModel):
    events: List[EventDataResponse]


