from sqlalchemy import insert, select
from app.persistence.entities import CeremonyEntity, CeremonyTypeEntity
from app.db.database import get_db

def create_ceremony(ceremony: CeremonyEntity)->int:
    with get_db() as db_session:
        insert_stmt = (insert(CeremonyEntity).values(ceremony_type_id=ceremony.ceremony_type_id,
                        event_id=ceremony.event_id, date=ceremony.date).returning(CeremonyEntity.id))
        
        result = db_session.execute(insert_stmt.returning(CeremonyEntity.id))
        ceremony_id = result.fetchone()[0]

        return ceremony_id

def get_ceremony_type(code: str)->list[CeremonyTypeEntity]:
    with get_db() as db_session:
        return db_session.scalars(select(CeremonyTypeEntity).where(CeremonyTypeEntity.code == code)).first()

