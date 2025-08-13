"""
N11 Home Page Object Model.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class HomePage(BasePage):
    """N11 Home page of https://www.n11.com"""
    
    # Private locators
    SEARCH_BOX = (By.ID, "searchData")
    SEARCH_BUTTON = (By.CLASS_NAME, "searchBtn")
    LOGO = (By.CLASS_NAME, "logo")
    
    HOME_URL = "https://www.n11.com"

    def __init__(self, driver):
        """Initialize HomePage."""
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self.navigate_to(self.HOME_URL)
        self.check()

    def check(self):
        """Check if page is loaded correctly."""
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.LOGO))
            self.logger.info("Home page loaded successfully")
        except TimeoutException:
            self.logger.error("Timeout: Home page not loaded after 10 seconds")
            raise
    
    def enter_search_keyword(self, keyword: str) -> None:
        """
        Enters search keyword in the search box.
        
        Args:
            keyword: The keyword to search for
        """
        self.type(self.SEARCH_BOX, keyword)
        self.logger.info(f"Entered search keyword: {keyword}")
    
    def click_search_button(self) -> None:
        """Clicks the search button on the home page."""
        self.click(self.SEARCH_BUTTON)
        self.logger.info("Clicked search button")
        self.wait.wait_for_page_load()
    
    def search_for_product(self, product_name: str) -> None:
        """
        Searches for a product.
        
        Args:
            product_name: Name of the product to search for
        """
        self.enter_search_keyword(product_name)
        self.click_search_button()
        self.logger.info(f"Searched for product: {product_name}")
        
    

    