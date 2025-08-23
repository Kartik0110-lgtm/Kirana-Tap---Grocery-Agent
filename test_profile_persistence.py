#!/usr/bin/env python3
"""
Comprehensive test script for Chrome profile persistence and login functionality.
This will help diagnose why login sessions aren't being saved.
"""

from blinkit_automation_clean import BlinkitAutomation
import time
import os

def test_profile_persistence():
    """Test the complete profile persistence functionality"""
    print("🧪 Testing Chrome Profile Persistence & Login")
    print("=" * 60)
    
    # Create automation instance
    automation = BlinkitAutomation()
    
    # Check profile status
    print("\n📁 Checking Chrome profile status...")
    automation.get_profile_info()
    
    # Setup driver with persistent profile
    print("\n🚀 Setting up Chrome driver with persistent profile...")
    if not automation.setup_driver():
        print("❌ Failed to setup Chrome driver")
        return False
    
    try:
        # Verify profile is working
        print("\n🔍 Verifying profile usage...")
        if automation.verify_profile_usage():
            print("✅ Profile verification successful")
        else:
            print("⚠️ Profile verification failed - this may cause login issues")
        
        # Navigate to Blinkit (this will check login status)
        print("\n🌐 Navigating to Blinkit...")
        if not automation.navigate_to_blinkit():
            print("❌ Failed to navigate to Blinkit")
            return False
        
        print("\n✅ Navigation completed!")
        
        # Check current login status
        print("\n🔐 Checking current login status...")
        if automation.is_user_logged_in():
            print("✅ User is currently logged in!")
            print("🎯 This means the profile is working correctly")
        else:
            print("❌ User is NOT logged in")
            print("📝 You'll need to log in manually on this first run")
            print("⏳ Waiting for manual login...")
            
            # Wait for user to log in
            max_wait = 180  # 3 minutes for manual login
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                if automation.is_user_logged_in():
                    print("✅ Manual login successful!")
                    print("💾 Session should now be saved in the profile")
                    break
                time.sleep(5)
            else:
                print("⚠️ Login timeout - continuing anyway")
        
        # Show profile information
        print("\n📊 Profile Information:")
        automation.get_profile_info()
        
        # Check cookies and session data
        try:
            cookies = automation.driver.get_cookies()
            print(f"🍪 Current cookies: {len(cookies)}")
            
            # Check for Blinkit-specific cookies
            blinkit_cookies = [c for c in cookies if 'blinkit' in c.get('domain', '').lower()]
            print(f"🔗 Blinkit cookies: {len(blinkit_cookies)}")
            
            if blinkit_cookies:
                print("✅ Blinkit cookies found - session should persist")
            else:
                print("⚠️ No Blinkit cookies found - session may not persist")
                
        except Exception as e:
            print(f"⚠️ Could not check cookies: {e}")
        
        print("\n🎯 Next steps:")
        print("   1. Close this browser window")
        print("   2. Run this script again")
        print("   3. Check if you're automatically logged in")
        print("   4. If not, the profile may not be working correctly")
        
        # Wait a bit to show the page
        print("\n⏳ Waiting 15 seconds to show the page...")
        time.sleep(15)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    finally:
        # Don't quit the driver - let user see the page
        print("\n🔍 Browser window kept open for inspection")
        print("   Close it manually when ready")

def clear_and_retest():
    """Clear profile and test from scratch"""
    print("🧹 Clearing Chrome profile and testing from scratch...")
    
    automation = BlinkitAutomation()
    automation.clear_chrome_profile()
    
    print("✅ Profile cleared. Testing fresh setup...")
    time.sleep(2)
    
    return test_profile_persistence()

def diagnose_profile_issues():
    """Diagnose common profile issues"""
    print("🔍 Diagnosing Profile Issues")
    print("=" * 40)
    
    profile_dir = "./chrome-profile"
    
    if not os.path.exists(profile_dir):
        print("❌ Profile directory doesn't exist")
        print("💡 This is normal for first run")
        return
    
    print(f"📁 Profile directory: {profile_dir}")
    
    try:
        # Check directory size
        total_size = 0
        file_count = 0
        
        for dirpath, dirnames, filenames in os.walk(profile_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                    file_count += 1
                except:
                    pass
        
        print(f"📊 Profile size: {total_size / (1024*1024):.2f} MB")
        print(f"📄 File count: {file_count}")
        
        if total_size < 1024*1024:  # Less than 1MB
            print("⚠️ Profile seems too small - may not be working correctly")
        else:
            print("✅ Profile size looks normal")
            
        # Check for specific Chrome profile files
        chrome_files = ['Preferences', 'Cookies', 'Login Data', 'Web Data']
        for file in chrome_files:
            filepath = os.path.join(profile_dir, 'Default', file)
            if os.path.exists(filepath):
                print(f"✅ Found {file}")
            else:
                print(f"❌ Missing {file}")
                
    except Exception as e:
        print(f"❌ Error checking profile: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "clear":
            clear_and_retest()
        elif sys.argv[1] == "diagnose":
            diagnose_profile_issues()
        else:
            print("Usage: python test_profile_persistence.py [clear|diagnose]")
    else:
        test_profile_persistence()
