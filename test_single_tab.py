#!/usr/bin/env python3
"""
Simple test script to verify that only one Chrome tab opens.
This will help diagnose the multiple tab issue.
"""

from blinkit_automation_clean import BlinkitAutomation
import time

def test_single_tab():
    """Test that only one Chrome tab opens"""
    print("🧪 Testing Single Chrome Tab")
    print("=" * 40)
    
    # Create automation instance
    automation = BlinkitAutomation()
    
    print("\n🔍 Testing Chrome driver setup...")
    
    # Try to setup driver
    if automation.setup_driver():
        print("✅ Chrome driver setup successful!")
        
        try:
            # Count the number of tabs
            tabs = automation.driver.window_handles
            print(f"📊 Number of tabs open: {len(tabs)}")
            
            if len(tabs) == 1:
                print("✅ Only one tab opened - this is correct!")
            else:
                print(f"⚠️ Multiple tabs opened: {len(tabs)}")
                print("   This indicates a profile issue")
            
            # Test basic navigation
            print("\n🌐 Testing basic navigation...")
            automation.driver.get("https://www.google.com")
            print("✅ Successfully navigated to Google")
            
            # Wait a bit to show the page
            print("\n⏳ Waiting 10 seconds to show the page...")
            time.sleep(10)
            
            # Check tabs again
            tabs_after = automation.driver.window_handles
            print(f"📊 Number of tabs after navigation: {len(tabs_after)}")
            
            if len(tabs_after) == 1:
                print("✅ Still only one tab - profile is working correctly!")
            else:
                print(f"⚠️ Tab count changed to: {len(tabs_after)}")
                print("   This indicates a profile or Chrome configuration issue")
            
            print("\n🎯 Chrome driver test completed!")
            print("   - Browser window should be open")
            print("   - Google page should be visible")
            print("   - Only ONE tab should exist")
            print("   - Close the browser window when ready")
            
        except Exception as e:
            print(f"❌ Navigation test failed: {e}")
        
        finally:
            # Don't quit - let user see the page
            print("\n🔍 Browser window kept open for inspection")
            print("   Close it manually when ready")
    
    else:
        print("❌ Chrome driver setup failed!")
        print("\n🔧 Troubleshooting steps:")
        print("   1. Make sure Chrome browser is installed")
        print("   2. Make sure ChromeDriver is in your PATH")
        print("   3. Try closing all Chrome windows and retry")
        print("   4. Check if antivirus is blocking Chrome")

if __name__ == "__main__":
    test_single_tab()
