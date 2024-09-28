from fastapi.exceptions import RequestValidationError
from app.routers.schemas.base_schemas import BaseEventQL
from app.routers.schemas.country_schemas import CountryRequestQL
from app.routers.schemas.event_schemas import CreateEventRequestQL
from app.routers.schemas.song_schemas import SongRequestQL
from app.utils.exceptions import ValidationError
import datetime

def validate_song_request_ql(song: SongRequestQL):

    errors = ""

    if not song.title.strip() or len(song.title) >= 50:
        errors += "Title is required and should be less than 50 characters. "

    if not song.artist.strip() or len(song.artist) >= 50:
        errors += "Artist is required and should be less than 50 characters. "

    if len(errors) > 0:
        raise ValidationError(message=errors)
    

def validate_country_request_ql(country: CountryRequestQL):

    errors = ""

    if not country.name.strip() or len(country.name) >= 50:
        errors += "Name is required and should be less than 50 characters. "

    if not country.code.strip() or len(country.code) >= 5:
        errors += "Code is required and should be less than 5 characters. "

    if len(errors) > 0:
        raise ValidationError(message=errors)
    
def validate_event_request_ql(event: BaseEventQL):

    errors = ""

    if not event.slogan.strip() or len(event.slogan) >= 50:
        errors += "Slogan is required and should be less than 50 characters. "

    if not event.host_city.strip() or len(event.host_city) >= 50:
        errors += "Host city is required and should be less than 50 characters. "

    if not event.arena.strip() or len(event.arena) >= 50:
        errors += "Arena is required and should be less than 50 characters. "
    

    if len(errors) > 0:
        raise ValidationError(message=errors)

    
def validate_create_event_request_ql(event: CreateEventRequestQL):

    errors = ""

    try:
        validate_event_request_ql(event)
    except ValidationError as e:
        errors += e.message

    # event year cannot be less than current year
    if event.year < datetime.datetime.now().year:
        errors += "Year cannot be less than current year. "

    if event.year != event.grand_final_date.year:
        errors += "Year should be the same as grand final date year. "

    if event.grand_final_date < datetime.datetime.now().date():
        errors += "Grand final date cannot be less than current date. "

    if len(errors) > 0:
        raise ValidationError(message=errors)

    
    


