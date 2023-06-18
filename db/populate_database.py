import datetime
from database import get_db
from models import Event, Country, Song, Ceremony, CeremonyType
import pandas as pd
from utils.constants import COUNTRY_NAME_TO_CODE
from random import randint


def populate_events_with_ceremonies(path: str):
    dataframe = pd.read_csv(path)
    check_dataframe_has_columns(dataframe, ['year', 'slogan', 'host_city', 'arena'])
    
    with get_db() as db:
        db.query(Event).delete()
        db.query(Ceremony).delete()
        for row in dataframe.itertuples(index=False):
            event = Event(year=row.year, slogan=row.slogan, 
                    host_city=row.host_city, arena=row.arena)
            db.add(event)
            for ceremony_type_id in range(1,4):
                ceremony = Ceremony(ceremony_type_id=ceremony_type_id, event_id=row.id)
                db.add(ceremony)


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
            jury_potential_score, televote_potential_score = calculate_potential_scores(row.position)
            song = Song(title=row.title, artist=row.artist, country_id=row.country_id, jury_potential_score=jury_potential_score,
                televote_potential_score=televote_potential_score)
            db.add(song)

def populate_ceremony_types():
    with get_db() as db:
        db.query(CeremonyType).delete()
        db.add(CeremonyType(name='Semifinal 1', code='SF1'))
        db.add(CeremonyType(name='Semifinal 2', code='SF2'))
        db.add(CeremonyType(name='Grand Final', code="GF"))
    


def check_dataframe_has_columns(dataframe: pd.DataFrame, columns: list[str]): 
    if not all(col in dataframe.columns for col in columns):
        raise Exception("Dataframe has not the required columns")
    

def calculate_potential_scores(position: int)-> tuple:
    """
    Calculate the potential scores for a song based on its position in the final ranking
    returns a tuple: (jury_potential_score, televote_potential_score)
    """
    if position in range(1,4):
        return (randint(9, 10), randint(9, 10))
    
    elif position in range (4, 6):
        return (randint(8, 9), randint(8, 9))
    
    elif position in range (6, 11):
        return (randint(7, 9), randint(7, 9))
    
    elif position in range (11, 16):
        return (randint(6, 8), randint(6, 8))
    
    elif position in range (16, 21):
        return (randint(5, 7), randint(5, 7))
    
    elif position in range (21, 28):
        return (randint(2, 5), randint(2, 5))
    
    else:
        return (randint(1, 4), randint(1, 4))

if __name__ == '__main__':
    populate_ceremony_types()
    populate_events_with_ceremonies(r'C:\Users\Jesus\Desktop\Proyectos\esc-simulator\db\data\events.csv')
    populate_countries(r'C:\Users\Jesus\Desktop\Proyectos\esc-simulator\db\data\countries.csv')
    populate_songs(r'C:\Users\Jesus\Desktop\Proyectos\esc-simulator\db\data\songs.csv')
