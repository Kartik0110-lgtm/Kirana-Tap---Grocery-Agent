#!/usr/bin/env python3
"""
Debug script to test Blinkit search functionality step by step
"""

from blinkit_automation_clean import BlinkitAutomation
import time

def test_search_debug():
    """Test the search functionality with detailed debugging"""
    automation = BlinkitAutomation()
    
    try:
        print("🚀 Starting Blinkit Search Debug Test...")
        
        # Setup driver
        print("📱 Setting up Chrome driver...")
        if not automation.setup_driver():
            print("❌ Failed to setup driver")
            return
        
        print("✅ Driver setup successful")
        
        # Navigate to Blinkit
        print("🌐 Navigating to Blinkit website...")
        if not automation.navigate_to_blinkit():
            print("❌ Failed to navigate to Blinkit")
            return
        
        print("✅ Successfully navigated to Blinkit")
        print("🔍 Now testing search functionality...")
        
        # Wait a bit more for page to settle
        time.sleep(5)
        
        # Test item
        test_item = {'name': 'atta'}
        print(f"🔍 Testing search for: {test_item['name']}")
        
        # Try to search using the new helper function
        print("🔍 Testing helper function search_blinkit_item...")
        search_success = automation.search_blinkit_item(test_item['name'])
        
        if search_success:
            print("✅ Helper function search successful!")
        else:
            print("❌ Helper function search failed!")
        
        # Also test the main search method
        print("🔍 Testing main search_and_add_item method...")
        automation.search_and_add_item(test_item)
        
        print("✅ Search test completed")
        
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
    test_search_debug()
