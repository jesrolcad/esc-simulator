from typing import List
from pydantic import BaseModel
import strawberry
from .base_schemas import BaseParticipant, BaseSimulationResult

class ParticipantDataResponse(BaseParticipant):
    pass

class ParticipantDataResponseList(BaseModel):
    participants: List[ParticipantDataResponse]

class ParticipantResultDataResponse(BaseParticipant):
    position: int
    total_score: int
    jury_score: int
    televote_score: int

class ParticipantResultDataResponseList(BaseModel):
    participants: List[ParticipantResultDataResponse]

class SimulationCeremonyResultDataResponse(BaseSimulationResult):
    ceremony_type_id: int
    ceremony_type_name: str
    results: ParticipantResultDataResponseList

class SimulationResultDataResponse(BaseModel):
    simulation_ceremonies_result: List[SimulationCeremonyResultDataResponse]