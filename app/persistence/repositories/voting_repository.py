from typing import Any
from sqlalchemy import Sequence, desc, and_
from sqlalchemy.sql import func, case, select
from app.persistence.repositories.base_repository import BaseRepository
from app.persistence.entities import CeremonyTypeEntity, CountryEntity, SongEntity, VotingEntity, EventEntity, CeremonyEntity


class VotingRepository(BaseRepository):
    
    def get_scores_by_event_id(self, event_id: int)->Sequence[Any]:
        return (self.session.execute(
            select(
                   SongEntity.id.label('song_id'), 
                   SongEntity.title.label('song_title'), 
                   SongEntity.artist.label('song_artist'),
                   SongEntity.jury_potential_score.label('jury_potential_score'),
                   SongEntity.televote_potential_score.label('televote_potential_score'),
                   CountryEntity.id.label('country_id'), 
                   CountryEntity.name.label('country_name'), 
                   VotingEntity.ceremony_id.label('ceremony_id'),
                   CeremonyTypeEntity.id.label('ceremony_type_id'),
                   CeremonyTypeEntity.name.label('ceremony_type_name'),
                func.sum(case((VotingEntity.voting_type_id == 1, VotingEntity.score), else_= 0)).label('jury_score'),
                func.sum(case((VotingEntity.voting_type_id == 2, VotingEntity.score), else_= 0)).label('televote_score'),
                func.sum(VotingEntity.score).label('total_score')
                )
            .join(SongEntity, VotingEntity.song_id == SongEntity.id)
            .join(CountryEntity, SongEntity.country_id == CountryEntity.id)
            .join(CeremonyEntity, VotingEntity.ceremony_id == CeremonyEntity.id)
            .join(CeremonyTypeEntity, CeremonyEntity.ceremony_type_id == CeremonyTypeEntity.id)
            .join(EventEntity, CeremonyEntity.event_id == EventEntity.id)
            .filter(EventEntity.id == event_id)
            .group_by(
                SongEntity.id,
                SongEntity.title,
                SongEntity.artist, 
                SongEntity.jury_potential_score,
                SongEntity.televote_potential_score,
                CountryEntity.id, 
                CountryEntity.name,  
                VotingEntity.ceremony_id,
                CeremonyTypeEntity.id,
                CeremonyTypeEntity.name)
            .order_by(desc('total_score')))
            .all())
    
    def get_scores_by_event_id_and_ceremony_type_id(self, event_id: int, ceremony_type_id: int)->Sequence[Any]:
        return (self.session.execute(
            select(
                   SongEntity.id.label('song_id'), 
                   SongEntity.title.label('song_title'), 
                   SongEntity.artist.label('song_artist'),
                   SongEntity.jury_potential_score.label('jury_potential_score'),
                   SongEntity.televote_potential_score.label('televote_potential_score'),
                   CountryEntity.id.label('country_id'), 
                   CountryEntity.name.label('country_name'), 
                   VotingEntity.ceremony_id.label('ceremony_id'),
                   CeremonyTypeEntity.id.label('ceremony_type_id'),
                   CeremonyTypeEntity.name.label('ceremony_type_name'),
                func.sum(case((VotingEntity.voting_type_id == 1, VotingEntity.score), else_= 0)).label('jury_score'),
                func.sum(case((VotingEntity.voting_type_id == 2, VotingEntity.score), else_= 0)).label('televote_score'),
                func.sum(VotingEntity.score).label('total_score')
                )
            .join(SongEntity, VotingEntity.song_id == SongEntity.id)
            .join(CountryEntity, SongEntity.country_id == CountryEntity.id)
            .join(CeremonyEntity, VotingEntity.ceremony_id == CeremonyEntity.id)
            .join(CeremonyTypeEntity, CeremonyEntity.ceremony_type_id == CeremonyTypeEntity.id)
            .join(EventEntity, CeremonyEntity.event_id == EventEntity.id)
            .where(and_(EventEntity.id == event_id, CeremonyTypeEntity.id == ceremony_type_id))
            .group_by(
                SongEntity.id,
                SongEntity.title,
                SongEntity.artist, 
                SongEntity.jury_potential_score,
                SongEntity.televote_potential_score,
                CountryEntity.id, 
                CountryEntity.name,  
                VotingEntity.ceremony_id,
                CeremonyTypeEntity.id,
                CeremonyTypeEntity.name)
            .order_by(desc('total_score')))
            .all())

    def get_qualified_song_ids_for_grand_final(self, semifinal_one_ceremony_id: int, semifinal_two_ceremony_id: int)->list[int]:
        semifinal_one_subquery = (
            select(
            VotingEntity.song_id, VotingEntity.ceremony_id, 
            func.sum(case((VotingEntity.voting_type_id == 1, VotingEntity.score), else_= 0)).label('jury_score'),
            func.sum(case((VotingEntity.voting_type_id == 2, VotingEntity.score), else_= 0)).label('televote_score'),
            func.sum(VotingEntity.score).label('total_score')
            )
            .where(VotingEntity.ceremony_id == semifinal_one_ceremony_id)
            .group_by(VotingEntity.song_id, VotingEntity.ceremony_id)
            .order_by(desc("total_score"))
            .limit(10)
            .subquery()
            )

        semifinal_two_subquery = (select(
            VotingEntity.song_id, VotingEntity.ceremony_id, 
            func.sum(case((VotingEntity.voting_type_id == 1, VotingEntity.score), else_= 0)).label('jury_score'),
            func.sum(case((VotingEntity.voting_type_id == 2, VotingEntity.score), else_= 0)).label('televote_score'),
            func.sum(VotingEntity.score).label('total_score')
            )
            .where(VotingEntity.ceremony_id == semifinal_two_ceremony_id)
            .group_by(VotingEntity.song_id, VotingEntity.ceremony_id)
            .order_by(desc("total_score"))
            .limit(10)
            .subquery()
            )
        
        final_query = select(semifinal_one_subquery.c.song_id).union_all(
            select(semifinal_two_subquery.c.song_id))
        
        return self.session.execute(final_query).scalars().all()


    

    