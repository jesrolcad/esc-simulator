from app.logic.models import Ceremony, CeremonyType
from app.persistence.entities import CeremonyEntity, CeremonyTypeEntity

def map_to_ceremony_entity(ceremony: Ceremony)->CeremonyEntity:
    return CeremonyEntity(id=ceremony.id, ceremony_type_id=ceremony.ceremony_type.id, 
                        event_id=ceremony.event.id, date=ceremony.date)


def map_to_ceremony_model(ceremony_entity: CeremonyEntity)->Ceremony:
    return Ceremony(id=ceremony_entity.id, ceremony_type_id=ceremony_entity.ceremony_type_id, 
                    event_id=ceremony_entity.event_id, date=ceremony_entity.date)

def map_to_ceremony_type_model(ceremony_type_entity: CeremonyTypeEntity)->CeremonyType:
    return CeremonyType(id=ceremony_type_entity.id, name=ceremony_type_entity.name, code=ceremony_type_entity.code)