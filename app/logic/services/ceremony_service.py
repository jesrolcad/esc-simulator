from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.logic.model_mappers import ceremony_model_mapper
from app.logic.models import Ceremony
from app.logic.services.base_service import BaseService

class CeremonyService(BaseService):
    def create_ceremony(self, ceremony: Ceremony)->int:
        ceremony_entity = ceremony_model_mapper.map_to_ceremony_entity(ceremony)
        return CeremonyRepository(self.session).create_ceremony(ceremony_entity)