from fastapi import APIRouter, Depends, Response, status
from app.db.database import get_db 
from app.logic.services.song_service import SongService
from app.routers.endpoints.definitions.song_definitions import get_song_endpoint, get_songs_endpoint, create_song_endpoint
from app.routers.api_mappers.song_api_mapper import SongApiMapper
from app.routers.schemas.song_schemas import CreateSongRequest
from app.routers.schemas.base_schemas import ResultResponse, SchemaId

router = APIRouter(prefix="/songs", tags=["songs"])

@router.get(path="", summary=get_songs_endpoint["summary"], description=get_songs_endpoint["description"], responses=get_songs_endpoint["responses"])
async def get_songs(title: str | None = None, country_code: str | None = None, event_year: int | None = None,db: get_db = Depends()):
    response = SongService(db).get_songs(title=title, country_code=country_code, event_year=event_year)
    return [SongApiMapper().map_to_song_data_response(song) for song in response]

@router.get(path="/{song_id}", summary=get_song_endpoint["summary"], description=get_song_endpoint["description"], responses=get_song_endpoint["responses"])
async def get_song(song_id: int, db: get_db = Depends()):
    response = SongService(db).get_song(song_id)
    return SongApiMapper().map_to_song_data_response(response)


@router.post(path="", summary=create_song_endpoint["summary"], description=create_song_endpoint["description"], 
            responses=create_song_endpoint["responses"], status_code=status.HTTP_201_CREATED)
async def create_song(song: CreateSongRequest, db: get_db = Depends()):
    song_model = SongApiMapper().map_to_song_model(song_schema=song)
    song_response = SongService(db).create_song(song_model)
    return ResultResponse(message="Song created successfully", data=SchemaId(id=song_response.id))
