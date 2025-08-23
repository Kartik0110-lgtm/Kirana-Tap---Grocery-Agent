#!/usr/bin/env python3
"""
Test script specifically for testing cart addition functionality
"""

from blinkit_automation_clean import BlinkitAutomation
import time

def test_cart_addition():
    """Test the cart addition functionality step by step"""
    automation = BlinkitAutomation()
    
    try:
        print("🚀 Starting Cart Addition Test...")
        
        # Setup driver
        if not automation.setup_driver():
            print("❌ Failed to setup driver")
            return
        
        # Navigate to Blinkit
        if not automation.navigate_to_blinkit():
            print("❌ Failed to navigate to Blinkit")
            return
        
        print("✅ Successfully navigated to Blinkit")
        
        # Test item
        test_item = {'name': 'amul toned milk'}
        print(f"🔍 Testing cart addition for: {test_item['name']}")
        
        # Try to search and add to cart
        automation.search_and_add_item(test_item)
        
        print("✅ Cart addition test completed")
        
        # Keep browser open for manual inspection
        input("Press Enter to close browser...")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if automation.driver:
            automation.driver.quit()
            print("Browser closed")

if __name__ == "__main__":
    test_cart_addition()
