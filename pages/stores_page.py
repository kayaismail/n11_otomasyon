"""
N11 Stores Page Object Model.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import random
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class StoresPage(BasePage):
    """N11 Stores page  of https://www.n11.com/magazalar"""
    
    # Private locators
    LETTERS_CONTAINER = (By.CLASS_NAME, "letters")
    SELLER_TITLE = (By.XPATH, "//a[contains(@class, 'btnGreen') and @title='Mağaza Aç']")
    
    STORES_URL = "https://www.n11.com/magazalar"
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)  # Modül bazlı logger
        self.navigate_to(self.STORES_URL)  # Generic method kullan
        self.check()

    def check(self):
        """Check if page is loaded correctly."""
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.LETTERS_CONTAINER))
            self.logger.info("Letters container is visible")
        except TimeoutException:
            self.logger.error("Timeout: Letters container not visible after 10 seconds")
            raise

    def click_letter(self, letter: str) -> None:
        """
        Filters stores by starting letter.
        
        Args:
            letter: Letter to filter by (e.g., "S")
        """
        # Click on the letter filter within letters container
        letter_locator = (By.CSS_SELECTOR, '.letters span[data-has-seller="{}"]'.format(letter))
        
        # Use default Selenium click with explicit wait
        self.wait.for_element_clickable(letter_locator)
        element = self.driver.find_element(*letter_locator)
        element.click()
        
        # Wait for page to load using WaitHelper
        self.wait.wait_for_page_load()
        self.logger.info("Filtered stores by letter: {}".format(letter))

    def get_store_count(self) -> int:
        """
        Gets total number of stores in the list.
        
        Returns:
            Number of stores
        """
        store_list_locator = "div.tabPanel.allSellers > div.sellerListHolder > ul > li"
        stores = self.driver.find_elements(By.CSS_SELECTOR, store_list_locator)
        count = len(stores)
        self.logger.info(f"Found {count} stores in the list")
        return count
    
    def get_random_store_index(self) -> int:
        """
        Generates a random store index.
        
        Returns:
            Random index (1-based for CSS nth-child)
        """
        store_count = self.get_store_count()
        if store_count == 0:
            raise Exception("No stores found in the list")
        
        random_index = random.randint(1, store_count)
        self.logger.info(f"Generated random store index: {random_index} (total stores: {store_count})")
        return random_index
    
    def click_store_by_index(self, index: int):
        """
        Clicks on a store by its index.

        Args:
            index: Store index (1-based)
        """
        # Try to find the store link directly
        store_link_locator = (By.CSS_SELECTOR, "div.tabPanel.allSellers > div.sellerListHolder > ul > li:nth-child({}) a".format(index))

        # Use default Selenium click with explicit wait
        self.wait.for_element_clickable(store_link_locator)
        element = self.driver.find_element(*store_link_locator)
        element.click()

        self.logger.info("Clicked on store at index: {}".format(index))
        from pages.search_result_page import ResultViewPage
        return ResultViewPage(self.driver)
    
    def filter_and_click_random_store(self, letter: str) -> int:
        """
        Filters stores by letter and clicks on a random one.
        
        Args:
            letter: Letter to filter by (e.g., "S")
            
        Returns:
            Index of the clicked store
        """
        # Step 1: Filter by letter
        self.click_letter(letter)
        
        # Step 2: Get random index
        random_index = self.get_random_store_index()
        
        # Step 3: Click on random store
        self.click_store_by_index(random_index)
        
        self.logger.info("Filtered by '{}' and clicked store at index: {}".format(letter, random_index))
        return random_index
    
    