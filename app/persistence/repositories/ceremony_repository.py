from sqlalchemy import insert, select
from app.persistence.entities import CeremonyEntity, CeremonyTypeEntity
from app.persistence.repositories.base_repository import BaseRepository

class CeremonyRepository(BaseRepository):

    def create_ceremony(self, ceremony: CeremonyEntity)->int:
        insert_stmt = (insert(CeremonyEntity).values(ceremony_type_id=ceremony.ceremony_type_id,
                        event_id=ceremony.event_id, date=ceremony.date).returning(CeremonyEntity.id))
        
        result = self.session.execute(insert_stmt.returning(CeremonyEntity.id))
        ceremony_id = result.fetchone()[0]

        return ceremony_id

    def get_ceremony_type(self, code: str)->CeremonyTypeEntity:
        return self.session.scalars(select(CeremonyTypeEntity).where(CeremonyTypeEntity.code == code)).first()

