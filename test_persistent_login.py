#!/usr/bin/env python3
"""
Test script for persistent Chrome profile login functionality.
This demonstrates how the automation will maintain login sessions across runs.
"""

from blinkit_automation_clean import BlinkitAutomation
import time

def test_persistent_login():
    """Test the persistent login functionality"""
    print("🧪 Testing Persistent Chrome Profile Login")
    print("=" * 50)
    
    # Create automation instance
    automation = BlinkitAutomation()
    
    # Check profile status
    print("\n📁 Checking Chrome profile status...")
    automation.get_profile_info()
    
    # Setup driver with persistent profile
    print("\n🚀 Setting up Chrome driver with persistent profile...")
    if not automation.setup_driver():
        print("❌ Failed to setup Chrome driver")
        return
    
    try:
        # Navigate to Blinkit (this will check login status)
        print("\n🌐 Navigating to Blinkit...")
        if not automation.navigate_to_blinkit():
            print("❌ Failed to navigate to Blinkit")
            return
        
        print("\n✅ Navigation completed!")
        print("\n📝 What happened:")
        print("   - If this was your first run: You needed to log in manually")
        print("   - If you've run before: You were automatically logged in")
        print("   - Your login session is now saved in ./chrome-profile/")
        
        # Wait a bit to show the page
        print("\n⏳ Waiting 10 seconds to show the page...")
        time.sleep(10)
        
        print("\n🎯 Next steps:")
        print("   1. Close this browser window")
        print("   2. Run this script again")
        print("   3. You should be automatically logged in!")
        print("   4. No more manual OTP entry needed")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        # Don't quit the driver - let user see the page
        print("\n🔍 Browser window kept open for inspection")
        print("   Close it manually when ready")

def clear_profile():
    """Clear the Chrome profile (useful for troubleshooting)"""
    print("🧹 Clearing Chrome profile...")
    automation = BlinkitAutomation()
    automation.clear_chrome_profile()
    print("✅ Profile cleared. Next run will require fresh login.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_profile()
    else:
        test_persistent_login()
