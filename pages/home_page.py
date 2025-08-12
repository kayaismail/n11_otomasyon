"""
N11 Stores Page Object Model.
"""
from imp import SEARCH_ERROR
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import random
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class HomePage(BasePage):
    """N11 Stores page  of https://www.n11.com"""
    
    # Private locators
    LETTERS_CONTAINER = (By.CLASS_NAME, "letters")
    SEARCH_BUTTON = (By.ID, "#searchData")
    
    HOME_URL = "https://www.n11.com"

    def __init__(self, driver):
        """Initialize StoresPage."""
        super().__init__(driver)
        self.navigate_to(self.HOME_URL)
        self.check()

    def check(self):
        """Check if page is loaded correctly."""
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.LETTERS_CONTAINER))
            logging.info("Letters container is visible")
        except TimeoutException:
            logging.error("Timeout: Letters container not visible after 10 seconds")
            raise
    
    def click_search_button(self):
        """Click on search button."""
        self.wait.for_element_clickable(self.SEARCH_BUTTON)
        self.driver.find_element(*self.SEARCH_BUTTON).click()


    