
from app.logic.models import Participant, SimulationCeremonyResult
from app.logic.services.base_service import BaseService
from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.persistence.repositories.voting_repository import VotingRepository
from app.logic.model_mappers import CeremonyModelMapper, SimulationModelMapper


class SimulatorService(BaseService):

    def get_simulation_participants_by_event_ceremony(self, event_id: int, ceremony_id: int)->list[Participant]:
        
        ceremony_entity = CeremonyRepository(self.session).get_event_ceremony(event_id=event_id, ceremony_id=ceremony_id)
        ceremony = CeremonyModelMapper().map_to_ceremony_model_without_event(ceremony_entity=ceremony_entity)

        if ceremony is None:
            return []
        
        return [SimulationModelMapper().build_participant_info(song) for song in ceremony.songs]
    
    def get_simulation_event_results(self, event_id: int)->SimulationCeremonyResult:

        #Repository retrieves a list of rows containing song_id, ceremony_id, jury_score, televote_score, total_score
        #Get song and ceremony information with those song_id and ceremony_id
        results = VotingRepository(self.session).get_scores_by_event_id(event_id=event_id)


        if results is None:
            return []

        return SimulationModelMapper().map_to_simulation_ceremony_result_model_list(results)



    