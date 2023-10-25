from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.logic.model_mappers import CeremonyModelMapper
from app.logic.models import Ceremony
from app.logic.services.base_service import BaseService

class CeremonyService(BaseService):

    def get_event_ceremonies(self, ceremony_id: int, event_id: int)->list[Ceremony]:
        ceremony_entities = CeremonyRepository(self.session).get_event_ceremony(ceremony_id=ceremony_id, event_id=event_id)

        return [CeremonyModelMapper.map_to_ceremony_model_without_event(ceremony_entity=ceremony_entity) 
                for ceremony_entity in ceremony_entities]


    def create_ceremony(self, ceremony: Ceremony)->int:
        ceremony_entity = CeremonyModelMapper.map_to_ceremony_entity(ceremony)
        return CeremonyRepository(self.session).create_ceremony(ceremony_entity)