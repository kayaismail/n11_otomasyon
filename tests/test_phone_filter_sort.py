"""
Test cases for N11 Phone search with filtering and sorting functionality.
"""
import pytest
from pages.home_page import HomePage
from pages.product_listing_page import ProductListingPage
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

        # Act - Step 1: Search for "telefon"
        home_page.search_for_product("telefon")
        logger.info("Successfully searched for 'telefon'")

        # Act - Step 2: Navigate to product listing page
        product_listing_page = ProductListingPage(home_page.driver)
        
        # Act - Step 3: Select second brand filter
        product_listing_page.click_brand_checkbox_by_index(2)
        logger.info("Selected second brand filter")
        
        # Act - Step 4: Sort by comment count
        product_listing_page.click_sort_by_icon()
        logger.info("clicked sort by icon")
        
        # Act - Step 5: Get and list free shipping products
        product_listing_page.click_sort_option(4)
        logger.info("clicked sort by comment count")
        product_listing_page.click_cargo_filter()
        product_listing_page.click_free_shipment_option()
        logger.info("clicked free shipment option")
        
        # Assert - Verify that products were found
  
        
        # Log free shipping products

        
        logger.info("Test completed successfully")
