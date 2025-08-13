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
import time
from simple_report import SimpleReporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Global reporter instance (reset at session start)
reporter = None

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
        "profile.default_content_settings.popups": 0
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
        
        logging.info("Page refreshed and loaded with cookie consent")
        
    except Exception as e:
        logging.warning("Could not set cookie consent: {}".format(e))

@pytest.fixture
def home_page(driver):
    """
    HomePage fixture.
    
    Args:
        driver: WebDriver fixture
        
    Returns:
        HomePage: Initialized home page object
    """
    from pages.home_page import HomePage
    
    # Navigate to home page
    home_page = HomePage(driver)
    
    # Handle cookie popup if present
    handle_cookie_popup(driver)
    
    return home_page

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

# Pytest hooks for simple reporting
def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line("markers", "smoke: smoke tests")
    config.addinivalue_line("markers", "regression: regression tests")
    config.addinivalue_line("markers", "slow: slow running tests")

def pytest_sessionstart(session):
    """Initialize reporter at session start."""
    global reporter
    # Eğer reporter zaten varsa eski testleri koru, yoksa yeni oluştur
    if reporter is None:
        reporter = SimpleReporter()
        logging.info("🆕 Simple reporter initialized")
    else:
        logging.info("📄 Existing reporter found, keeping previous test results")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for simple report."""
    outcome = yield
    report = outcome.get_result()
    
    # Only capture call phase results (actual test execution)
    if report.when == "call":
        test_name = item.name
        status = "PASS" if report.passed else "FAIL"
        duration = report.duration if hasattr(report, 'duration') else 0
        error_msg = ""
        logs = ""
        
        if report.failed and hasattr(report, 'longrepr'):
            # Extract error message
            try:
                error_msg = str(report.longrepr).split('\n')[-2] if report.longrepr else ""
            except:
                error_msg = "Test failed"
        
        # Capture logs from report sections (captured stdout/stderr)
        try:
            if hasattr(report, 'sections') and report.sections:
                log_sections = []
                for section_name, section_content in report.sections:
                    if any(keyword in section_name.lower() for keyword in ['log', 'stderr', 'stdout']):
                        log_sections.append(f"--- {section_name} ---\n{section_content}")
                if log_sections:
                    logs = "\n\n".join(log_sections)
                else:
                    logs = "Log sections bulunamadı"
            else:
                logs = "Report sections mevcut değil"
        except Exception as e:
            logs = f"Log bilgisi alınamadı: {str(e)}"
        
        # Add to reporter
        reporter.add_result(test_name, status, duration, error_msg, logs)
        logging.info(f"📝 Captured test result: {test_name} = {status}")

def pytest_sessionfinish(session, exitstatus):
    """Generate simple HTML report when session finishes."""
    try:
        output_path = reporter.generate_html("reports/live_report.html")
        print(f"\n🎉 Live HTML Report: file://{output_path}")
    except Exception as e:
        logging.error(f"Failed to generate simple report: {e}")