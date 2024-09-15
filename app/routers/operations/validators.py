from fastapi.exceptions import RequestValidationError
from app.routers.schemas.song_schemas import SongRequestQL
from app.utils.exceptions import ValidationError

def validate_song_request_ql(song: SongRequestQL):

    errors = ""

    if not song.title.strip() or len(song.title) >= 50:
        errors += "Title is required and should be less than 50 characters. "

    if not song.artist.strip() or len(song.artist) >= 50:
        errors += "Artist is required and should be less than 50 characters. "

    if len(errors) > 0:
        raise ValidationError(message=errors)


