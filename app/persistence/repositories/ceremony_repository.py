from typing import Any
from sqlalchemy import insert, select, delete, and_, Sequence
from sqlalchemy.orm import joinedload
from app.persistence.entities import CeremonyEntity, CeremonyTypeEntity, SongCeremony
from app.persistence.repositories.base_repository import BaseRepository

class CeremonyRepository(BaseRepository):

    def get_event_ceremony(self, ceremony_id: int, event_id: int)->list[CeremonyEntity]:
        return self.session.scalars(select(CeremonyEntity).where(and_(CeremonyEntity.id == ceremony_id, CeremonyEntity.event_id == event_id))).first()

    def get_ceremony_type(self, code: str)->CeremonyTypeEntity:
        return self.session.scalars(select(CeremonyTypeEntity).where(CeremonyTypeEntity.code == code)).first()

    def get_ceremonies_by_event_id(self, event_id: int)->Sequence[Any]:
        return self.session.execute(select(CeremonyEntity.ceremony_type_id, CeremonyEntity.id).where(CeremonyEntity.event_id == event_id)).all()

    def get_ceremonies_with_ceremony_types_by_event_id(self, event_id: int)->Sequence[Any]:
        return self.session.scalars(select(CeremonyEntity)
                                    .options(joinedload(CeremonyEntity.ceremony_type))
                            .where(CeremonyEntity.event_id == event_id)).all()
    
    
    def create_ceremony(self, ceremony: CeremonyEntity)->int:
        insert_stmt = (insert(CeremonyEntity).values(ceremony_type_id=ceremony.ceremony_type_id,
                        event_id=ceremony.event_id, date=ceremony.date).returning(CeremonyEntity.id))
        
        result = self.session.execute(insert_stmt.returning(CeremonyEntity.id))
        ceremony_id = result.fetchone()[0]

        return ceremony_id

    def add_songs_to_ceremony(self, ceremony_id: int, song_ids: list[int]):
        song_ceremony_dicts = [{"ceremony_id": ceremony_id, "song_id": song_id} for song_id in song_ids]
        self.session.execute(insert(SongCeremony), song_ceremony_dicts)


    def delete_ceremonies_by_event_id(self, event_id: int):
        delete_stmt = (delete(CeremonyEntity).where(CeremonyEntity.event_id == event_id))
        self.session.execute(delete_stmt)








