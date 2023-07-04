from fastapi import status
from app.routers.schemas.base_schemas import ErrorResponse
from app.routers.schemas.song_schemas import SongDataResponse

get_song = {
    "summary": "Get song by id",
    "description": """Get song details by id. If the song is not found, a 404 error will be returned.""",
    "responses": {
        status.HTTP_200_OK: {
            "model": SongDataResponse, 
            "description": "Song details retrieved successfully"},

        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse, 
            "description": "Song not found"}}
}