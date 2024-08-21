
from app.logic.models import Participant, SimulationCeremonyResult
from app.logic.services.base_service import BaseService
from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.persistence.repositories.voting_repository import VotingRepository
from app.logic.model_mappers import CeremonyModelMapper, SimulationModelMapper
from app.utils.exceptions import NotFoundError


class SimulatorService(BaseService):

    def get_simulation_participants_by_event_ceremony(self, event_id: int, ceremony_id: int)->list[Participant]:
        
        ceremony_entity = CeremonyRepository(self.session).get_event_ceremony(event_id=event_id, ceremony_id=ceremony_id)
        ceremony = CeremonyModelMapper().map_to_ceremony_model_without_event(ceremony_entity=ceremony_entity)

        if ceremony is None:
            return []
        
        return [SimulationModelMapper().build_participant_info(song) for song in ceremony.songs]
    
    def get_simulation_event_results(self, event_id: int)->list[SimulationCeremonyResult]:
        results = VotingRepository(self.session).get_scores_by_event_id(event_id=event_id)


        if results is None:
            return []

        return SimulationModelMapper().map_to_simulation_ceremony_result_model_list(results)
    
    def get_simulation_event_results_by_ceremony_type(self, event_id: int, ceremony_type_id: int)->SimulationCeremonyResult:

        result = VotingRepository(self.session).get_scores_by_event_id_and_ceremony_type_id(event_id=event_id, ceremony_type_id=ceremony_type_id)

        print("Result", result)

        if result is None or len(result) == 0:
            raise NotFoundError(field="event_id, ceremony_type_id", message=f"No results found for event_id {event_id} and ceremony_type_id {ceremony_type_id}")


        return SimulationModelMapper().map_to_simulation_ceremony_result_model(result) if result else None




    