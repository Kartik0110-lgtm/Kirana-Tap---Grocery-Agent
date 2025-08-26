#!/usr/bin/env python3
"""
Test script to verify detailed logging is working
"""

from blinkit_automation_clean import BlinkitAutomation

def test_logging():
    """Test that detailed logging is working"""
    print("🧪 Testing Detailed Logging...")
    print("=" * 50)
    
    # Create automation instance
    automation = BlinkitAutomation()
    
    # Test logging methods
    print("\n1️⃣ Testing basic logging...")
    automation.logger.info("🔍 This is a test info message")
    automation.logger.warning("⚠️ This is a test warning message")
    automation.logger.error("❌ This is a test error message")
    
    print("\n2️⃣ Testing profile info logging...")
    automation.get_profile_info()
    
    print("\n3️⃣ Testing profile debugging...")
    automation.debug_profile_issues()
    
    print("\n" + "=" * 50)
    print("🎯 Logging Test Complete!")
    print("💡 If you see detailed messages above, logging is working!")
    print("📝 Now try running your app - you should see detailed automation steps!")

if __name__ == "__main__":
    test_logging()
