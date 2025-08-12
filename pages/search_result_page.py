"""
N11 Result View Page Object Model.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ResultViewPage(BasePage):
    """N11 Result View page for search results."""

    # Private locators for result view page
    RESULT_VIEW = (By.CSS_SELECTOR, ".resultView")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".searchResults")
    PRODUCT_LIST = (By.CSS_SELECTOR, ".productList")
    STORE_PRODUCTS = (By.CSS_SELECTOR, ".storeProducts")

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
                    EC.visibility_of_element_located(self.RESULT_VIEW)
                )
            )
            logging.info("Result view page loaded successfully")
        except TimeoutException:
            logging.error("Timeout: Result view page not loaded after 10 seconds")
            raise

    def wait_for_store_page_load(self) :
        """Waits for store page to load after clicking store."""
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: 'arama?s=' in driver.current_url
            )
            logging.info("Store page loaded successfully - URL contains 'arama?s='")
        except TimeoutException:
            logging.error("Timeout: URL does not contain 'arama?s=' after 10 seconds")
            raise
    
    def verify_result_view_element(self):
        """
        Verifies that .resultView element is present and visible on the page.
        
        Returns:
            True if element is found and visible, False otherwise
        """
        try:
            # Wait for .resultView element to be visible
            self.wait.for_element_visible(self.RESULT_VIEW, timeout=10)
            
            # Additional check to ensure element is displayed
            result_view_element = self.driver.find_element(*self.RESULT_VIEW)
            
            if result_view_element.is_displayed():
                logging.info(".resultView element is present and visible")
                return True
            else:
                logging.warning(".resultView element found but not visible")
                return False
                
        except Exception as e:
            logging.error(".resultView element not found or not visible: {}".format(e))
            
            # Log current URL for debugging
            current_url = self.driver.current_url
            logging.info("Current URL: {}".format(current_url))
            
            # Try to find alternative elements
            try:
                search_results = self.driver.find_element(*self.SEARCH_RESULTS)
                if search_results.is_displayed():
                    logging.info("Alternative element .searchResults found and visible")
                    return True
            except:
                pass
            
            return False


   