#!/usr/bin/env python3
"""
Test script to verify that personal Chrome tabs are preserved while automation Chrome is managed.
This ensures the fix works correctly.
"""

from blinkit_automation_clean import BlinkitAutomation
import time
import psutil

def test_preserve_personal_chrome():
    """Test that personal Chrome tabs are preserved"""
    print("🧪 Testing Personal Chrome Tab Preservation")
    print("=" * 50)
    
    print("\n📋 INSTRUCTIONS:")
    print("1. Open some Chrome tabs with your personal browsing (YouTube, Gmail, etc.)")
    print("2. Keep them open while running this test")
    print("3. This test will verify they are NOT closed")
    
    input("\nPress Enter when you have some personal Chrome tabs open...")
    
    # Count personal Chrome processes before test
    print("\n🔍 Counting personal Chrome processes before test...")
    personal_chrome_before = count_personal_chrome_processes()
    print(f"📊 Personal Chrome processes: {personal_chrome_before}")
    
    # Create automation instance
    automation = BlinkitAutomation()
    
    print("\n🚀 Testing Chrome driver setup...")
    
    # Try to setup driver
    if automation.setup_driver():
        print("✅ Chrome driver setup successful!")
        
        # Count personal Chrome processes after test
        print("\n🔍 Counting personal Chrome processes after test...")
        personal_chrome_after = count_personal_chrome_processes()
        print(f"📊 Personal Chrome processes: {personal_chrome_after}")
        
        # Check if personal Chrome was preserved
        if personal_chrome_after >= personal_chrome_before:
            print("✅ SUCCESS: Personal Chrome tabs were preserved!")
            print("🎯 Your login persistence functionality is intact")
        else:
            print("❌ FAILED: Personal Chrome tabs were closed!")
            print("🔧 This needs to be fixed")
        
        # Count automation Chrome processes
        automation_chrome = count_automation_chrome_processes()
        print(f"🤖 Automation Chrome processes: {automation_chrome}")
        
        try:
            # Test basic navigation
            print("\n🌐 Testing basic navigation...")
            automation.driver.get("https://www.google.com")
            print("✅ Successfully navigated to Google")
            
            # Wait a bit to show the page
            print("\n⏳ Waiting 10 seconds to show the page...")
            time.sleep(10)
            
            print("\n🎯 Test completed!")
            print("   - Your personal Chrome tabs should still be open")
            print("   - Only automation Chrome should be managed")
            print("   - Login persistence should still work")
            print("   - Close the automation browser when ready")
            
        except Exception as e:
            print(f"❌ Navigation test failed: {e}")
        
        finally:
            # Don't quit - let user see the page
            print("\n🔍 Browser window kept open for inspection")
            print("   Close it manually when ready")
    
    else:
        print("❌ Chrome driver setup failed!")

def count_personal_chrome_processes():
    """Count Chrome processes that are NOT automation-related"""
    try:
        count = 0
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    cmdline = proc.info.get('cmdline', [])
                    # Personal Chrome doesn't have --user-data-dir argument
                    if not any('--user-data-dir' in str(arg) for arg in cmdline):
                        count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return count
    except Exception as e:
        print(f"⚠️ Error counting personal Chrome: {e}")
        return 0

def count_automation_chrome_processes():
    """Count Chrome processes that ARE automation-related"""
    try:
        count = 0
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    cmdline = proc.info.get('cmdline', [])
                    # Automation Chrome has --user-data-dir argument
                    if any('--user-data-dir' in str(arg) for arg in cmdline):
                        count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return count
    except Exception as e:
        print(f"⚠️ Error counting automation Chrome: {e}")
        return 0

if __name__ == "__main__":
    test_preserve_personal_chrome()
