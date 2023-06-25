from app.persistence.repositories import ceremony_repository
from app.logic.model_mappers import ceremony_model_mapper
from app.logic.models.ceremony import Ceremony

def create_ceremony(ceremony: Ceremony)->int:
    ceremony_entity = ceremony_model_mapper.map_to_ceremony_entity(ceremony)
    return ceremony_repository.create_ceremony(ceremony_entity)