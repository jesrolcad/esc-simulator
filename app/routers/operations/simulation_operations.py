import strawberry

from app.logic.models import Participant, ParticipantResult, SimulationCeremonyResult
from app.logic.services.simulator_service import SimulatorService
from app.routers.schemas.api_schemas import ResultResponseQL
from app.routers.schemas.base_schemas import BaseParticipantQL, BaseSimulationResultQL

# TODO: Decide whether participant_info should have a resolver or not
class ParticipantDataResponseQL(BaseParticipantQL):

    @staticmethod
    def map_to_participant_data_response_ql(participant_model: Participant)->'ParticipantDataResponseQL':
        return ParticipantDataResponseQL(country_id=participant_model.country_id, song_id=participant_model.song_id, 
                                        participant_info=participant_model.participant_info)
                                        
@strawberry.type
class ParticipantResultDataResponseQL(BaseParticipantQL):
    position: int
    total_score: int
    jury_score: int
    televote_score: int
    
    @staticmethod
    def map_to_participant_result_data_response_ql(participant_model: ParticipantResult, position: int)->'ParticipantResultDataResponseQL':
        return ParticipantResultDataResponseQL(country_id=participant_model.country_id, song_id=participant_model.song_id, 
                                        participant_info=participant_model.participant_info, position=position, total_score=participant_model.total_score,
                                        jury_score=participant_model.jury_score, televote_score=participant_model.televote_score)

@strawberry.type
class SimulationCeremonyResultResponseQL(BaseSimulationResultQL):
    ceremony_type_id: int
    ceremony_type_name: str
    results: list[ParticipantResultDataResponseQL]
    
    @staticmethod
    def map_to_simulation_ceremony_result_data_response_ql(simulation_result_model: SimulationCeremonyResult)->'SimulationCeremonyResultResponseQL':
        return SimulationCeremonyResultResponseQL(ceremony_id=simulation_result_model.ceremony_id, 
                                                  ceremony_type_id=simulation_result_model.ceremony_type.id, 
                                                  ceremony_type_name=simulation_result_model.ceremony_type.name, 
                                                  results=[ParticipantResultDataResponseQL.map_to_participant_result_data_response_ql(participant_model=result, position=position) 
                                                           for position, result in enumerate(simulation_result_model.results, start=1)])


@strawberry.type
class SimulatorQuery:
    @strawberry.field
    def event_ceremony_participants(self, info: strawberry.Info, event_id: int, ceremony_id: int)-> list[ParticipantDataResponseQL]:
        participants = SimulatorService(info.context.db).get_simulation_participants_by_event_ceremony(event_id=event_id, 
                                                                                                       ceremony_id=ceremony_id)

        return [ParticipantDataResponseQL.map_to_participant_data_response_ql(participant_model=participant) 
                for participant in participants]
    
    @strawberry.field
    def event_results(self, info: strawberry.Info, event_id: int)-> list[SimulationCeremonyResultResponseQL]:
        simulation_results = SimulatorService(info.context.db).get_simulation_event_results(event_id=event_id)

        return [SimulationCeremonyResultResponseQL.map_to_simulation_ceremony_result_data_response_ql(simulation_result_model=simulation) for simulation in simulation_results]
    
    @strawberry.field
    def event_ceremony_type_results(self, info: strawberry.Info, event_id: int, ceremony_type_id: int)-> SimulationCeremonyResultResponseQL:
        simulation = SimulatorService(info.context.db).get_simulation_event_results_by_ceremony_type(event_id=event_id, 
                                                                                                     ceremony_type_id=ceremony_type_id)

        return SimulationCeremonyResultResponseQL.map_to_simulation_ceremony_result_data_response_ql(simulation_result_model=simulation)

@strawberry.type
class SimulatorMutation:
    @strawberry.mutation
    def create_event_simulation(self, info: strawberry.Info, event_id: int)-> ResultResponseQL:
        SimulatorService(info.context.db).create_simulation(event_id=event_id)

        return ResultResponseQL(success=True,message="Event simulated successfully")

    @strawberry.mutation
    def delete_event_simulation(self, info: strawberry.Info, event_id: int)-> ResultResponseQL:
        SimulatorService(info.context.db).delete_simulation_by_event_id(event_id=event_id)

        return ResultResponseQL(success=True,message="Event simulation deleted successfully")