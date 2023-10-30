from typing import List
from pydantic import BaseModel
from .base_schemas import BaseParticipant

class ParticipantDataResponse(BaseParticipant):
    pass

class ParticipantDataResponseList(BaseModel):
    participants: List[ParticipantDataResponse]