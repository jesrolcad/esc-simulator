import pandas as pd
from app.db.database import get_db
from app.persistence.entities import EventEntity, CountryEntity, SongEntity, CeremonyEntity, CeremonyTypeEntity, VotingTypeEntity
from app.utils.constants import COUNTRY_NAME_TO_CODE
from app.utils.song_functions import calculate_potential_scores

#CeremonyEntity dates must be populated manually in the database

def populate_events_with_ceremonies(path: str):
    dataframe = pd.read_csv(path)
    check_dataframe_has_columns(dataframe, ['year', 'slogan', 'host_city', 'arena'])
    
    with get_db() as db_session:
        for row in dataframe.itertuples(index=False):
            event = EventEntity(year=row.year, slogan=row.slogan, 
                    host_city=row.host_city, arena=row.arena)
            db_session.add(event)
            for ceremony_type_id in range(1,4):
                ceremony = CeremonyEntity(ceremony_type_id=ceremony_type_id, event_id=row.id)
                db_session.add(ceremony)


def populate_countries(path: str):
    dataframe = pd.read_csv(path)
    check_dataframe_has_columns(dataframe, ['name'])

    with get_db() as db_session:
        for row in dataframe.itertuples(index=False):
            country = CountryEntity(name=row.name, code=COUNTRY_NAME_TO_CODE[row.name])
            db_session.add(country)


def populate_songs(path: str):
    dataframe = pd.read_csv(path)
    check_dataframe_has_columns(dataframe, ['title', 'artist', 'country_id', 'event_id', 'belongs_to_host_country'])

    with get_db() as db_session:
        data = [{'title': row.title, 'artist': row.artist, 'country_id': row.country_id, 'event_id': row.event_id,
        'jury_potential_score': calculate_potential_scores(row.position)[0],
        'televote_potential_score': calculate_potential_scores(row.position)[1],
        'belongs_to_host_country': row.belongs_to_host_country} for row in dataframe.itertuples(index=False)]

        db_session.bulk_insert_mappings(SongEntity, data)


def populate_ceremony_types():
    with get_db() as db_session:
        db_session.add(CeremonyTypeEntity(name='Semifinal 1', code='SF1'))
        db_session.add(CeremonyTypeEntity(name='Semifinal 2', code='SF2'))
        db_session.add(CeremonyTypeEntity(name='Grand Final', code="GF"))


def populate_score_types():
    with get_db() as db_session:
        db_session.add(VotingTypeEntity(name='Jury'))
        db_session.add(VotingTypeEntity(name='Televote'))

def check_dataframe_has_columns(dataframe: pd.DataFrame, columns: list[str]): 
    if not all(col in dataframe.columns for col in columns):
        raise Exception("Dataframe has not the required columns")
    

if __name__ == '__main__':
    # Add here your source files
    EVENTS_CSV = r""
    COUNTRIES_CSV = r""
    SONGS_CSV = r""
    populate_ceremony_types()
    populate_events_with_ceremonies(EVENTS_CSV)
    populate_countries(COUNTRIES_CSV)
    populate_songs(SONGS_CSV)
    populate_score_types()
