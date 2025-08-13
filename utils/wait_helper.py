"""
Wait Helper module for explicit waits.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
import logging
import time

class WaitHelper:
    """Helper class for explicit waits."""

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

    # ------------------- Senin mevcut metodların -------------------

    def for_element_visible(self, locator: tuple, timeout: int = None) -> None:
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def for_element_clickable(self, locator: tuple, timeout: int = None) -> None:
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def for_element_present(self, locator: tuple, timeout: int = None) -> None:
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.presence_of_element_located(locator)
        )

    def for_text_present(self, locator: tuple, text: str, timeout: int = None) -> None:
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    def wait_for_page_load(self, timeout: int = None) -> None:
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    # ------------------- Eklenmiş gelişmiş metodlar -------------------

    def for_invisible(self, locator: tuple, timeout: int = None) -> None:
        """Waits for element to become invisible."""
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def for_elements_count_at_least(self, locator: tuple, count: int, timeout: int = None):
        """Wait until at least `count` elements are present in DOM."""
        wait_timeout = timeout or self.timeout
        def _enough(drv):
            elements = drv.find_elements(*locator)
            return elements if len(elements) >= count else False
        return WebDriverWait(self.driver, wait_timeout).until(_enough)

    def for_url_contains(self, text: str, timeout: int = None) -> None:
        """Wait until URL contains given text."""
        wait_timeout = timeout or self.timeout
        WebDriverWait(self.driver, wait_timeout).until(
            EC.url_contains(text)
        )

    def for_element_stable(self, locator: tuple, still_ms: int = 300, timeout: int = None):
        """Wait until element is visually stable (no size/position changes)."""
        wait_timeout = timeout or self.timeout
        start_time = time.time()
        last_rect = None
        while time.time() - start_time < wait_timeout:
            el = self.for_element_visible(locator, timeout=1)
            el = self.driver.find_element(*locator)
            rect = (el.location['x'], el.location['y'], el.size['width'], el.size['height'])
            if rect == last_rect:
                time.sleep(still_ms / 1000)
                el2 = self.driver.find_element(*locator)
                rect2 = (el2.location['x'], el2.location['y'], el2.size['width'], el2.size['height'])
                if rect2 == rect:
                    return el2
            last_rect = rect
            time.sleep(0.05)
        raise TimeoutException(f"Element not stable within {wait_timeout}s: {locator}")

    def dom_idle(self, idle_ms: int = 400, timeout: int = None):
        """Wait until DOM stops changing for `idle_ms` milliseconds."""
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

    def safe_click(self, locator: tuple, timeout: int = None, scroll=True, js_fallback=True):
        """Click with retries, scroll into view, and optional JS fallback."""
        tries = 2
        last_exc = None
        for _ in range(tries):
            try:
                el = WebDriverWait(self.driver, timeout or self.timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                if scroll:
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                el.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                last_exc = e
        if js_fallback:
            el = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", el)
            return
        raise last_exc or TimeoutException(f"safe_click failed: {locator}")
