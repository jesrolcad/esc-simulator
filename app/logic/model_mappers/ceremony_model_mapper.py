from app.logic.models.ceremony import Ceremony
from app.persistence.entities import CeremonyEntity

def map_to_ceremony_entity(ceremony: Ceremony)->CeremonyEntity:
    return CeremonyEntity(id=ceremony.id, ceremony_type_id=ceremony.ceremony_type.id, 
                        event_id=ceremony.event.id, date=ceremony.date)


def map_to_ceremony_model(ceremony_entity: CeremonyEntity)->Ceremony:
    return Ceremony(id=ceremony_entity.id, ceremony_type_id=ceremony_entity.ceremony_type_id, 
                    event_id=ceremony_entity.event_id, date=ceremony_entity.date)