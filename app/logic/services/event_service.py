from datetime import datetime, timedelta
from app.logic.services.base_service import BaseService
from app.persistence.repositories.event_repository import EventRepository
from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.logic.model_mappers.event_model_mapper import EventModelMapper
from app.logic.model_mappers.ceremony_model_mapper import CeremonyModelMapper
from app.logic.models import Event
from app.logic.models import Ceremony

class EventService(BaseService):

    def get_event(self, id: int = None, year: int = None)->Event:
        event_entity = EventRepository(self.session).get_event(id, year)
        return EventModelMapper.map_to_event_model(event_entity)


    def create_event_and_associated_ceremonies(self, event: Event, grand_final_date: datetime)->Event:
        event_entity = EventModelMapper.map_to_event_entity(event)
        with self.session as session:
            created_event_entity = EventRepository(self.session).create_event(event_entity)
            created_event_model = EventModelMapper.map_to_event_model(created_event_entity)
            self.associate_ceremonies_to_event(created_event_model, grand_final_date)

            return created_event_model


    def associate_ceremonies_to_event(self, event: Event, grand_final_date: datetime):
        semifinal1_date = grand_final_date - timedelta(days=4)
        semifinal2_date = grand_final_date - timedelta(days=2)

        first_semifinal_ceremony_type = (CeremonyModelMapper
                                        .map_to_ceremony_type_model(CeremonyRepository(self.session).get_ceremony_type(code='SF1')))
        
        second_semifinal_ceremony_type = (CeremonyModelMapper
                                        .map_to_ceremony_type_model(CeremonyRepository(self.session).get_ceremony_type(code='SF2')))

        grand_final_ceremony_type = (CeremonyModelMapper
                                        .map_to_ceremony_type_model(CeremonyRepository(self.session).get_ceremony_type(code='GF')))

        first_semifinal_ceremony = Ceremony(date=semifinal1_date, ceremony_type=first_semifinal_ceremony_type, event=event)
        second_semifinal_ceremony = Ceremony(date=semifinal2_date, ceremony_type=second_semifinal_ceremony_type, event=event)
        grand_final_ceremmony = Ceremony(date=grand_final_date, ceremony_type=grand_final_ceremony_type, event=event)

        CeremonyRepository(self.session).create_ceremony(CeremonyModelMapper.map_to_ceremony_entity(first_semifinal_ceremony))
        CeremonyRepository(self.session).create_ceremony(CeremonyModelMapper.map_to_ceremony_entity(second_semifinal_ceremony))
        CeremonyRepository(self.session).create_ceremony(CeremonyModelMapper.map_to_ceremony_entity(grand_final_ceremmony))

