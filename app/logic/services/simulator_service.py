
from app.logic.models import Participant, Song
from app.logic.services.base_service import BaseService
from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.logic.model_mappers import CeremonyModelMapper


class SimulatorService(BaseService):

    def get_simulation_participants_by_event_ceremony(self, event_id: int, ceremony_id: int)->list[Participant]:

        ceremony_entity = CeremonyRepository(self.session).get_event_ceremony(event_id=event_id, ceremony_id=ceremony_id)
        ceremony = CeremonyModelMapper().map_to_ceremony_model_without_event(ceremony_entity=ceremony_entity)
        
        return [self.build_participant_info(song) for song in ceremony.songs]


    def build_participant_info(self, song: Song)->Participant:

        participant_info = f"{song.country.name}. {song.artist} - {song.title}. Jury potential score: {song.jury_potential_score} | Televote potential score: {song.televote_potential_score}"
        return Participant(country_id=song.country.id, song_id=song.id, participant_info=participant_info)