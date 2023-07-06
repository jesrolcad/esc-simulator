from fastapi import APIRouter, Depends
from app.db.database import get_db 
from app.logic.services.song_service import SongService
from app.routers.endpoints.definitions.song_definitions import get_song_by_id, get_song_list
from app.routers.api_mappers import song_api_mapper

router = APIRouter(prefix="/songs", tags=["songs"])

@router.get(path="", summary=get_song_list["summary"], description=get_song_list["description"], responses=get_song_list["responses"])
async def get_songs(title: str | None = None, country_code: str | None = None, event_year: int | None = None,db: get_db = Depends()):
    response = SongService(db).get_songs(title=title, country_code=country_code, event_year=event_year)
    return [song_api_mapper.map_to_song_data_response(song) for song in response]

@router.get(path="/{song_id}", summary=get_song_by_id["summary"], description=get_song_by_id["description"], responses=get_song_by_id["responses"])
async def get_song(song_id: int, db: get_db = Depends()):
    response = SongService(db).get_song(song_id)
    return song_api_mapper.map_to_song_data_response(response)
