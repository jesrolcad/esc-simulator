from typing import Any
from sqlalchemy import Sequence, desc
from sqlalchemy.sql import func, case, select
from app.persistence.repositories.base_repository import BaseRepository
from app.persistence.entities import CeremonyTypeEntity, CountryEntity, SongEntity, VotingEntity, EventEntity, CeremonyEntity


class VotingRepository(BaseRepository):

# TODO: Rix query to access the attributes by label
    
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
    

    