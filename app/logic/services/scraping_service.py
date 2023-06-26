from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from app.core.config import Settings
from app.utils import constants
from app.logic.services import event_service, country_service, song_service
from app.logic.models import Country, Event, Song


SCRAPING_BASE_URL = "https://eurovisionworld.com/eurovision/"

service = Service(Settings.CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

def selenium_scraping(url: str, chrome_driver: webdriver.Chrome)-> str:
    chrome_driver.get(url)
    chrome_driver.maximize_window()
    html_source_code = chrome_driver.execute_script("return document.body.innerHTML;")
    return html_source_code


def scrape_data(years: list[int]):
    for year in years:
        event = event_service.get_event(year=year)
        if not event:
            print(f"Scraping data for year {year}")
            
            general_html = selenium_scraping(url=SCRAPING_BASE_URL + str(year),chrome_driver=driver)
            soup = BeautifulSoup(general_html, "html.parser")
            event_data = soup.find("div", class_="voting_info mm")
            #TODO: get last year winner country scraping last year event
            last_year_winner = event_data.find("p", text='last year\'s winner').find("a").text
            last_year_winner_country = country_service.get_country(name=last_year_winner)
            event = scrape_event_info(event_data=event_data)
            data_list = soup.find("div", id="voting_table").find_all("tr", id=True)
            for data in data_list:
                country = scrape_country_info(country_data=data)
                scrape_song_info(song_data=data, associated_event=event, associated_country=country, 
                                        last_year_winner_country=last_year_winner_country)

def scrape_event_info(event_data: str)-> Event:
    date_str = event_data.p.a.text
    date_format = "%d %B %Y"
    grand_final_date = datetime.strptime(date_str, date_format)
    host_city = event_data.p.find_all("a")[0].text
    arena = event_data.p.find_all("a")[1].text
    slogan = event_data.p.find_all()[-1].text

    event = Event(year=grand_final_date.year, slogan=slogan, host_city=host_city, arena=arena)
    created_event = event_service.create_event_and_associated_ceremonies(event, grand_final_date)

    return created_event


def scrape_country_info(country_data: str)-> Country:
    country_name = country_data.a['title'].split(" in")[0].strip()
    country_code = constants.COUNTRY_NAME_TO_CODE.get(country_name, constants.UNREGISTERED_COUNTRY_CODE)
    country = Country(name=country_name, code=country_code)
    created_country = country_service.create_country(country)    
    
    return created_country


def scrape_song_info(song_data: str, associated_event: Event, associated_country: Country, last_year_winner_country: Country):
    song_position = int(song_data.td.text)
    html_class = "r500n"
    header = song_data.find("td", class_= html_class).find_previous_sibling().a['title'].split(":")
    song_and_artist = header[1].split("-")
    song_artist = song_and_artist[0].strip()
    song_title = song_and_artist[1].strip().replace('"', "")
    jury_potential_score, televote_potential_score = song_service.calculate_potential_scores(position=song_position)
    belongs_to_host_country = last_year_winner_country.id == associated_country.id
    song = Song(title=song_title, artist=song_artist, position=song_position, jury_potential_score=jury_potential_score, 
                televote_potential_score=televote_potential_score, belongs_to_host_country=belongs_to_host_country,
                country=associated_country, event=associated_event)

    return song_service.create_song(song=song)

if __name__ == '__main__':
    scrape_data(years=[2023])
    driver.quit()





