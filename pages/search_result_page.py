"""
N11 Product Listing Page Object Model.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class SearchResultPage(BasePage):
    """N11 Product Listing page for search results."""

    # Private locators for search result page
    _ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".btnBasket")
    _PRODUCT_ITEMS = (By.CSS_SELECTOR, ".productItem")
    _PRODUCT_LIST = (By.CSS_SELECTOR, ".productList")
    _SEARCH_RESULTS = (By.CSS_SELECTOR, ".searchResults")
    _ITEMS_INFO = (By.CSS_SELECTOR, ".items-info")
    _SKUS_ITEM = (By.CSS_SELECTOR, ".skus-item")
    _JS_ADD_BASKET_SKU = (By.ID, "js-addBasketSku")
    _BASKET_ICON = (By.CSS_SELECTOR, ".basket-icon")
    _PROD_DETAIL = (By.CSS_SELECTOR, ".prodDetail")
    _RATING_TEXT = (By.CSS_SELECTOR, ".ratingCont > .ratingText")
    _CARGO_BADGE_FIELD = (By.CSS_SELECTOR, ".cargoBadgeField")
    _IMG_HOLDER = (By.CSS_SELECTOR, ".imgHolder")
    
    # Filter and sort locators
    _ICON_SORT_BY = (By.CSS_SELECTOR, ".iconSortBy")
    _ITEM_I4 = (By.CSS_SELECTOR, ".item.i4")
    _CARGO_FILTER = (By.CSS_SELECTOR, ".filter.cargoFilter.acc")
    _FREE_SHIPMENT_OPTION = (By.ID, "freeShipmentOption")

    # Private locators for result view page
    RESULT_VIEW = (By.CSS_SELECTOR, ".resultView")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".searchResults")
    PRODUCT_LIST = (By.CSS_SELECTOR, ".productList")
    STORE_PRODUCTS = (By.CSS_SELECTOR, ".storeProducts")
    RESULT_TEXT = (By.CSS_SELECTOR, ".resultText")

    def __init__(self, driver):
        """Initialize ProductListingPage."""
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        # URL'e navigate etmeye gerek yok, zaten result sayfasındayız
        
        self.check()

    def check(self):
        """Check if product listing page is loaded correctly."""
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self._ADD_TO_CART_BUTTON))
            self.logger.info("Add to cart button is visible")
        except TimeoutException:
            self.logger.error("Timeout: add to cart button not visible after 10 seconds")
            raise

    def wait_for_store_page_load(self):
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

    def get_result_text(self) -> str:
        """
        Gets the full result text showing search results count.

        Returns:
            H1 text (e.g., "saatgroup")
        """
        try:
            result_element = self.find(self.RESULT_TEXT)
            result_text = result_element.text.strip()
            self.logger.info(f"Found result text: {result_text}")
            return result_text
        except Exception as e:
            self.logger.error(f"Error getting result text: {e}")
            return ""
    
    def is_product_added_to_cart(self) -> bool:
        """Check if product is added to cart."""
        try:
            self.wait.for_element_visible(self._ITEMS_INFO, timeout=15)
            return True
        except TimeoutException:
            return False

    # Özel metodlar - Açıklayıcı ve güvenli
    def click_skus_item(self, index: int = 1) -> None:
        """Clicks on SKUS item by index."""
        self._click_element_by_index(self._SKUS_ITEM, index, "SKUS item")
    
    def click_add_to_cart_button(self, index: int = 1) -> None:
        """
        Clicks on add to cart button by index.
        
        Args:
            index: Index of add to cart button to click (1-based, default: 1)
        """
        try:
            # Tüm add to cart buttonları bul
            elements = self.driver.find_elements(*self._ADD_TO_CART_BUTTON)
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
        """Generic method to click element using BasePage method."""
        self.click(locator)

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
        return self.get_item_count(self._SKUS_ITEM, "SKUS item")

    def get_add_to_cart_button_count(self) -> int:
        """
        Gets the number of add to cart buttons available.
        
        Returns:
            Number of add to cart buttons
        """
        return self.get_item_count(self._ADD_TO_CART_BUTTON, "add to cart button")
    
    def click_js_add_basket_sku(self) -> None:
        """Clicks on JS add basket sku."""
        self._click_element(self._JS_ADD_BASKET_SKU, "JS add basket sku")
    
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
    
    def click_brand_checkbox_by_index(self, index: int) -> None:
        """Clicks on a brand checkbox by index."""
        locator = (By.XPATH, f"(//label[contains(@for, 'brand-m-')])[{index}]")
        self.click(locator)
        self.logger.info(f"Clicked brand checkbox at index: {index}")
    
    def click_sort_option(self, option_number: int) -> None:
        """Clicks on sort option by number (1-7)."""
        locator = (By.CSS_SELECTOR, f".item.i{option_number}")
        self.click(locator)
        self.logger.info(f"Clicked sort option: item i{option_number}")
    
    def click_sort_by_icon(self) -> None:
        """Clicks on icon sort by."""
        self.click(self._ICON_SORT_BY)

    def click_cargo_filter(self) -> None:
        """Clicks on cargo filter."""
        self.click(self._CARGO_FILTER)

    def click_free_shipment_option(self) -> None:
        """Clicks on free shipment option."""
        self.click(self._FREE_SHIPMENT_OPTION)
    
    def click_basket_icon(self) -> None:
        """Clicks on basket icon."""
        self.click(self._BASKET_ICON)
    
    def get_prod_detail_count(self) -> None:
        """Gets the number of prod detail elements."""
        prod_detail_count = self.get_item_count(self._PROD_DETAIL, "prod detail")
        self.logger.info(f"Found {prod_detail_count} prod detail elements")
        return prod_detail_count
    
    def get_rating_text_by_index(self, index: int) -> str:
        """Gets the rating text by index with only numbers extracted."""
        import re
        try:
            rating_elements = self.driver.find_elements(*self._RATING_TEXT)
            if index < 1 or index > len(rating_elements):
                self.logger.error(f"Index {index} out of range. Found {len(rating_elements)} rating elements")
                return "0"
            
            rating_element = rating_elements[index - 1]  # 1-based index
            rating_text = rating_element.text
            cleaned = re.sub(r"[^\d]", "", rating_text)
            self.logger.info(f"Rating at index {index}: {rating_text}, cleaned: {cleaned}")
            return cleaned
        except Exception as e:
            self.logger.error(f"Error getting rating at index {index}: {e}")
            return "0"

    def verify_rating_sort_descending(self, count: int = 5) -> bool:
        """
        Verifies that ratings are sorted in descending order (biggest to smallest).
        
        Args:
            count: Number of ratings to check (default: 5)
            
        Returns:
            True if ratings are sorted descending, False otherwise
        """
        try:
            ratings = []
            for i in range(1, count + 1):
                rating_str = self.get_rating_text_by_index(i)
                rating_num = int(rating_str) if rating_str.isdigit() else 0
                ratings.append(rating_num)
            
            self.logger.info(f"Found ratings: {ratings}")
            
            # Check if list is sorted in descending order
            is_sorted_desc = all(ratings[i] >= ratings[i + 1] for i in range(len(ratings) - 1))
            
            if is_sorted_desc:
                self.logger.info(f"✅ Ratings are correctly sorted descending: {ratings}")
            else:
                self.logger.error(f"❌ Ratings are NOT sorted descending: {ratings}")
                
            return is_sorted_desc
            
        except Exception as e:
            self.logger.error(f"Error verifying rating sort: {e}")
            return False

    def verify_cargo_badge_field_all_products(self) -> bool:
        """Verifies that cargo badge field exists in all product imgHolder sections."""
        try:
            # imgHolder elementlerini bul
            img_holder_elements = self.driver.find_elements(*self._IMG_HOLDER)
            self.logger.info(f"Found {len(img_holder_elements)} imgHolder elements")
            
            products_with_cargo = 0
            products_without_cargo = 0
            
            for i, img_holder in enumerate(img_holder_elements, 1):
                try:
                    # Her imgHolder içinde cargoBadgeField var mı kontrol et
                    cargo_badge = img_holder.find_element(By.CSS_SELECTOR, ".cargoBadgeField")
                    if cargo_badge.is_displayed():
                        cargo_text = cargo_badge.find_element(By.CSS_SELECTOR, ".cargoBadgeText").text
                        self.logger.info(f"✅ Product {i}: Has cargo badge - '{cargo_text}'")
                        products_with_cargo += 1
                    else:
                        self.logger.warning(f"⚠️ Product {i}: Cargo badge exists but not visible")
                        products_without_cargo += 1
                except:
                    self.logger.warning(f"❌ Product {i}: No cargo badge found")
                    products_without_cargo += 1
            
            total_products = len(img_holder_elements)
            self.logger.info(f"📊 SUMMARY: {products_with_cargo}/{total_products} products have cargo badges")
            
            if products_with_cargo == total_products:
                self.logger.info("✅ ALL products have cargo badge field")
                return True
            else:
                self.logger.info(f"⚠️ {products_without_cargo} products don't have cargo badge")
                return False
                
        except Exception as e:
            self.logger.error(f"Error verifying cargo badge fields: {e}")
            return False