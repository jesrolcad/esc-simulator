from sqlalchemy import insert
from app.persistence.entities import CeremonyEntity
from app.db.database import get_db

def create_ceremony(ceremony: CeremonyEntity)->int:
    with get_db() as db_session:
        insert_stmt = (insert(CeremonyEntity).values(ceremony_type_id=ceremony.ceremony_type_id,
                        event_id=ceremony.event_id, date=ceremony.date).returning(CeremonyEntity.id))
        
        result = db_session.execute(insert_stmt.returning(CeremonyEntity.id))
        ceremony_id = result.fetchone()[0]

        return ceremony_id

