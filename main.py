# %%
from selenium import webdriver
from utilities.logger import get_logger
logger = get_logger(__name__)
from selenium.webdriver.chrome.options import Options

from utilities.config import CITY_NAME, LOCATION, BASE_URL, DEMO

import pom.home_page
import pom.results_page

from importlib import reload
reload(pom.home_page)
reload(pom.results_page)

from pom.home_page import HomePage
from pom.results_page import ResultsPage

import json
import csv
import pandas as pd

# %%
options = Options()
options.add_experimental_option(
    'prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'profile.password_leak_detection_enabled': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.popups': 0
	}
)

options.add_argument('--disable-notifications')
options.add_argument('--disable-autofill')
options.add_argument('--disable-save-password-bubble')
options.add_argument('--guest')
options.add_argument('--incognito')
options.add_argument('--disable-info-bars')
options.add_argument('--disable-popup-blocking')

# %%
logger.info('Launching Browser')
driver = webdriver.Chrome(options=options)
driver.get(BASE_URL)

home = HomePage(driver)
home.search(CITY_NAME, LOCATION)

results = ResultsPage(driver)
info = results.scrape_listings()

# %%
if not info:
    logger.warning('No listings collected')
    driver.quit()
    exit()

# %%
with open('data/property_listings.json', 'w') as f:
    json.dump(info, f, indent=4)

headers = info[0].keys()
with open('data/property_listings.csv', 'w', newline="") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(info)

df = pd.DataFrame(info)
df.to_excel('data/property_listings.xlsx', index = False)


