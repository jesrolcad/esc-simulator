import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from app.core.config import Settings
from app.utils import constants
from app.repositories import country_repository
from app.db.models import Country

SCRAPING_BASE_URL = "https://eurovisionworld.com/eurovision/"

service = Service(Settings.CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

def selenium_scraping(url: str, driver: webdriver.Chrome)-> str:
    driver.get(url)
    driver.maximize_window()
    html_source_code = driver.execute_script("return document.body.innerHTML;")
    return html_source_code


def populate_db(years: list[int]):
    for year in years:
        general_html = selenium_scraping(SCRAPING_BASE_URL + year,driver)
        soup = BeautifulSoup(general_html, "html.parser")
        data_list = soup.find("div", id="voting_table").find_all("tr", id=True)
        for data in data_list:
            country_link_info = "https://eurovisionworld.com" + data.a['href']
            song_link_info = country_link_info.split("/")[-1]
            country_name = data.a['title'].split(" in")[0].strip()
            if not country_repository.exists_country_by_name(country_name):
                country = Country(name=country_name, code=constants.COUNTRY_NAME_TO_CODE.get(country_name, constants.UNREGISTERED_COUNTRY_CODE))
                # country_repository.create_country(country_name, COUNTRY_NAME_TO_CODE[country_name])





