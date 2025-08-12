"""
Pytest configuration and fixtures.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@pytest.fixture(scope="function")
def driver():
    """
    WebDriver fixture for each test.
    
    Yields:
        WebDriver: Chrome WebDriver instance
    """
    # Chrome options for better stability
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    # Performance preferences
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 2  # Disable images for faster loading
    })
    
    # Create service and driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set timeouts for better stability
    driver.set_page_load_timeout(30)  # Page load timeout
    driver.set_script_timeout(30)     # Script timeout
    
    # DO NOT use implicit wait - it can cause issues with explicit waits
    # driver.implicitly_wait(10)  # KALDIR!
    
    logging.info("WebDriver initialized with optimized settings")
    
    yield driver
    
    # Cleanup
    try:
        driver.quit()
        logging.info("WebDriver closed successfully")
    except Exception as e:
        logging.warning(f"Error closing WebDriver: {e}")

def handle_cookie_popup(driver):
    """
    Handles cookie consent by setting localStorage consent data.
    
    Args:
        driver: WebDriver instance
    """
    try:
        # Set localStorage consent data
        consent_data = {
            "updatedAt": 1754951633783,
            "categories": {
                "essential": True,
                "functional": True,
                "marketing": True,
                "other": True
            },
            "browserData": {
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                "pageLoad": 1753.2000000178814,
                "language": "tr",
                "networkType": "4g",
                "screen": {
                    "devicePixelRatio": 2,
                    "height": 1080,
                    "width": 1920
                },
                "uuid": "58c47cce-cfae-48e0-8020-a47b780a521c"
            }
        }
        
        # Set the consent data in localStorage
        driver.execute_script("localStorage.setItem('efl-saved-consent', JSON.stringify(arguments[0]));", consent_data)
        
        logging.info("Cookie consent data set in localStorage")
        
        # Refresh page to apply the consent
        driver.refresh()
        
        # Wait for page to load after refresh
        from utils.wait_helper import WaitHelper
        wait_helper = WaitHelper(driver)
        wait_helper.wait_for_page_load(timeout=15)
        wait_helper.wait_for_network_idle(timeout=10)
        
        logging.info("Page refreshed and loaded with cookie consent")
        
    except Exception as e:
        logging.warning("Could not set cookie consent: {}".format(e))

@pytest.fixture
def stores_page(driver):
    """
    StoresPage fixture.
    
    Args:
        driver: WebDriver fixture
        
    Returns:
        StoresPage: Initialized stores page object
    """
    from pages.stores_page import StoresPage
    
    # Navigate to stores page
    stores_page = StoresPage(driver)
    
    # Handle cookie popup if present
    handle_cookie_popup(driver)
    
    return stores_page

# Pytest hooks for HTML reporting
def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line("markers", "smoke: smoke tests")
    config.addinivalue_line("markers", "regression: regression tests")
    config.addinivalue_line("markers", "slow: slow running tests")

def pytest_html_report_title(report):
    """Customize HTML report title."""
    report.title = "N11 Automation Test Report"

def pytest_html_results_summary(prefix, summary, postfix):
    """Add custom summary to HTML report."""
    prefix.extend([
        f"<p><strong>Test Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
        f"<p><strong>Project:</strong> N11 E-commerce Automation</p>"
    ])
