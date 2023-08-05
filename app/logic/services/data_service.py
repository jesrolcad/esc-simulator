import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from app.core.config import BaseSettings as Settings
from app.utils import constants
from app.logic.services.base_service import BaseService
from app.logic.services.song_service import SongService
from app.persistence.repositories.event_repository import EventRepository
from app.persistence.repositories.country_repository import CountryRepository
from app.persistence.repositories.song_repository import SongRepository
from app.persistence.repositories.ceremony_repository import CeremonyRepository
from app.logic.models import Country, Event, Song, Ceremony, CeremonyType
from app.logic.model_mappers import CeremonyModelMapper, EventModelMapper, CountryModelMapper, SongModelMapper
from app.utils.exceptions import AlreadyExistsError

SCRAPING_BASE_URL = "https://eurovisionworld.com/eurovision/"

GITHUB_ACTIONS_CHROME_DRIVER_PATH = "/usr/bin/chromedriver"

if os.getenv('GITHUB_ACTIONS') == 'true':
    service = Service(GITHUB_ACTIONS_CHROME_DRIVER_PATH)

else:
    service = Service(Settings.CHROME_DRIVER_PATH)

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

class DataService(BaseService):

    def selenium_scraping(self, url: str, chrome_driver: webdriver.Chrome)-> str:
        chrome_driver.get(url)
        chrome_driver.maximize_window()
        html_source_code = chrome_driver.execute_script("return document.body.innerHTML;")
        return html_source_code

    def scrape_data(self, years: list[int]):
        for year in years:
            event = EventRepository(self.session).get_event(year=year)
            if event:
                raise AlreadyExistsError("Event", event.id, message=f"Event for year {year} already exists")
            else:
                general_html = self.selenium_scraping(url=SCRAPING_BASE_URL + str(year),chrome_driver=driver)
                soup = BeautifulSoup(general_html, "html.parser")
                event_data = soup.find("div", class_="voting_info mm")
                last_year_winner_country_name = self.scrape_winner_country_from_last_year(last_year=year-1)
                last_year_winner_country = (CountryModelMapper().map_to_country_model(CountryRepository(self.session)
                                                                    .get_country(name=last_year_winner_country_name)))
                event = self.scrape_event_info(event_data=event_data)
                data_list = soup.find("div", id="voting_table").find_all("tr", id=True)
                for data in data_list:
                    country = self.scrape_country_info(country_data=data)
                    self.scrape_song_info(song_data=data, associated_event=event, associated_country=country, 
                                            last_year_winner_country=last_year_winner_country)

    def scrape_event_info(self, event_data: str)-> Event:
        try:
            date_str = event_data.p.span.text
            host_city = event_data.p.find_all("a")[0].text
            arena = event_data.p.find_all("a")[1].text
        except AttributeError:
            date_str = event_data.p.a.text
            host_city = event_data.p.find_all("a")[1].text
            arena = event_data.p.find_all("a")[2].text

        date_format = "%d %B %Y"
        grand_final_date = datetime.strptime(date_str, date_format)
        slogan = event_data.p.find_all()[-1].text

        event = Event(year=grand_final_date.year, slogan=slogan, host_city=host_city, arena=arena)
        created_event = EventModelMapper().map_to_event_model(EventRepository(self.session).create_event(event=event))

        first_semifinal_ceremony = CeremonyModelMapper().map_to_ceremony_entity((Ceremony(date=grand_final_date - timedelta(days=4), 
                                            event=created_event, ceremony_type=CeremonyType(id=1, name="Semifinal 1", code="SF1"))))
        
        second_semifinal_ceremony = CeremonyModelMapper().map_to_ceremony_entity((Ceremony(date=grand_final_date - timedelta(days=2), 
                                            event=created_event, ceremony_type=CeremonyType(id=2, name="Semifinal 2", code="SF2"))))
        
        grand_final_ceremony = CeremonyModelMapper().map_to_ceremony_entity((Ceremony(date=grand_final_date, event=created_event, 
                                                                            ceremony_type=CeremonyType(id=3, name="Grand Final", code="GF"))))
        

        for ceremony_entity in [first_semifinal_ceremony, second_semifinal_ceremony, grand_final_ceremony]:
            CeremonyRepository(self.session).create_ceremony(ceremony=ceremony_entity)

        return created_event


    def scrape_country_info(self, country_data: str)-> Country:
        country_name = country_data.a['title'].split(" in")[0].strip()
        country_code = constants.COUNTRY_NAME_TO_CODE.get(country_name, constants.UNREGISTERED_COUNTRY_CODE)
        country = Country(name=country_name, code=country_code)
        existing_country = CountryRepository(self.session).get_country(name=country_name)

        if existing_country:
            return CountryModelMapper().map_to_country_model(existing_country)

        created_country = CountryModelMapper().map_to_country_model(CountryRepository(self.session).create_country(country=country))
        
        return created_country


    def scrape_song_info(self, song_data: str, associated_event: Event, associated_country: Country, last_year_winner_country: Country):
        song_position = int(song_data.td.text)
        html_class = "r500n"
        if song_position < 27: # this is a general rule, but there are some exceptions, like ESC 2022 (25 songs in the final)
            html_class = "v_td_point"
        try:
            header = song_data.find("td", class_= html_class).find_previous_sibling().a['title'].split(":")
        except AttributeError:
            header = song_data.find("td", class_= "r500n").find_previous_sibling().a['title'].split(":")
        song_and_artist = header[1].split("-")
        song_artist = song_and_artist[0].strip()
        song_title = song_and_artist[1].strip().replace('"', "")
        jury_potential_score, televote_potential_score = SongService(self.session).calculate_potential_scores(position=song_position)
        belongs_to_host_country = last_year_winner_country.id == associated_country.id
        Song.update_forward_refs()
        song = Song(title=song_title, artist=song_artist, position=song_position, jury_potential_score=jury_potential_score, 
                    televote_potential_score=televote_potential_score, belongs_to_host_country=belongs_to_host_country,
                    country=associated_country, event=associated_event)

        song_entity = SongModelMapper().map_to_song_entity(song)

        return SongModelMapper().map_to_song_model(SongRepository(self.session).create_song(song=song_entity))


    def scrape_winner_country_from_last_year(self, last_year: int)->str:
        general_html = self.selenium_scraping(url=SCRAPING_BASE_URL + str(last_year),chrome_driver=driver)
        soup = BeautifulSoup(general_html, "html.parser")
        winner_data = soup.find("div", id="voting_table").find_all("tr", id=True)[0]
        country_name = winner_data.a['title'].split(" in")[0].strip()
        return country_name






