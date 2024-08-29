from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.logic.model_mappers import CeremonyModelMapper
from app.logic.models import Ceremony
from app.logic.services.base_service import BaseService
from app.utils.exceptions import NotFoundError

class CeremonyService(BaseService):

    def get_event_ceremony(self, ceremony_id: int, event_id: int)->Ceremony:
        ceremony_entity = CeremonyRepository(self.session).get_event_ceremony(ceremony_id=ceremony_id, event_id=event_id)

        if ceremony_entity is None:
            raise NotFoundError(field="event_id,ceremony_id",message=f"Ceremony with id {ceremony_id} associated to event with id {event_id} not found")

        return CeremonyModelMapper().map_to_ceremony_model_without_event(ceremony_entity=ceremony_entity)
    
    def get_event_ceremonies(self, event_id: int)->dict[int, int]:
        ceremony_entities = CeremonyRepository(self.session).get_ceremonies_by_event_id(event_id=event_id)
        return CeremonyModelMapper().map_to_ceremony_map(rows=ceremony_entities)


    def create_ceremony(self, ceremony: Ceremony)->int:
        ceremony_entity = CeremonyModelMapper.map_to_ceremony_entity(ceremony)
        return CeremonyRepository(self.session).create_ceremony(ceremony_entity)
    
    def add_songs_to_ceremony(self, ceremony_id: int, song_ids: list[int]):
        CeremonyRepository(self.session).add_songs_to_ceremony(ceremony_id=ceremony_id, song_ids=song_ids)
        