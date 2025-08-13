"""
Base Page Object Model class.
"""
import os
import time
import logging
from typing import List, Tuple, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from utils.wait_helper import WaitHelper
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)

DEFAULT_TIMEOUT = 10

class BasePage:
    """
    BasePage: All page objects inherit from this class.
    Handles common Selenium actions with logging and wait mechanisms.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        self.wait = WaitHelper(driver, timeout=DEFAULT_TIMEOUT)

    # ------------------
    # Navigation
    # ------------------
    def navigate_to(self, url: str) -> None:
        """Navigate to URL and wait for page load."""
        self.driver.get(url)
        self.wait.wait_for_page_load()
        self.logger.info(f"Navigated to: {url}")

    # ------------------
    # Find Methods
    # ------------------
    def find(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT):
        """Find single element after ensuring it's visible."""
        self.wait.for_element_visible(locator, timeout)
        return self.driver.find_element(*locator)

    def find_all(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> List:
        """Find all visible elements."""
        self.wait.for_element_visible(locator, timeout)
        return self.driver.find_elements(*locator)

    # ------------------
    # Click / Type
    # ------------------
    def click(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT):
        """Wait until clickable, then click."""
        try:
            self.wait.for_element_clickable(locator, timeout)
            self.driver.find_element(*locator).click()
            self.logger.info(f"Clicked on: {locator}")
        except (StaleElementReferenceException, ElementClickInterceptedException):
            self.logger.warning(f"Retry click due to stale/intercepted: {locator}")
            self.wait.for_element_clickable(locator, timeout)
            self.driver.find_element(*locator).click()

    def click_nth(self, locator: Tuple[str, str], index: int, timeout: int = DEFAULT_TIMEOUT):
        """Click Nth element from a list (1-based index)."""
        elements = self.find_all(locator, timeout)
        if index < 1 or index > len(elements):
            raise IndexError(f"Index {index} out of range. Found {len(elements)} elements.")
        elements[index - 1].click()
        self.logger.info(f"Clicked {index}th element from: {locator}")

    def type(self, locator: Tuple[str, str], value: str, timeout: int = DEFAULT_TIMEOUT, clear: bool = True):
        """Wait until visible, then type text."""
        self.wait.for_element_visible(locator, timeout)
        element = self.driver.find_element(*locator)
        if clear:
            element.clear()
        element.send_keys(value)
        self.logger.info(f"Typed '{value}' into: {locator}")

    def js_click(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT):
        """Click using JavaScript."""
        self.wait.for_element_visible(locator, timeout)
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", element)
        self.logger.info(f"JS clicked: {locator}")

    # ------------------
    # Scroll
    # ------------------
    def scroll_into_view(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT):
        """Scroll element into view."""
        self.wait.for_element_visible(locator, timeout)
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info(f"Scrolled into view: {locator}")

    # ------------------
    # Screenshot
    # ------------------
    def screenshot_on_fail(self, file_name: Optional[str] = None):
        """Take screenshot and save to screenshots folder."""
        if not file_name:
            file_name = f"screenshot_{int(time.time())}.png"
        path = os.path.join("screenshots", file_name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.driver.save_screenshot(path)
        self.logger.info(f"Screenshot saved: {path}")
