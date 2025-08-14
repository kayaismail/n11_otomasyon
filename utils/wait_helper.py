"""
Wait Helper module for explicit waits.
"""
import logging
from typing import List, Optional, Tuple
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException

class WaitHelper:
    """
    Helper class for explicit waits with comprehensive waiting strategies.
    
    Provides various wait conditions and utility methods for robust web automation.
    """

    def __init__(self, driver, timeout: int = 10):
        """
        Initialize WaitHelper.

        Args:
            driver: WebDriver instance
            timeout: Default timeout in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.logger = logging.getLogger(__name__)

    # ------------------- Senin mevcut metodların -------------------

    def for_element_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        """
        Wait for element to be visible.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Optional timeout override
        """
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.visibility_of_element_located(locator)
        )
        self.logger.debug(f"Element visible: {locator}")

    def for_element_clickable(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        """
        Wait for element to be clickable.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Optional timeout override
        """
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.element_to_be_clickable(locator)
        )
        self.logger.debug(f"Element clickable: {locator}")

    def for_element_present(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        """
        Wait for element to be present in DOM.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Optional timeout override
        """
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.presence_of_element_located(locator)
        )
        self.logger.debug(f"Element present: {locator}")

    def for_text_present(self, locator: Tuple[str, str], text: str, timeout: Optional[int] = None) -> None:
        """
        Wait for specific text to be present in element.
        
        Args:
            locator: Tuple of (By, value) for element location
            text: Text to wait for
            timeout: Optional timeout override
        """
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
        self.logger.debug(f"Text '{text}' present in: {locator}")

    def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """
        Wait for page to completely load.
        
        Args:
            timeout: Optional timeout override
        """
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        self.logger.debug("Page loaded completely")

    # ------------------- Eklenmiş gelişmiş metodlar -------------------

    def for_invisible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        """
        Wait for element to become invisible.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Optional timeout override
        """
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.invisibility_of_element_located(locator)
        )
        self.logger.debug(f"Element invisible: {locator}")

    def for_elements_count_at_least(self, locator: Tuple[str, str], count: int, timeout: Optional[int] = None) -> List[WebElement]:
        """
        Wait until at least `count` elements are present in DOM.
        
        Args:
            locator: Tuple of (By, value) for element location
            count: Minimum number of elements required
            timeout: Optional timeout override
            
        Returns:
            List[WebElement]: List of found elements
        """
        wait_timeout = timeout or self.timeout
        def _enough(drv):
            elements = drv.find_elements(*locator)
            return elements if len(elements) >= count else False
        elements = WebDriverWait(self.driver, wait_timeout).until(_enough)
        self.logger.debug(f"Found {len(elements)} elements (needed >= {count}): {locator}")
        return elements

    def for_url_contains(self, text: str, timeout: Optional[int] = None) -> None:
        """
        Wait until URL contains given text.
        
        Args:
            text: Text that URL should contain
            timeout: Optional timeout override
        """
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.url_contains(text)
        )
        self.logger.debug(f"URL contains '{text}'")

    def for_element_stable(self, locator: Tuple[str, str], still_ms: int = 300, timeout: Optional[int] = None) -> WebElement:
        """
        Wait until element is visually stable (no size/position changes).
        
        Args:
            locator: Tuple of (By, value) for element location
            still_ms: Milliseconds element must remain stable
            timeout: Optional timeout override
            
        Returns:
            WebElement: The stable element
            
        Raises:
            TimeoutException: If element doesn't stabilize within timeout
        """
        wait_timeout = timeout or self.timeout
        
        def _is_stable(driver):
            try:
                self.for_element_visible(locator, timeout=1)
                el = driver.find_element(*locator)
                
                # Take initial measurement
                initial_rect = (el.location['x'], el.location['y'], el.size['width'], el.size['height'])
                
                # Wait using WebDriverWait instead of time.sleep
                WebDriverWait(driver, still_ms / 1000).until(
                    lambda d: d.find_element(*locator).is_displayed()
                )
                
                # Take second measurement
                el2 = driver.find_element(*locator)
                final_rect = (el2.location['x'], el2.location['y'], el2.size['width'], el2.size['height'])
                
                if initial_rect == final_rect:
                    return el2
                return False
            except:
                return False
        
        element = WebDriverWait(self.driver, wait_timeout).until(_is_stable)
        self.logger.debug(f"Element stable: {locator}")
        return element

    def dom_idle(self, idle_ms: int = 400, timeout: Optional[int] = None) -> None:
        """
        Wait until DOM stops changing for `idle_ms` milliseconds.
        
        Args:
            idle_ms: Milliseconds DOM must remain idle
            timeout: Optional timeout override
        """
        script = """
        const cb = arguments[arguments.length - 1];
        const idleMs = arguments[0];
        let timer = null;
        const obs = new MutationObserver(() => {
            clearTimeout(timer);
            timer = setTimeout(done, idleMs);
        });
        function done(){ obs.disconnect(); cb(true); }
        obs.observe(document, {subtree:true, childList:true, attributes:true});
        timer = setTimeout(done, idleMs);
        """
        self.driver.set_script_timeout(timeout or self.timeout)
        self.driver.execute_async_script(script, idle_ms)
        self.logger.debug(f"DOM idle for {idle_ms}ms")

    def safe_click(self, locator: Tuple[str, str], timeout: Optional[int] = None, scroll: bool = True, js_fallback: bool = True) -> None:
        """
        Click with retries, scroll into view, and optional JS fallback.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Optional timeout override
            scroll: Whether to scroll element into view
            js_fallback: Whether to use JavaScript click as fallback
            
        Raises:
            TimeoutException: If all click attempts fail
        """
        tries = 2
        last_exc = None
        for attempt in range(tries):
            try:
                el = WebDriverWait(self.driver, timeout or self.timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                if scroll:
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                el.click()
                self.logger.debug(f"Safe click successful on attempt {attempt + 1}: {locator}")
                return
            except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                last_exc = e
                self.logger.warning(f"Click attempt {attempt + 1} failed: {type(e).__name__}")
        
        if js_fallback:
            try:
                el = self.driver.find_element(*locator)
                self.driver.execute_script("arguments[0].click();", el)
                self.logger.debug(f"JS fallback click successful: {locator}")
                return
            except Exception as e:
                self.logger.error(f"JS fallback also failed: {e}")
        
        raise last_exc or TimeoutException(f"safe_click failed after all attempts: {locator}")
