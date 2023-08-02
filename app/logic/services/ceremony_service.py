from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.logic.model_mappers import CeremonyModelMapper
from app.logic.models import Ceremony
from app.logic.services.base_service import BaseService

class CeremonyService(BaseService):
    def create_ceremony(self, ceremony: Ceremony)->int:
        ceremony_entity = CeremonyModelMapper.map_to_ceremony_entity(ceremony)
        return CeremonyRepository(self.session).create_ceremony(ceremony_entity)