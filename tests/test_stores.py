"""
Test cases for N11 Stores functionality.
"""
import pytest
from pages.stores_page import StoresPage
import logging
from selenium.common.exceptions import TimeoutException

class TestStores:
    """Test class for N11 stores functionality."""

    def test_filter_and_click_random_store(self, stores_page):
        """
        Test case is: Filter stores by letter 'S' and click on a random store.

        Steps:
        1. Filter stores by letter 'S'
        2. Click on a random store
        """
        # Arrange
        logger = logging.getLogger(__name__)

        logger.info("🚀 STARTING TEST: Filter and Click Random Store")

        # Act - Step 1: Filter stores by letter 'S'
        logger.info("🔤 STEP 1: Filtering stores by letter 'S' from alphabet filter")
        stores_page.click_letter("S")
        logger.info("✅ SUCCESS: Successfully filtered stores by letter 'S'")

        # Assert - Verify stores are available after filtering
        logger.info("🔍 STEP 2: Verifying that stores are available after filtering")
        store_count = stores_page.get_store_count()
        assert store_count > 0, "Should find stores after filtering by 'S'"
        logger.info(f"✅ SUCCESS: Found {store_count} stores after filtering by 'S'")

        # Act - Step 3: Get random index and click
        logger.info("🎲 STEP 3: Generating random store index for selection")
        random_index = stores_page.get_random_store_index()
        assert 1 <= random_index <= store_count, "Random index should be within valid range"
        logger.info(f"✅ SUCCESS: Generated random index: {random_index} (valid range: 1-{store_count})")

        # Act - Step 4: Click on the random store and get result view page
        logger.info(f"🏪 STEP 4: Clicking on store at index {random_index}")
        result_view_page = stores_page.click_store_by_index(random_index)
        logger.info(f"✅ SUCCESS: Successfully clicked on store at index: {random_index}")

        # Act - Step 5: Verify result view page
        logger.info("📋 STEP 5: Waiting for store page to load completely")
        result_view_page.wait_for_store_page_load()
        logger.info("✅ SUCCESS: Store page loaded successfully")
        
        # Verify result view elements are present
        logger.info("🔍 STEP 6: Verifying that result view elements are present and visible")
        is_result_visible = result_view_page.verify_result_view_element()
        assert is_result_visible, "Result view elements should be visible after clicking store"
        logger.info("✅ SUCCESS: Result view elements are present and visible")

        # Assert - Test completed successfully

        logger.info("🎉 TEST COMPLETED SUCCESSFULLY: Filter and Click Random Store")
