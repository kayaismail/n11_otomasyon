"""
Test cases for N11 Search functionality.
"""
import pytest
from pages.home_page import HomePage
from pages.product_listing_page import ProductListingPage
import logging

class TestSearch:
    """Test class for N11 search functionality."""

    def test_search_and_add_to_cart(self, home_page):
        """
        Test: Search for a product and add to cart.

        Steps:
        1. Search for a product
        2. Add product to cart
        """
        # Arrange
        logger = logging.getLogger(__name__)
        logger.info("Starting test: Search and add to cart")

        # Act - Step 1: Search for product
        home_page.search_for_product("iphone")
        logger.info("Successfully searched for 'iphone'")

        # Act - Step 2: Navigate to product listing page
        product_listing_page = ProductListingPage(home_page.driver)
        
        # Act - Step 3: Add product to cart
        product_listing_page.click_add_to_cart_button()
        logger.info("Successfully added product to cart")
        
        # Act - Step 4: Select first SKUS item (daha güvenli)
        product_listing_page.click_skus_item(1)
        logger.info("Clicked first SKUS item")
        
        # Act - Step 5: Get SKUS items count for verification
        skus_items_count: int = product_listing_page.get_skus_items_count()
        product_listing_page.click_skus_item(skus_items_count)
        logger.info(f"Found {skus_items_count} SKUS items")
        
        # Act - Step 6: Click JS add basket sku
        product_listing_page.click_js_add_basket_sku()
        logger.info("Clicked JS add basket sku")
        
        # Assert - Verify product was added to cart
        is_added = product_listing_page.is_product_added_to_cart()
        assert is_added, "Product should be added to cart"
        logger.info("Test completed successfully")

        add_to_cart_button_count: int = product_listing_page.get_add_to_cart_button_count()
        logger.info(f"Found {add_to_cart_button_count} add to cart buttons")

         # Act - Step 3: Add product to cart
        product_listing_page.click_add_to_cart_button(add_to_cart_button_count)
        logger.info("Successfully added product to cart")
        
        # Act - Step 4: Select first SKUS item (daha güvenli)
        product_listing_page.click_skus_item(1)
        logger.info("Clicked first SKUS item")
        
        # Act - Step 5: Get SKUS items count for verification
        skus_items_count: int = product_listing_page.get_skus_items_count()
        product_listing_page.click_skus_item(skus_items_count)
        logger.info(f"Found {skus_items_count} SKUS items")
        
        # Act - Step 6: Click JS add basket sku
        product_listing_page.click_js_add_basket_sku()
        logger.info("Clicked JS add basket sku")
        
        # Assert - Verify product was added to cart
        is_added = product_listing_page.is_product_added_to_cart()
        assert is_added, "Product should be added to cart"
        logger.info("Test completed successfully") 
        