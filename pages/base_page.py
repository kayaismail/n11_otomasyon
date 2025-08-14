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
        """
        Find single element after ensuring it's visible.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement: The found element
        """
        self.wait.for_element_visible(locator, timeout)
        return self.driver.find_element(*locator)

    def find_all(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> List:
        """
        Find all visible elements.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Maximum wait time in seconds
            
        Returns:
            List[WebElement]: List of found elements
        """
        self.wait.for_element_visible(locator, timeout)
        return self.driver.find_elements(*locator)

    # ------------------
    # Click / Type
    # ------------------
    def click(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Wait until clickable, then click with retry mechanism.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Maximum wait time in seconds
        """
        try:
            self.wait.for_element_clickable(locator, timeout)
            self.driver.find_element(*locator).click()
            self.logger.info(f"Clicked on: {locator}")
        except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            self.logger.warning(f"Retry click due to {type(e).__name__}: {locator}")
            self.wait.for_element_clickable(locator, timeout)
            self.driver.find_element(*locator).click()
            self.logger.info(f"Successfully clicked on retry: {locator}")

    def click_nth(self, locator: Tuple[str, str], index: int, timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Click Nth element from a list (1-based index).
        
        Args:
            locator: Tuple of (By, value) for element location
            index: Element index (1-based)
            timeout: Maximum wait time in seconds
            
        Raises:
            IndexError: If index is out of range
        """
        elements = self.find_all(locator, timeout)
        if index < 1 or index > len(elements):
            raise IndexError(f"Index {index} out of range. Found {len(elements)} elements.")
        elements[index - 1].click()
        self.logger.info(f"Clicked {index}th element from: {locator}")

    def type(self, locator: Tuple[str, str], value: str, timeout: int = DEFAULT_TIMEOUT, clear: bool = True) -> None:
        """
        Wait until visible, then type text.
        
        Args:
            locator: Tuple of (By, value) for element location
            value: Text to type
            timeout: Maximum wait time in seconds
            clear: Whether to clear field before typing
        """
        self.wait.for_element_visible(locator, timeout)
        element = self.driver.find_element(*locator)
        if clear:
            element.clear()
        element.send_keys(value)
        self.logger.info(f"Typed '{value}' into: {locator}")

    def js_click(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Click using JavaScript (bypasses DOM click issues).
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Maximum wait time in seconds
        """
        self.wait.for_element_visible(locator, timeout)
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", element)
        self.logger.info(f"JS clicked: {locator}")

    # ------------------
    # Scroll
    # ------------------
    def scroll_into_view(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Scroll element into view.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Maximum wait time in seconds
        """
        self.wait.for_element_visible(locator, timeout)
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info(f"Scrolled into view: {locator}")

    # ------------------
    # Screenshot
    # ------------------
    def screenshot_on_fail(self, file_name: Optional[str] = None) -> str:
        """
        Take screenshot and save to screenshots folder.
        
        Args:
            file_name: Optional filename, auto-generated if None
            
        Returns:
            str: Path to saved screenshot file
        """
        if not file_name:
            file_name = f"screenshot_{int(time.time())}.png"
        path = os.path.join("screenshots", file_name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.driver.save_screenshot(path)
        self.logger.info(f"Screenshot saved: {path}")
        return path

    # ------------------
    # Wait Methods
    # ------------------
    def wait_visible(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Wait for element to be visible.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Maximum wait time in seconds
        """
        self.wait.for_element_visible(locator, timeout)
        self.logger.info(f"Element is visible: {locator}")

    def wait_clickable(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Wait for element to be clickable.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Maximum wait time in seconds
        """
        self.wait.for_element_clickable(locator, timeout)
        self.logger.info(f"Element is clickable: {locator}")

    # ------------------
    # Utility Methods
    # ------------------
    def get_text(self, locator: Tuple[str, str], timeout: int = DEFAULT_TIMEOUT) -> str:
        """
        Get text from element.
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Maximum wait time in seconds
            
        Returns:
            str: Element text content
        """
        element = self.find(locator, timeout)
        text = element.text.strip()
        self.logger.info(f"Got text '{text}' from: {locator}")
        return text

    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is present in DOM (without waiting).
        
        Args:
            locator: Tuple of (By, value) for element location
            
        Returns:
            bool: True if element exists, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is visible (without waiting).
        
        Args:
            locator: Tuple of (By, value) for element location
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except:
            return False
