#!/usr/bin/env python3
"""
Integration test script to verify Flask app can use the working BlinkitAutomation
"""

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("🔍 Testing imports...")
        
        # Test Flask app imports
        from app import app, socketio
        print("✅ Flask app imports successful")
        
        # Test BlinkitAutomation import
        from blinkit_automation_clean import BlinkitAutomation
        print("✅ BlinkitAutomation import successful")
        
        # Test if we can create an instance
        automation = BlinkitAutomation()
        print("✅ BlinkitAutomation instance creation successful")
        
        print("\n🎉 All imports successful! The integration is ready.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_automation_methods():
    """Test if the automation class has the required methods"""
    try:
        print("\n🔍 Testing automation methods...")
        
        from blinkit_automation_clean import BlinkitAutomation
        automation = BlinkitAutomation()
        
        # Check if required methods exist
        required_methods = [
            'setup_driver',
            'navigate_to_blinkit', 
            'search_blinkit_item',
            'search_and_add_item',
            'place_order'
        ]
        
        for method_name in required_methods:
            if hasattr(automation, method_name):
                print(f"✅ Method '{method_name}' exists")
            else:
                print(f"❌ Method '{method_name}' missing")
                return False
        
        print("✅ All required methods found!")
        return True
        
    except Exception as e:
        print(f"❌ Method test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Kirana Tap Integration...")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test automation methods
        methods_ok = test_automation_methods()
        
        if methods_ok:
            print("\n🎉 Integration test PASSED!")
            print("✅ Your Flask app is ready to use the working BlinkitAutomation!")
            print("\n🚀 You can now run:")
            print("   .\\run_kirana_tap.ps1")
            print("   or")
            print("   python app.py")
        else:
            print("\n❌ Integration test FAILED - Methods missing")
    else:
        print("\n❌ Integration test FAILED - Import issues")
    
    print("\n" + "=" * 50)
