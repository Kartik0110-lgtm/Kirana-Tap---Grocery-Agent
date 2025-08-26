#!/usr/bin/env python3
"""
Test script to verify Chrome profile setup and auto-login functionality
"""

import time
import os
from blinkit_automation_clean import BlinkitAutomation

def test_profile_setup():
    """Test the Chrome profile setup and verification"""
    print("🧪 Testing Chrome Profile Setup...")
    print("=" * 50)
    
    automation = BlinkitAutomation()
    
    # Test 1: Profile directory check
    print("\n1️⃣ Testing Profile Directory...")
    profile_dir = "./chrome-profile"
    if os.path.exists(profile_dir):
        print(f"✅ Profile directory exists: {profile_dir}")
        
        # Check profile size
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
        print(f"📁 Total files: {file_count}")
        
        # Check essential files
        essential_files = [
            os.path.join(profile_dir, "Default", "Preferences"),
            os.path.join(profile_dir, "Default", "Login Data"),
            os.path.join(profile_dir, "Default", "Cookies"),
            os.path.join(profile_dir, "Default", "Web Data")
        ]
        
        for file_path in essential_files:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✅ {os.path.basename(file_path)}: {size} bytes")
            else:
                print(f"❌ {os.path.basename(file_path)}: Missing")
    else:
        print(f"❌ Profile directory missing: {profile_dir}")
        return False
    
    # Test 2: Profile integrity check
    print("\n2️⃣ Testing Profile Integrity...")
    if automation.check_profile_integrity():
        print("✅ Profile integrity check passed")
    else:
        print("❌ Profile integrity check failed")
    
    # Test 3: Driver setup
    print("\n3️⃣ Testing Chrome Driver Setup...")
    if automation.setup_driver():
        print("✅ Chrome driver setup successful")
        
        # Test 4: Profile verification
        print("\n4️⃣ Testing Profile Usage Verification...")
        if automation.verify_profile_usage():
            print("✅ Profile usage verification passed")
        else:
            print("❌ Profile usage verification failed")
        
        # Test 5: Navigate to Blinkit and check login status
        print("\n5️⃣ Testing Blinkit Navigation and Login Status...")
        try:
            automation.driver.get("https://blinkit.com")
            time.sleep(5)
            
            if automation.is_user_logged_in():
                print("✅ User is logged in - profile is working!")
            else:
                print("❌ User is NOT logged in - profile may not be working")
                print("💡 This might be normal if you haven't logged in yet")
            
        except Exception as e:
            print(f"❌ Error testing Blinkit navigation: {e}")
        
        # Cleanup
        if automation.driver:
            automation.driver.quit()
            print("\n🧹 Chrome driver closed")
    else:
        print("❌ Chrome driver setup failed")
        return False
    
    print("\n" + "=" * 50)
    print("🎯 Profile Test Complete!")
    return True

def test_login_persistence():
    """Test if login persists between sessions"""
    print("\n🔄 Testing Login Persistence...")
    print("=" * 50)
    
    automation1 = BlinkitAutomation()
    
    if not automation1.setup_driver():
        print("❌ Failed to setup first driver")
        return False
    
    try:
        # Navigate to Blinkit
        automation1.driver.get("https://blinkit.com")
        time.sleep(5)
        
        # Check login status
        login_status_1 = automation1.is_user_logged_in()
        print(f"📱 First session login status: {'✅ Logged In' if login_status_1 else '❌ Not Logged In'}")
        
        # Close first driver
        automation1.driver.quit()
        time.sleep(3)
        
        # Start second driver with same profile
        automation2 = BlinkitAutomation()
        if not automation2.setup_driver():
            print("❌ Failed to setup second driver")
            return False
        
        try:
            # Navigate to Blinkit again
            automation2.driver.get("https://blinkit.com")
            time.sleep(5)
            
            # Check login status again
            login_status_2 = automation2.is_user_logged_in()
            print(f"📱 Second session login status: {'✅ Logged In' if login_status_2 else '❌ Not Logged In'}")
            
            # Check persistence
            if login_status_1 == login_status_2:
                if login_status_1:
                    print("✅ Login persistence working - user stays logged in")
                else:
                    print("ℹ️ User not logged in in either session")
            else:
                print("❌ Login persistence failed - status changed between sessions")
            
        finally:
            automation2.driver.quit()
            
    except Exception as e:
        print(f"❌ Error testing login persistence: {e}")
        if automation1.driver:
            automation1.driver.quit()
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Chrome Profile Tests...")
    
    # Run basic profile tests
    if test_profile_setup():
        print("\n✅ Basic profile tests passed!")
        
        # Run login persistence test
        if test_login_persistence():
            print("\n✅ Login persistence test completed!")
        else:
            print("\n❌ Login persistence test failed!")
    else:
        print("\n❌ Basic profile tests failed!")
    
    print("\n🏁 All tests completed!")
