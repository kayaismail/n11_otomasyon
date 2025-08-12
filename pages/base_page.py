"""
Base Page Object Model class.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.wait_helper import WaitHelper
from selenium.common.exceptions import TimeoutException
import logging

class BasePage:
    """Base page object with common functionality."""
    
    def __init__(self, driver):
        """
        Initialize BasePage.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WaitHelper(driver)
    
    def navigate_to(self, url: str) -> None:
        """
        Generic navigation method for any URL.
        
        Args:
            url: URL to navigate to
        """
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        logging.info("Navigated to: {}".format(url))
    
    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.driver.current_url
    
    def wait_for_url_contains(self, text: str, timeout: int = 10) -> None:
        """Wait for URL to contain specific text."""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: text in driver.current_url
        )
        logging.info("URL contains '{}': {}".format(text, self.driver.current_url))

    def click_element(self, locator: tuple) -> None:
        """
        Clicks the element after waiting for it to be clickable.

        Args:
            locator: Tuple(By, value)
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logging.info("Element clicked successfully: {}".format(locator))
        except Exception as e:
            logging.error("An error occurred while clicking the element: {}".format(str(e)))
            logging.error("Failed at locator: {}".format(locator))
            raise AssertionError("Clicking the element failed at locator: {}".format(locator))

    def wait_for_element_to_be_visible(self, locator, timeout=10):
        """
        Wait for element to be visible
        :param locator: element locator
        :param timeout: int Maximum time you want to wait for the element

        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except Exception as e:
            raise Exception("Element not visible after {} seconds".format(timeout)) from e

    def wait_for_elements_to_be_visible(self, locator, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_any_elements_located(locator)
            )
            return elements
        except Exception as e:
            raise Exception("Elements not visible after {} seconds".format(timeout)) from e

    def wait_for_element_invisible(self, locator, timeout=20):
        """
        Wait for element to be invisible
        :param locator: locator of the element to find
        :param int timeout: Maximum time you want to wait for the element

        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            print("Element is now invisible.")
        except TimeoutException:
            print("Element is still visible after {} seconds.".format(timeout))