#!/usr/bin/env python3
"""
Simple test script to verify Chrome driver setup works.
This will help diagnose any Chrome driver issues.
"""

from blinkit_automation_clean import BlinkitAutomation
import time

def test_chrome_setup():
    """Test basic Chrome driver setup"""
    print("🧪 Testing Chrome Driver Setup")
    print("=" * 40)
    
    # Create automation instance
    automation = BlinkitAutomation()
    
    print("\n🔍 Testing Chrome driver setup...")
    
    # Try to setup driver
    if automation.setup_driver():
        print("✅ Chrome driver setup successful!")
        
        try:
            # Test basic navigation
            print("\n🌐 Testing basic navigation...")
            automation.driver.get("https://www.google.com")
            print("✅ Successfully navigated to Google")
            
            # Wait a bit to show the page
            print("\n⏳ Waiting 5 seconds to show the page...")
            time.sleep(5)
            
            print("\n🎯 Chrome driver is working correctly!")
            print("   - Browser window should be open")
            print("   - Google page should be visible")
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
    test_chrome_setup()
