import strawberry
from app.db.database import get_db, get_db_as_context_manager
from app.logic.services.song_service import SongService
from app.routers.api_mappers.song_api_mapper import SongApiMapper
from app.routers.schemas.song_schemas import SongDataResponseQL

@strawberry.type
class SongQuery:
    @strawberry.field
    def songs(self, info: strawberry.Info, title: str | None = None, country_code: str | None = None, event_year: int | None = None) -> list[SongDataResponseQL]:
        response = SongService(info.context.db).get_songs(title=title, country_code=country_code, event_year=event_year)
        return [SongApiMapper().map_to_song_data_response_ql(song) for song in response]