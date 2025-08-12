"""
N11 Result View Page Object Model.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ProductListingPage(BasePage):
    """N11 Result View page for search results."""

    # Private locators for result view page
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".btnBasket")


    def __init__(self, driver):
        """Initialize ResultViewPage."""
        super().__init__(driver)
        # URL'e navigate etmeye gerek yok, zaten result sayfasındayız
        
        self.check()

    def check(self):
        """Check if result view page is loaded correctly."""
        try:
            # Wait for either resultView or search results to be visible
            WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.visibility_of_element_located(self.ADD_TO_CART_BUTTON)
                )
            )
            logging.info("Result view page loaded successfully")
        except TimeoutException:
            logging.error("Timeout: Result view page not loaded after 10 seconds")
            raise

    def click_add_to_cart_button(self):
        """Click on add to cart button."""
        self.wait.for_element_clickable(self.ADD_TO_CART_BUTTON)
        self.driver.find_element(*self.ADD_TO_CART_BUTTON).click()

