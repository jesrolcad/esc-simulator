from fastapi import APIRouter, Depends
from app.db.database import get_db 
from app.logic.services.song_service import SongService
from app.routers.endpoints.definitions.song_definitions import get_song, get_songs
from app.routers.api_mappers import song_api_mapper

router = APIRouter(prefix="/songs", tags=["songs"])

@router.get(path="", summary=get_songs["summary"], description=get_songs["description"], responses=get_songs["responses"])
async def get_all_songs(db: get_db = Depends()):
    response = SongService(db).get_songs()
    return [song_api_mapper.map_to_song_data_response(song) for song in response]

@router.get(path="/{song_id}", summary=get_song["summary"], description=get_song["description"], responses=get_song["responses"])
async def get_song_by_id(song_id: int, db: get_db = Depends()):
    response = SongService(db).get_song(song_id)
    return song_api_mapper.map_to_song_data_response(response)
