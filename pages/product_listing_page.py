"""
N11 Product Listing Page Object Model.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ProductListingPage(BasePage):
    """N11 Product Listing page for search results."""

    # Private locators for product listing page
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".btnBasket")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".productItem")
    PRODUCT_LIST = (By.CSS_SELECTOR, ".productList")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".searchResults")
    ITEMS_INFO = (By.CSS_SELECTOR, ".items-info")
    SKUS_ITEM = (By.CSS_SELECTOR, ".skus-item")
    JS_ADD_BASKET_SKU = (By.ID, "js-addBasketSku")

    def __init__(self, driver):
        """Initialize ProductListingPage."""
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        # URL'e navigate etmeye gerek yok, zaten result sayfasındayız
        
        self.check()

    def check(self):
        """Check if product listing page is loaded correctly."""
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ADD_TO_CART_BUTTON))
            self.logger.info("Add to cart button is visible")
        except TimeoutException:
            self.logger.error("Timeout: add to cart button not visible after 10 seconds")
            raise
    
    def is_product_added_to_cart(self) -> bool:
        """Check if product is added to cart."""
        try:
            self.wait.for_element_visible(self.ITEMS_INFO, timeout=15)
            return True
        except TimeoutException:
            return False

    # Özel metodlar - Açıklayıcı ve güvenli
    def click_skus_item(self, index: int = 1) -> None:
        """Clicks on SKUS item by index."""
        self._click_element_by_index(self.SKUS_ITEM, index, "SKUS item")
    
    def click_add_to_cart_button(self, index: int = 1) -> None:
        """
        Clicks on add to cart button by index.
        
        Args:
            index: Index of add to cart button to click (1-based, default: 1)
        """
        try:
            # Tüm add to cart buttonları bul
            elements = self.driver.find_elements(*self.ADD_TO_CART_BUTTON)
            self.logger.info(f"Found {len(elements)} add to cart buttons")
            
            # Index kontrolü
            if index < 1 or index > len(elements):
                raise Exception(f"Index {index} out of range. Found {len(elements)} add to cart buttons")
            
            # İstenen index'teki elementi al (1-based index)
            target_element = elements[index - 1]
            
            # Element'i görünür hale getir
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", target_element)
            
            # Kısa bekleme
            import time
            time.sleep(1)
            
            # Element'in tıklanabilir olmasını bekle
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            
            # Element'in kendisinin tıklanabilir olmasını bekle
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(target_element))
            
            # Tıkla
            target_element.click()
            self.logger.info(f"Clicked add to cart button at index: {index} (total: {len(elements)})")
            
        except Exception as e:
            self.logger.error(f"Error clicking add to cart button at index {index}: {e}")
            raise
    
    # Private yardımcı metodlar - Kod tekrarını önler
    def _click_element_by_index(self, locator: tuple, index: int, element_name: str) -> None:
        """Generic method to click element by index."""
        try:
            # Tüm elementleri bul
            elements = self.driver.find_elements(*locator)
            
            # Index kontrolü
            if index < 1 or index > len(elements):
                raise Exception(f"Index {index} out of range. Found {len(elements)} {element_name} elements")
            
            # İstenen index'teki elementi al (1-based index)
            element = elements[index - 1]
            
            # Element'i görünür hale getir (scroll)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            
            # Kısa bir bekleme
            import time
            time.sleep(1)
            
            # Element'in tıklanabilir olmasını bekle
            self.wait.for_element_clickable(locator, timeout=15)
            
            # Tıkla
            element.click()
            self.logger.info(f"Clicked {element_name} at index: {index} (total: {len(elements)})")
            
        except Exception as e:
            self.logger.error(f"Error clicking {element_name} at index {index}: {e}")
            raise
    
    def _click_element(self, locator: tuple, element_name: str) -> None:
        """Generic method to click element."""
        try:
            self.wait.for_element_clickable(locator, timeout=15)
            element = self.driver.find_element(*locator)
            element.click()
            self.logger.info(f"Clicked {element_name}")
        except Exception as e:
            self.logger.error(f"Error clicking {element_name}: {e}")
            raise

    def get_item_count(self, locator: tuple, item_name: str = "item") -> int:
        """
        Gets the number of items available for any locator.
        
        Args:
            locator: Tuple(By, value) - Locator to find elements
            item_name: str - Name of the item for logging
            
        Returns:
            Number of items found
        """
        try:
            elements = self.driver.find_elements(*locator)
            count = len(elements)
            self.logger.info(f"Found {count} {item_name} elements")
            return count
        except Exception as e:
            self.logger.error(f"Error getting {item_name} count: {e}")
            return 0
    
    def get_skus_items_count(self) -> int:
        """
        Gets the number of SKUS items available.
        
        Returns:
            Number of SKUS items
        """
        return self.get_item_count(self.SKUS_ITEM, "SKUS item")

    def get_add_to_cart_button_count(self) -> int:
        """
        Gets the number of add to cart buttons available.
        
        Returns:
            Number of add to cart buttons
        """
        return self.get_item_count(self.ADD_TO_CART_BUTTON, "add to cart button")
    
    def click_js_add_basket_sku(self) -> None:
        """Clicks on JS add basket sku."""
        self._click_element(self.JS_ADD_BASKET_SKU, "JS add basket sku")
    
    def has_skus_items(self) -> bool:
        """
        Check if product has SKU variants.
        
        Returns:
            True if SKU items exist, False otherwise
        """
        try:
            skus_count = self.get_skus_items_count()
            has_skus = skus_count > 0
            self.logger.info(f"Product has SKUs: {has_skus} (count: {skus_count})")
            return has_skus
        except Exception as e:
            self.logger.error(f"Error checking SKUs existence: {e}")
            return False
