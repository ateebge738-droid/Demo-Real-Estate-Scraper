from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utilities.helpers import wait_visible
from utilities.logger import get_logger
import time

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.logger = get_logger(self.__class__.__name__)

    city_field = (By.CSS_SELECTOR, 'div[aria-label="City filter"]')
    city_list = (By.CSS_SELECTOR, 'div[role="listbox"]') 
    city_list_btns = (By.CSS_SELECTOR, 'div[role="listbox"] span button') 
    location_field=(By.CSS_SELECTOR, 'div[aria-label="Location filter"] input')
    find_btn=(By.CSS_SELECTOR, 'a[aria-label="Find button"]')

    #Selecting city
    def select_city(self, city_name):
        try:
            ad_frame = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="3rd party ad content"]')))
            self.driver.switch_to.frame(ad_frame)
            close_btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[class="close_cross_big"]')))
            self.driver.execute_script("arguments[0].click();", close_btn)
            self.driver.switch_to.default_content()
        except:
            pass

        self.logger.info('Waiting for visibility of city_field')
        city_btn = wait_visible(self.driver, self.city_field)
        self.logger.info('City field sucessfully located')
       
        city_btn.click()
        self.logger.info('City field sucessfully clicked')
        
        city_btns = self.wait.until(EC.visibility_of_all_elements_located(self.city_list_btns))
        self.logger.info('City Buttons located in the dropdown box')
        self.logger.info(f'Number of City Buttons located {len(city_btns)}')

        found = False
        self.logger.info('Looking through the city buttons')
        for city_btn in city_btns:

            if city_name.strip().lower() in city_btn.text.strip().lower():
                self.logger.info(f'Found city, {city_name.strip().lower()}, {city_btn.text.strip().lower()}')

                city_btn.click()
                self.logger.info('City selected')

                found = True
                break

        if not found:
            self.logger.info('City not found in buttons')
            print('City not found in dropdown. Try another city.')

    def input_location(self, location_name):
        self.logger.info('Waiting for visibility of Location field')
        location_input = wait_visible(self.driver, self.location_field)
        self.logger.info('Location field sucessfully located')

        location_input.click()
        self.logger.info('Location field clicked')

        location_input.send_keys(location_name)
        time.sleep(0.3)
        location_input.send_keys(Keys.ENTER)
        self.logger.info(f'Sending {location_name} to Location field.')

    def click_find_btn(self):
        self.logger.info('Waiting for the Find button to be clickable')
        self.wait.until(EC.element_to_be_clickable(self.find_btn)).click()
        self.logger.info('Find Button clicked')

    def search(self, city_name, location_name):
        self.select_city(city_name)
        self.input_location(location_name)
        self.click_find_btn()