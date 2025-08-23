#!/usr/bin/env python3
"""
Test script to verify Chrome profile repair functionality.
This will help ensure the login persistence works reliably.
"""

from blinkit_automation_clean import BlinkitAutomation
import time
import os

def test_profile_repair():
    """Test the profile repair functionality"""
    print("🧪 Testing Chrome Profile Repair")
    print("=" * 50)
    
    # Create automation instance
    automation = BlinkitAutomation()
    
    print("\n📁 Checking current profile status...")
    automation.get_profile_info()
    
    print("\n🔍 Testing profile integrity...")
    if automation.check_profile_integrity():
        print("✅ Profile is healthy")
    else:
        print("⚠️ Profile has issues")
    
    print("\n🚀 Testing Chrome driver setup with repair capability...")
    
    # Try to setup driver
    if automation.setup_driver():
        print("✅ Chrome driver setup successful!")
        
        try:
            # Test basic navigation
            print("\n🌐 Testing basic navigation...")
            automation.driver.get("https://www.google.com")
            print("✅ Successfully navigated to Google")
            
            # Wait a bit to show the page
            print("\n⏳ Waiting 10 seconds to show the page...")
            time.sleep(10)
            
            print("\n🎯 Profile repair test completed!")
            print("   - Chrome should be running with persistent profile")
            print("   - Profile should be healthy and working")
            print("   - Login persistence should be maintained")
            print("   - Close the browser window when ready")
            
        except Exception as e:
            print(f"❌ Navigation test failed: {e}")
        
        finally:
            # Don't quit - let user see the page
            print("\n🔍 Browser window kept open for inspection")
            print("   Close it manually when ready")
    
    else:
        print("❌ Chrome driver setup failed!")
        print("\n🔧 This indicates the profile repair didn't work")

def test_profile_corruption_and_repair():
    """Test what happens when profile is corrupted"""
    print("\n🧪 Testing Profile Corruption & Repair")
    print("=" * 50)
    
    automation = BlinkitAutomation()
    
    # Check if profile exists
    profile_dir = "./chrome-profile"
    if os.path.exists(profile_dir):
        print(f"📁 Found existing profile: {profile_dir}")
        
        # Create a backup
        backup_dir = profile_dir + "_backup_test"
        if os.path.exists(backup_dir):
            import shutil
            shutil.rmtree(backup_dir)
        
        import shutil
        shutil.copytree(profile_dir, backup_dir)
        print(f"💾 Created backup: {backup_dir}")
        
        # Corrupt the profile by removing essential files
        print("🔧 Corrupting profile for testing...")
        essential_files = [
            os.path.join(profile_dir, "Default", "Cookies"),
            os.path.join(profile_dir, "Default", "Login Data")
        ]
        
        for file_path in essential_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️ Removed: {os.path.basename(file_path)}")
        
        print("✅ Profile corrupted for testing")
        
        # Test profile repair
        print("\n🔧 Testing profile repair...")
        if automation.repair_broken_profile():
            print("✅ Profile repair successful!")
            
            # Restore from backup
            print("🔄 Restoring profile from backup...")
            if os.path.exists(profile_dir):
                shutil.rmtree(profile_dir)
            shutil.copytree(backup_dir, profile_dir)
            print("✅ Profile restored from backup")
            
        else:
            print("❌ Profile repair failed!")
            
            # Restore from backup anyway
            print("🔄 Restoring profile from backup...")
            if os.path.exists(profile_dir):
                shutil.rmtree(profile_dir)
            shutil.copytree(backup_dir, profile_dir)
            print("✅ Profile restored from backup")
        
        # Clean up backup
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
            print("🧹 Cleaned up test backup")
    
    else:
        print("📁 No existing profile found - nothing to corrupt")

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Test profile repair functionality")
    print("2. Test profile corruption and repair")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_profile_repair()
    elif choice == "2":
        test_profile_corruption_and_repair()
    else:
        print("Invalid choice. Running basic profile repair test...")
        test_profile_repair()
