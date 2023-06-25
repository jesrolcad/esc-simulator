from typing import List
from pydantic import BaseModel
from app.logic.models import ceremony

class Event(BaseModel):
    id: int
    year: int
    slogan: str
    host_city: str
    arena: str
    ceremonies: List[ceremony.Ceremony]