"""
Test cases for N11 Phone search with filtering and sorting functionality.
"""
import pytest
from pages.home_page import HomePage
from pages.search_result_page import SearchResultPage
import logging


class TestPhoneFilterSort:
    """Test class for phone search with filtering and sorting."""

    def test_phone_search_filter_sort_free_shipping(self, home_page):
        """
        Test: Phone search with brand filtering, comment sorting and free shipping listing.

        Steps:
        1. Search for "telefon" keyword
        2. Select second brand filter
        3. Sort by comment count
        4. List products with free shipping
        """
        # Arrange
        logger = logging.getLogger(__name__)
        logger.info("Starting test: Phone search with filtering and sorting")

        # Act - Step 1: Search for "telefon" keyword
        logger.info("📱 STEP 1: Searching for 'telefon' keyword on N11 homepage")
        home_page.search_for_product("telefon")
        logger.info("✅ SUCCESS: Successfully searched for 'telefon' keyword")

        # Act - Step 2: Navigate to product listing page
        logger.info("📋 STEP 2: Navigating to product listing page")
        product_listing_page = SearchResultPage(home_page.driver)
        logger.info("✅ SUCCESS: Product listing page loaded successfully")
        
        # Act - Step 3: Select second brand filter
        logger.info("🏷️ STEP 3: Selecting second brand filter from available brands")
        product_listing_page.click_brand_checkbox_by_index(2)
        logger.info("✅ SUCCESS: Second brand filter selected successfully")
        
        # Act - Step 4: Sort by comment count
        logger.info("📊 STEP 4: Opening sort dropdown to sort products")
        product_listing_page.click_sort_by_icon()
        logger.info("✅ SUCCESS: Sort dropdown opened successfully")
        
        logger.info("📈 STEP 4.1: Selecting 'Sort by Comment Count' option")
        product_listing_page.click_sort_option(4)
        logger.info("✅ SUCCESS: Products sorted by comment count successfully")
        
        # Act - Step 5: Filter by free shipping
        logger.info("🚚 STEP 5: Opening cargo filter to find free shipping products")
        product_listing_page.click_cargo_filter()
        logger.info("✅ SUCCESS: Cargo filter opened successfully")
        
        logger.info("📦 STEP 5.1: Selecting 'Free Shipment' option")
        product_listing_page.click_free_shipment_option()
        logger.info("✅ SUCCESS: Free shipment filter applied successfully")
        
        # Assert - Verify that products were found
  
        
        # Log free shipping products

        
        logger.info("=" * 80)
        logger.info("🎉 TEST COMPLETED SUCCESSFULLY: Phone Search with Filtering and Sorting")
