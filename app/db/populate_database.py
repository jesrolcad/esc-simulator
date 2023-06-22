from database import get_db
from app.persistence.entities import EventEntity, CountryEntity, SongEntity, CeremonyEntity, CeremonyEntity, ScoreTypeEntity
import pandas as pd
from utils.constants import COUNTRY_NAME_TO_CODE
from app.utils.song_functions import calculate_potential_scores

#CeremonyEntity dates must be populated manually in the database

def populate_events_with_ceremonies(path: str):
    dataframe = pd.read_csv(path)
    check_dataframe_has_columns(dataframe, ['year', 'slogan', 'host_city', 'arena'])
    
    with get_db() as db:
        db.query(EventEntity).delete()
        db.query(CeremonyEntity).delete()
        for row in dataframe.itertuples(index=False):
            event = EventEntity(year=row.year, slogan=row.slogan, 
                    host_city=row.host_city, arena=row.arena)
            db.add(event)
            for ceremony_type_id in range(1,4):
                ceremony = CeremonyEntity(ceremony_type_id=ceremony_type_id, event_id=row.id)
                db.add(ceremony)


def populate_countries(path: str):
    dataframe = pd.read_csv(path)
    check_dataframe_has_columns(dataframe, ['name'])

    with get_db() as db:
        db.query(CountryEntity).delete()
        for row in dataframe.itertuples(index=False):
            country = CountryEntity(name=row.name, code=COUNTRY_NAME_TO_CODE[row.name])
            db.add(country)


def populate_songs(path: str):
    dataframe = pd.read_csv(path)
    check_dataframe_has_columns(dataframe, ['title', 'artist', 'country_id', 'event_id', 'belongs_to_host_country'])

    with get_db() as db:
        db.query(SongEntity).delete()
        data = [{'title': row.title, 'artist': row.artist, 'country_id': row.country_id, 'event_id': row.event_id,
        'jury_potential_score': calculate_potential_scores(row.position)[0],
        'televote_potential_score': calculate_potential_scores(row.position)[1],
        'belongs_to_host_country': row.belongs_to_host_country} for row in dataframe.itertuples(index=False)]

        db.bulk_insert_mappings(SongEntity, data)


def populate_ceremony_types():
    with get_db() as db:
        db.query(CeremonyEntity).delete()
        db.add(CeremonyEntity(name='Semifinal 1', code='SF1'))
        db.add(CeremonyEntity(name='Semifinal 2', code='SF2'))
        db.add(CeremonyEntity(name='Grand Final', code="GF"))


def populate_score_types():
    with get_db() as db:
        db.query(ScoreTypeEntity).delete()
        db.add(ScoreTypeEntity(name='Jury'))
        db.add(ScoreTypeEntity(name='Televote'))


def check_dataframe_has_columns(dataframe: pd.DataFrame, columns: list[str]): 
    if not all(col in dataframe.columns for col in columns):
        raise Exception("Dataframe has not the required columns")
    

if __name__ == '__main__':
    # Add here your source files
    events_csv = r""
    countries_csv = r""
    songs_csv = r""
    populate_ceremony_types()
    populate_events_with_ceremonies(events_csv)
    populate_countries(countries_csv)
    populate_songs(songs_csv)
    populate_score_types()
