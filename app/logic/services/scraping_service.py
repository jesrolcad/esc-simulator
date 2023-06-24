from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from app.core.config import Settings
from app.utils import constants
from app.logic.services import country_service
from app.logic.models.country import Country

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
        general_html = selenium_scraping(url=SCRAPING_BASE_URL + year,chrome_driver=driver)
        soup = BeautifulSoup(general_html, "html.parser")
        data_list = soup.find("div", id="voting_table").find_all("tr", id=True)
        for data in data_list:
            scrape_country_info(country_data=data)
            country_link_info = "https://eurovisionworld.com" + data.a['href']
            


def scrape_country_info(country_data: str)-> int:
    country_name = country_data.a['title'].split(" in")[0].strip()
    existing_country = country_service.get_country(name=country_name)
    if not existing_country:
        country_code = constants.COUNTRY_NAME_TO_CODE.get(country_name, constants.UNREGISTERED_COUNTRY_CODE)
        country = Country(name=country_name, code=country_code)
        country_id = country_service.create_country(country)    

    else:
        country_id = existing_country.id
    
    return country_id


def scrape_song_info(song_data: str, associated_event_id: int, associated_country_id: int):
    song_position = int(song_data.td.text)
    html_class = "r500n"
    header = song_data.find("td", class_= html_class).find_previous_sibling().a['title'].split(":")
    song_and_artist = header[1].split("-")
    song_artist = song_and_artist[0].strip()
    song_title = song_and_artist[1].strip().replace('"', "")

    #TODO: Scrape last year's winner to fill in belongs_to_host_country field



    




