"""
Test cases for N11 Phone search with filtering and sorting functionality.
"""
import pytest
from pages.home_page import HomePage
from pages.search_result_page import SearchResultPage
import logging


class TestPhoneFilterSort:
    """Test class for phone search with filtering and sorting."""

    @pytest.mark.smoke
    def test_phone_search_filter(self, home_page):
        """
        Test: Phone search with brand filtering, comment sorting and rating order verification.

        Steps:
        1. Search for "telefon" keyword
        2. Select second brand filter
        3. Sort by comment count (rating)
        4. Verify first 5 products are sorted by rating (descending)
        5. List products with free shipping
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
        
        # Act - Step 5: Verify rating sort order (descending)
        logger.info("🔍 STEP 5: Verifying that products are sorted by rating (descending order)")
        is_sorted_correctly = product_listing_page.verify_rating_sort_descending(5)
        assert is_sorted_correctly, "Products should be sorted by rating in descending order"
        logger.info("✅ SUCCESS: Rating sort order verified - products sorted correctly")
        
        # Act - Step 6: Filter by free shipping
        logger.info("🚚 STEP 6: Opening cargo filter to find free shipping products")
        product_listing_page.click_cargo_filter()
        logger.info("✅ SUCCESS: Cargo filter opened successfully")
        
        logger.info("📦 STEP 6.1: Selecting 'Free Shipment' option")
        product_listing_page.click_free_shipment_option()
        logger.info("✅ SUCCESS: Free shipment filter applied successfully")
        
        # Assert - Verify final results
        logger.info("📊 STEP 7: Final verification - checking that filtered results are present")
        
        # Verify cargo badge fields exist for all products
        logger.info("🚚 STEP 7.1: Verifying that all products have cargo badge information")
        all_have_cargo_badges = product_listing_page.verify_cargo_badge_field_all_products()
        assert all_have_cargo_badges == True, "All products should have cargo badge information"
        logger.info(f"✅ SUCCESS: Cargo badge verification completed - All products have badges: {all_have_cargo_badges}")
        
        logger.info("🎉 TEST COMPLETED SUCCESSFULLY: Phone Search with Rating Sort Verification")
