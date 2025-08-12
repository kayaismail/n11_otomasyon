"""
Test cases for N11 Stores functionality.
"""
import pytest
from pages.stores_page import StoresPage
import logging

class TestStores:
    """Test class for N11 stores functionality."""

    def test_filter_and_click_random_store(self, stores_page):
        """
        Test: Filter stores by letter 'S' and click on a random store.

        Steps:
        1. Filter stores by letter 'S'
        2. Click on a random store
        """
        # Arrange
        logging.info("Starting test: Filter and click random store")

        # Act - Step 1: Filter stores by letter 'S'
        stores_page.click_letter("S")
        logging.info("Successfully filtered stores by letter 'S'")

        # Assert - Verify stores are available after filtering
        store_count = stores_page.get_store_count()
        assert store_count > 0, "Should find stores after filtering by 'S'"
        logging.info("Found {} stores after filtering".format(store_count))

        # Act - Step 2: Get random index and click
        random_index = stores_page.get_random_store_index()
        assert 1 <= random_index <= store_count, "Random index should be within valid range"
        logging.info("Generated random index: {} (valid range: 1-{})".format(random_index, store_count))

        # Act - Step 3: Click on the random store and get result view page
        result_view_page = stores_page.click_store_by_index(random_index)

        # Act - Step 4: Verify result view page
        result_view_page.wait_for_store_page_load()
        result_view_page.verify_result_view_element()

        # Assert - Test completed successfully
        logging.info("Successfully clicked on store at index: {}".format(random_index))
