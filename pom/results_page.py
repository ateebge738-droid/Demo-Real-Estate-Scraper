from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.logger import get_logger
from selenium.common.exceptions import TimeoutException as e
from selenium.common.exceptions import ElementClickInterceptedException as c
import time
from utilities.config import DEMO

class ResultsPage():
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = get_logger(self.__class__.__name__)

    listing_cards = (By.CSS_SELECTOR, "li[role='article'][aria-label='Listing']")
    listing_links = (By.CSS_SELECTOR, "a[aria-label='Listing link']")
    listing_imgs = (By.CSS_SELECTOR, "img[aria-label='Listing photo']")
    listing_currency = (By.CSS_SELECTOR, "span[aria-label='Currency']")
    listing_price = (By.CSS_SELECTOR, "span[aria-label='Price']")
    listing_location = (By.CSS_SELECTOR, "div[aria-label='Location']")
    listing_beds = (By.CSS_SELECTOR, "span[aria-label='Beds']")
    listing_baths = (By.CSS_SELECTOR, "span[aria-label='Baths']")
    listing_area = (By.CSS_SELECTOR, "span[aria-label='Area'] span")
    listing_creation = (By.CSS_SELECTOR, "span[aria-label='Listing creation date']")
    listing_update = (By.CSS_SELECTOR, "span[aria-label='Listing updated date']")

    next_btn = (By.CSS_SELECTOR, 'a[title="Next"]')
    def scrape_listings(self):
        all_info = []
        page_no = 2
        while True:
            self.logger.info('Waiting for Cards')
            cards = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(self.listing_cards)
                )
            self.logger.info(f'{len(cards)} Cards Located')

            page_info = []
            self.logger.info('About to loop through each card')

            card_no = 1
            for card in cards:
                try:
                    card_link = card.find_element(*self.listing_links).get_attribute('href')
                except:
                    card_link = 'N/A'

                try:
                    card_image = card.find_element(*self.listing_imgs).get_attribute('src')
                except:
                    card_image = 'N/A'

                try:
                    card_currency = card.find_element(*self.listing_currency).text
                except:
                    card_currency = 'N/A'

                try:
                    card_price = card.find_element(*self.listing_price).text
                except:
                    card_price = 'N/A'

                try:
                    card_location = card.find_element(*self.listing_location).text
                except:
                    card_location = 'N/A'

                try:
                    card_beds = card.find_element(*self.listing_beds).text
                except:
                    card_beds = 'N/A'

                try:
                    card_baths = card.find_element(*self.listing_baths).text
                except:
                    card_baths = 'N/A'

                try:
                    card_area = card.find_element(*self.listing_area).text
                except:
                    card_area = 'N/A'

                try:
                    card_creation = card.find_element(*self.listing_creation).text
                except:
                    card_creation = 'N/A'

                try:
                    card_update = card.find_element(*self.listing_update).text
                except:
                    card_update = 'N/A'

                #Concatenating the price and currency
                currency_price = str(card_currency) + ' ' + str(card_price)

                listing = {
                        'Location': card_location,
                        'Area': card_area,
                        'No. of Beds': card_beds,
                        'No. of Baths': card_baths,
                        'Price': currency_price,
                        'Date Listed': card_creation,
                        'Date Updated': card_update,
                        'Link': card_link,
                        'Image Link': card_image
                    }

                if DEMO:
                    listing = self.sanitize_listing(listing)

                #Arranging the info in a dictionary and appending to the 'all_info' list. Each dictionary contains full info of one listing
                page_info.append(listing
                )
            
            all_info.extend(page_info)
            self.logger.info(f'Length of all_info {len(all_info)}')

            #Basically, checking for the presence of the next button and clicking. If it is not present then exiting the infinite loop.
            self.logger.info('Finished Scraping page')
            self.logger.info('Checking for availability of next page')           
            try:
                
                for _ in range(3):
                    try:
                        self.logger.info('Waiting for clickability of next button')
                        pagination_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.next_btn))
                        self.logger.info('Next button found')
                        self.driver.execute_script('arguments[0].scrollIntoView({behavior: "smooth", block: "center"});', pagination_button)
                        #y = pagination_button.location['y']
                        #driver.execute_script(f"window.scrollTo(0, {y - 100});")
                        pagination_button.click()
                        self.logger.info('Next Button clicked')
                        self.logger.info(f'Moving to Page: {page_no}')
                        page_no += 1
                        break

                    except c:
                        time.sleep(0.3)
                        self.logger.error('Could not click next button, trying agian.')
                else:
                    print('Click blocked repeatedly.')
                    return all_info

            except e:
                self.logger.info('No more pages')
                return all_info
                break

    def sanitize_listing(self, data: dict) -> dict:
        return {
            'Location': 'Sample Location',
            'Area': data.get('Area', 'N/A'),
            'No. of Beds': data.get('No. of Beds', 'N/A'),
            'No. of Baths': data.get('No. of Baths', 'N/A'),
            'Price': 'XXXXX',
            'Date Listed': 'N/A',
            'Date Updated': 'N/A',
            'Link': 'N/A',
            'Image Link': 'N/A'
        }