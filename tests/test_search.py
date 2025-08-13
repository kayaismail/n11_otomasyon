"""
Test cases for N11 Search functionality.
"""
import pytest
from pages.home_page import HomePage
from pages.search_result_page import SearchResultPage
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
        logger.info(f"🛒 Adding product to cart using button index: {cart_button_index}")
        product_listing_page.click_add_to_cart_button(cart_button_index)
        logger.info(f"✅ SUCCESS: Successfully added product to cart (button index: {cart_button_index})")
        
        if product_listing_page.has_skus_items():
            logger.info("📦 Product has SKU variants - selecting variants")
            
            # Select first SKUS item
            logger.info("🏷️ Selecting first SKU variant")
            product_listing_page.click_skus_item(1)
            logger.info("✅ SUCCESS: First SKU variant selected")
        
            # Select last SKUS item
            skus_items_count = product_listing_page.get_skus_items_count()
            logger.info(f"🏷️ Selecting last SKU variant (index: {skus_items_count})")
            product_listing_page.click_skus_item(skus_items_count)
            logger.info(f"✅ SUCCESS: Last SKU variant selected (index: {skus_items_count})")
        
            # Click JS add basket sku
            logger.info("🛒 Clicking 'Add to Basket' button for SKU selection")
            product_listing_page.click_js_add_basket_sku()
            logger.info("✅ SUCCESS: 'Add to Basket' button clicked for SKU")
        else:
            logger.info("📦 Product has no SKU variants - direct add to cart")
        
        # Verify product was added to cart
        logger.info("🔍 Verifying that product was successfully added to cart")
        is_added = product_listing_page.is_product_added_to_cart()
        assert is_added, "Product should be added to cart"
        logger.info("✅ SUCCESS: Product successfully added to cart")

    def test_search_and_add_to_cart(self, home_page):
        """
        Test: Search for a product and add to cart.

        Steps:
        1. Search for a product
        2. Add multiple products to cart using different cart buttons
        """
        # Arrange
        logger = logging.getLogger(__name__)
        logger.info("🚀 STARTING TEST: Search and Add to Cart")


        # Act - Step 1: Search for product
        logger.info("🔍 STEP 1: Searching for 'iphone' product on N11 homepage")
        home_page.search_for_product("iphone")
        logger.info("✅ SUCCESS: Successfully searched for 'iphone' product")

        # Act - Step 2: Navigate to product listing page
        logger.info("📋 STEP 2: Navigating to product listing page")
        product_listing_page = SearchResultPage(home_page.driver)
        logger.info("✅ SUCCESS: Product listing page loaded successfully")
        
        # Act - Step 3: Add first product to cart
        logger.info("🛒 STEP 3: Adding first product to cart")
        self._add_product_to_cart_workflow(product_listing_page, cart_button_index=1)
        
        # Act - Step 4: Check how many cart buttons are available
        logger.info("🔢 STEP 4: Checking total number of available cart buttons")
        add_to_cart_button_count = product_listing_page.get_add_to_cart_button_count()
        logger.info(f"✅ SUCCESS: Found {add_to_cart_button_count} add to cart buttons")
        
        # Act - Step 5: Add last product to cart (if more than 1 button exists)
        if add_to_cart_button_count > 1:
            logger.info(f"🛒 STEP 5: Adding last product to cart (button index: {add_to_cart_button_count})")
            self._add_product_to_cart_workflow(product_listing_page, cart_button_index=add_to_cart_button_count)
            logger.info("✅ SUCCESS: Last product added to cart successfully")
        else:
            logger.info("⚠️ STEP 5: Only one cart button found, skipping second addition")

        # Act - Step 6: Click basket icon
        logger.info("🛒 STEP 6: Clicking basket icon")
        product_listing_page.click_basket_icon()
        logger.info("✅ SUCCESS: Basket icon clicked")

        # Act - Step 7: Set prod detail count
        logger.info("🔢 STEP 7: Setting prod detail count")
        prod_detail_count = product_listing_page.get_prod_detail_count()
        assert prod_detail_count == 2, "Prod detail count should be 2"
        logger.info(f"✅ SUCCESS: Prod detail count is {prod_detail_count}")
        

        logger.info("🎉 TEST COMPLETED SUCCESSFULLY: Search and Add to Cart")
