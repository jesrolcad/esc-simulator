import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from app.utils import constants

# option = webdriver.ChromeOptions()
# option.headless = True
# option.add_argument("--incognito")
# driver = webdriver.Chrome("C:/Scraping/chromedriver.exe", chrome_options=option)

def selenium_scraping(url: str, driver: webdriver.Chrome)-> str:
    driver.get(url)
    driver.maximize_window()
    html_source_code = driver.execute_script("return document.body.innerHTML;")
    return html_source_code


def populate_db(years: list[int]):
    return 0

