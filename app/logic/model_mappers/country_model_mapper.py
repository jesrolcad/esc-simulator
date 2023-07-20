from app.logic.models import Country
from app.persistence.entities import CountryEntity
from app.logic.model_mappers.song_model_mapper import SongModelMapper


class CountryModelMapper:

    def map_to_country_entity(self, country: Country)->CountryEntity:
        return CountryEntity(id=country.id, name=country.name, code=country.code)


    def map_to_country_model(self, country_entity: CountryEntity)->Country:
        if country_entity is None:
            return None
        songs = [SongModelMapper().map_to_song_model(song) for song in country_entity.songs]

        return Country(id=country_entity.id, name=country_entity.name, code=country_entity.code, 
                    songs=songs)
