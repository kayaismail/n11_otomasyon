"""
Wait Helper module for explicit waits.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging

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
    
    def for_element_visible(self, locator: tuple, timeout: int = None) -> None:
        """
        Waits for the element to be visible.
        
        Args:
            locator: Tuple(By, value)
            timeout: Timeout in seconds (optional)
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        wait.until(EC.visibility_of_element_located(locator))
    
    def for_element_clickable(self, locator: tuple, timeout: int = None) -> None:
        """
        Waits for the element to be clickable.
        
        Args:
            locator: Tuple(By, value)
            timeout: Timeout in seconds (optional)
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        wait.until(EC.element_to_be_clickable(locator))
    
    def for_element_present(self, locator: tuple, timeout: int = None) -> None:
        """
        Waits for the element to be present in DOM.
        
        Args:
            locator: Tuple(By, value)
            timeout: Timeout in seconds (optional)
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        wait.until(EC.presence_of_element_located(locator))
    
    def for_text_present(self, locator: tuple, text: str, timeout: int = None) -> None:
        """
        Waits for specific text to be present in element.
        
        Args:
            locator: Tuple(By, value)
            text: Text to wait for
            timeout: Timeout in seconds (optional)
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        wait.until(EC.text_to_be_present_in_element(locator, text))
    
    def wait_for_page_load(self, timeout: int = None) -> None:
        """
        Waits for page to load completely.
        
        Args:
            timeout: Timeout in seconds (optional)
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")


