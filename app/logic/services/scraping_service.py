from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from app.core.config import Settings
from app.utils import constants
from app.logic.services.base_service import BaseService
from app.logic.services.event_service import EventService
from app.logic.services.country_service import CountryService
from app.logic.services.song_service import SongService
from app.logic.models import Country, Event, Song

SCRAPING_BASE_URL = "https://eurovisionworld.com/eurovision/"

service = Service(Settings.CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

class ScrapingService(BaseService):
    def selenium_scraping(self, url: str, chrome_driver: webdriver.Chrome)-> str:
        chrome_driver.get(url)
        chrome_driver.maximize_window()
        html_source_code = chrome_driver.execute_script("return document.body.innerHTML;")
        return html_source_code

    def scrape_data(self, years: list[int]):
        for year in years:
            event = EventService(self.session).get_event(year=year)
            if not event:
                print(f"Scraping data for year {year}")
                
                general_html = self.selenium_scraping(url=SCRAPING_BASE_URL + str(year),chrome_driver=driver)
                soup = BeautifulSoup(general_html, "html.parser")
                event_data = soup.find("div", class_="voting_info mm")
                last_year_winner_country_name = self.scrape_winner_country_from_last_year(last_year=year-1)
                last_year_winner_country = CountryService(self.session).get_country(name=last_year_winner_country_name)
                event = self.scrape_event_info(event_data=event_data)
                data_list = soup.find("div", id="voting_table").find_all("tr", id=True)
                for data in data_list:
                    country = self.scrape_country_info(country_data=data)
                    self.scrape_song_info(song_data=data, associated_event=event, associated_country=country, 
                                            last_year_winner_country=last_year_winner_country)

    def scrape_event_info(self, event_data: str)-> Event:
        date_str = event_data.p.span.text
        date_format = "%d %B %Y"
        grand_final_date = datetime.strptime(date_str, date_format)
        host_city = event_data.p.find_all("a")[0].text
        arena = event_data.p.find_all("a")[1].text
        slogan = event_data.p.find_all()[-1].text

        event = Event(year=grand_final_date.year, slogan=slogan, host_city=host_city, arena=arena)
        created_event = EventService(self.session).create_event_and_associated_ceremonies(event, grand_final_date)

        return created_event


    def scrape_country_info(self, country_data: str)-> Country:
        country_name = country_data.a['title'].split(" in")[0].strip()
        country_code = constants.COUNTRY_NAME_TO_CODE.get(country_name, constants.UNREGISTERED_COUNTRY_CODE)
        country = Country(name=country_name, code=country_code)
        created_country = CountryService(self.session).create_country(country)    
        
        return created_country


    def scrape_song_info(self, song_data: str, associated_event: Event, associated_country: Country, last_year_winner_country: Country):
        song_position = int(song_data.td.text)
        html_class = "r500n"
        header = song_data.find("td", class_= html_class).find_previous_sibling().a['title'].split(":")
        song_and_artist = header[1].split("-")
        song_artist = song_and_artist[0].strip()
        song_title = song_and_artist[1].strip().replace('"', "")
        jury_potential_score, televote_potential_score = SongService(self.session).calculate_potential_scores(position=song_position)
        belongs_to_host_country = last_year_winner_country.id == associated_country.id
        song = Song(title=song_title, artist=song_artist, position=song_position, jury_potential_score=jury_potential_score, 
                    televote_potential_score=televote_potential_score, belongs_to_host_country=belongs_to_host_country,
                    country=associated_country, event=associated_event)

        return SongService(self.session).create_song(song=song)


    def scrape_winner_country_from_last_year(self, last_year: int)->str:
        general_html = self.selenium_scraping(url=SCRAPING_BASE_URL + str(last_year),chrome_driver=driver)
        soup = BeautifulSoup(general_html, "html.parser")
        winner_data = soup.find("div", id="voting_table").find_all("tr", id=True)[0]
        country_name = winner_data.a['title'].split(" in")[0].strip()
        return country_name






