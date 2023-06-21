from app.schemas.country import CountryCreate
from app.db.models import Country

def map_to_country(country: CountryCreate)->Country:
    return Country(name=country.name, code=country.code)

