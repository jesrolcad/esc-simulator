from fastapi import status
from app.routers.schemas.base_schemas import ErrorResponse, ResultResponse
from app.routers.schemas.song_schemas import SongDataResponse, SongDataResponseList

get_song_endpoint = {
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

get_songs_endpoint = {
    "summary": "Get all songs",
    "description": """Get all songs. You can filter the results by song name, country or event. If no songs are found, an empty list will be returned.""",
    "responses": {
        status.HTTP_200_OK: {
            "model": SongDataResponseList,
            "description": "Songs retrieved successfully"}}
}

create_song_endpoint = {
    "summary": "Create song",
    "description": """Create a new song. If the song is created successfully, the song details will be returned.""",
    "responses": {
        status.HTTP_201_CREATED: {
            "model": ResultResponse,
            "description": "Song created successfully"},

        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid request body"},
    }
}

update_song_endpoint = {
    "summary": "Update song",
    "description": """Update an existing song. No content will be returned when the song is updated successfully.""",
    "responses": {
        status.HTTP_204_NO_CONTENT: {
            "description": "Song updated successfully"},

        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Song not found"},
    }
}
