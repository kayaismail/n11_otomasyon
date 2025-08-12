"""
Test cases for N11 Search functionality.
"""
import pytest
from pages.home_page import HomePage
from pages.product_listing_page import ProductListingPage
import logging

class TestSearch:
    """Test class for N11 search functionality."""
    
    def _add_product_to_cart_workflow(self, product_listing_page, cart_button_index: int = 1):
        """
        Helper method for add to cart workflow.
        
        Args:
            product_listing_page: ProductListingPage instance
            cart_button_index: Index of cart button to click
        """
        logger = logging.getLogger(__name__)
        
        # Add product to cart
        product_listing_page.click_add_to_cart_button(cart_button_index)
        
        logger.info(f"Successfully added product to cart (button index: {cart_button_index})")
        
        if product_listing_page.has_skus_items():
            # Select first SKUS item
            product_listing_page.click_skus_item(1)
            logger.info("Clicked first SKUS item")
        
            # Select last SKUS item
            skus_items_count = product_listing_page.get_skus_items_count()
            product_listing_page.click_skus_item(skus_items_count)
            logger.info(f"Clicked last SKUS item (index: {skus_items_count})")
        
            # Click JS add basket sku
            product_listing_page.click_js_add_basket_sku()
            logger.info("Clicked JS add basket sku")
        # Verify product was added to cart
        is_added = product_listing_page.is_product_added_to_cart()
        assert is_added, "Product should be added to cart"
        logger.info("Product successfully added to cart")

    def test_search_and_add_to_cart(self, home_page):
        """
        Test: Search for a product and add to cart.

        Steps:
        1. Search for a product
        2. Add multiple products to cart using different cart buttons
        """
        # Arrange
        logger = logging.getLogger(__name__)
        logger.info("Starting test: Search and add to cart")

        # Act - Step 1: Search for product
        home_page.search_for_product("iphone")
        logger.info("Successfully searched for 'iphone'")

        # Act - Step 2: Navigate to product listing page
        product_listing_page = ProductListingPage(home_page.driver)
        
        # Act - Step 3: Add first product to cart
        self._add_product_to_cart_workflow(product_listing_page, cart_button_index=1)
        
        # Act - Step 4: Check how many cart buttons are available
        add_to_cart_button_count = product_listing_page.get_add_to_cart_button_count()
        logger.info(f"Found {add_to_cart_button_count} add to cart buttons")
        
        # Act - Step 5: Add last product to cart (if more than 1 button exists)
        if add_to_cart_button_count > 1:
            self._add_product_to_cart_workflow(product_listing_page, cart_button_index=add_to_cart_button_count)
        else:
            logger.info("Only one cart button found, skipping second addition")
        
        logger.info("Test completed successfully")
