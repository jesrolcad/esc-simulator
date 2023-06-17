from database import get_db
from models import Event, Country, Song
import pandas as pd
from utils.constants import COUNTRY_NAME_TO_CODE
from random import randint


def populate_events(path: str):
    dataframe = pd.read_csv(path)
    check_dataframe_has_columns(dataframe, ['year', 'slogan', 'host_city', 'arena'])
    
    with get_db() as db:
        db.query(Event).delete()
        for row in dataframe.itertuples(index=False):
            event = Event(year=row.year, slogan=row.slogan, 
                    host_city=row.host_city, arena=row.arena)
            db.add(event)


def populate_countries(path: str):
    dataframe = pd.read_csv(path)
    check_dataframe_has_columns(dataframe, ['name'])

    with get_db() as db:
        db.query(Country).delete()
        for row in dataframe.itertuples(index=False):
            country = Country(name=row.name, code=COUNTRY_NAME_TO_CODE[row.name])
            db.add(country)


def populate_songs(path: str):
    dataframe = pd.read_csv(path)
    check_dataframe_has_columns(dataframe, ['title', 'artist', 'country_id'])

    with get_db() as db:
        db.query(Song).delete()
        for row in dataframe.itertuples(index=False):
            jury_potential_score = randint(1, 10)
            televote_potential_score = randint(1, 10)
            song = Song(title=row.title, artist=row.artist, country_id=row.country_id, jury_potential_score=jury_potential_score,
                televote_potential_score=televote_potential_score)
            db.add(song)


def check_dataframe_has_columns(dataframe: pd.DataFrame, columns: list[str]): 
    if not all(col in dataframe.columns for col in columns):
        raise Exception("Dataframe has not the required columns")


if __name__ == '__main__':
    populate_events(r'C:\Users\Jesus\Desktop\Proyectos\esc-simulator\db\data\events.csv')
    populate_countries(r'C:\Users\Jesus\Desktop\Proyectos\esc-simulator\db\data\countries.csv')
    populate_songs(r'C:\Users\Jesus\Desktop\Proyectos\esc-simulator\db\data\songs.csv')

