from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Function for Waiting for visibility of a single element
def wait_visible(driver, locator):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))