from datetime import datetime, timedelta
from app.logic.services.base_service import BaseService
from app.persistence.repositories.event_repository import EventRepository
from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.logic.model_mappers import EventModelMapper, CeremonyModelMapper
from app.logic.models import Event, Ceremony
from app.persistence.repositories.song_repository import SongRepository
from app.persistence.repositories.voting_repository import VotingRepository
from app.utils.exceptions import BusinessLogicValidationError, NotFoundError

class EventService(BaseService):

    def get_events(self, submodels: bool = True)->list[Event]:
        event_entities = EventRepository(self.session).get_events()

        if not submodels:
            return [EventModelMapper().map_to_event_model_without_submodels(event_entity=event_entity) for event_entity in event_entities]

        return [EventModelMapper().map_to_event_model(event_entity) for event_entity in event_entities]

    def get_event(self, id: int = None, year: int = None, submodels: bool = True)->Event:
        event_entity = EventRepository(self.session).get_event(id, year)

        if event_entity is None:
            raise NotFoundError(field="event_id",message=f"Event with id {id} not found")
        
        if not submodels:
            return EventModelMapper().map_to_event_model_without_submodels(event_entity=event_entity)

        return EventModelMapper().map_to_event_model(event_entity)

    def create_event_and_associated_ceremonies(self, event: Event, grand_final_date: datetime)->Event:
        event_entity = EventModelMapper().map_to_event_entity(event)
        created_event_entity = EventRepository(self.session).create_event(event_entity)
        created_event_model = EventModelMapper().map_to_event_model_without_submodels(created_event_entity)
        self.associate_ceremonies_to_event(created_event_model, grand_final_date)

        return created_event_model


    def associate_ceremonies_to_event(self, event: Event, grand_final_date: datetime):
        semifinal1_date = grand_final_date - timedelta(days=4)
        semifinal2_date = grand_final_date - timedelta(days=2)

        first_semifinal_ceremony_type = (CeremonyModelMapper()
                                        .map_to_ceremony_type_model(CeremonyRepository(self.session).get_ceremony_type(code='SF1')))
        
        second_semifinal_ceremony_type = (CeremonyModelMapper()
                                        .map_to_ceremony_type_model(CeremonyRepository(self.session).get_ceremony_type(code='SF2')))

        grand_final_ceremony_type = (CeremonyModelMapper()
                                        .map_to_ceremony_type_model(CeremonyRepository(self.session).get_ceremony_type(code='GF')))

        first_semifinal_ceremony = Ceremony(date=semifinal1_date, ceremony_type=first_semifinal_ceremony_type, event=event)
        second_semifinal_ceremony = Ceremony(date=semifinal2_date, ceremony_type=second_semifinal_ceremony_type, event=event)
        grand_final_ceremmony = Ceremony(date=grand_final_date, ceremony_type=grand_final_ceremony_type, event=event)

        CeremonyRepository(self.session).create_ceremony(CeremonyModelMapper().map_to_ceremony_entity(first_semifinal_ceremony))
        CeremonyRepository(self.session).create_ceremony(CeremonyModelMapper().map_to_ceremony_entity(second_semifinal_ceremony))
        CeremonyRepository(self.session).create_ceremony(CeremonyModelMapper().map_to_ceremony_entity(grand_final_ceremmony))


    def update_event(self, event_id: int, event: Event):
        self.get_event(id=event_id)
        exists_event_simulation = VotingRepository(self.session).check_exists_votings_by_event_id(event_id=event_id)

        if exists_event_simulation:
            raise NotFoundError(field="event_id", message=f"Event with id {event_id} cannot be updated because it has already been simulated")
        
        updated_event_entity = EventModelMapper().map_to_event_entity(event=event)
        updated_event_entity.id = event_id
        EventRepository(self.session).update_event(event=updated_event_entity)


    def delete_event(self, event_id: int):
        self.get_event(id=event_id)

        exists_event_simulation = VotingRepository(self.session).check_exists_votings_by_event_id(event_id=event_id)

        if exists_event_simulation:
            raise BusinessLogicValidationError(field="event_id", message=f"Event with id {event_id} cannot be deleted because it has already been simulated")
        
        SongRepository(self.session).delete_songs_by_event_id(event_id=event_id)
        CeremonyRepository(self.session).delete_ceremonies_by_event_id(event_id=event_id)
        EventRepository(self.session).delete_event(event_id=event_id)
