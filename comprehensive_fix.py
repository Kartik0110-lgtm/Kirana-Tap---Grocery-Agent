#!/usr/bin/env python3
"""
Comprehensive Chrome Profile Fix
This script will restore the profile to its working state by fixing all security-related changes
"""

import os
import shutil
import time

def comprehensive_profile_fix():
    """Fix all Chrome profile issues caused by security changes"""
    print("🔧 Comprehensive Chrome Profile Fix...")
    print("=" * 50)
    
    profile_dir = os.path.join(os.getcwd(), "chrome-profile")
    default_dir = os.path.join(profile_dir, "Default")
    network_dir = os.path.join(default_dir, "Network")
    
    print(f"Profile directory: {profile_dir}")
    
    # Step 1: Remove LOCK file
    print("\n1️⃣ Removing LOCK file...")
    lock_file = os.path.join(default_dir, "LOCK")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
            print("✅ Removed LOCK file")
        except Exception as e:
            print(f"❌ Could not remove LOCK file: {e}")
    else:
        print("ℹ️ No LOCK file found")
    
    # Step 2: Restore Cookies file structure
    print("\n2️⃣ Restoring Cookies file structure...")
    network_cookies = os.path.join(network_dir, "Cookies")
    default_cookies = os.path.join(default_dir, "Cookies")
    
    if os.path.exists(network_cookies):
        try:
            # Copy Cookies file to Default directory
            shutil.copy2(network_cookies, default_cookies)
            print("✅ Copied Cookies file to Default directory")
            
            # Copy journal file if it exists
            network_cookies_journal = os.path.join(network_dir, "Cookies-journal")
            default_cookies_journal = os.path.join(default_dir, "Cookies-journal")
            if os.path.exists(network_cookies_journal):
                shutil.copy2(network_cookies_journal, default_cookies_journal)
                print("✅ Copied Cookies-journal file to Default directory")
                
        except Exception as e:
            print(f"❌ Could not copy Cookies file: {e}")
    else:
        print("⚠️ Cookies file not found in Network directory")
    
    # Step 3: Clean up journal files
    print("\n3️⃣ Cleaning up journal files...")
    journal_files = []
    for root, dirs, files in os.walk(profile_dir):
        for file in files:
            if file.endswith('-journal'):
                journal_path = os.path.join(root, file)
                try:
                    os.remove(journal_path)
                    journal_files.append(journal_path)
                except:
                    pass
    
    if journal_files:
        print(f"✅ Removed {len(journal_files)} journal files")
    else:
        print("ℹ️ No journal files found")
    
    # Step 4: Verify essential files are in place
    print("\n4️⃣ Verifying essential files...")
    essential_files = [
        os.path.join(default_dir, "Preferences"),
        os.path.join(default_dir, "Cookies"),
        os.path.join(default_dir, "Login Data"),
        os.path.join(default_dir, "Web Data")
    ]
    
    all_files_present = True
    for file_path in essential_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {os.path.basename(file_path)}: {size} bytes")
        else:
            print(f"❌ {os.path.basename(file_path)}: Missing")
            all_files_present = False
    
    # Step 5: Test profile directory permissions
    print("\n5️⃣ Testing profile directory permissions...")
    try:
        test_file = os.path.join(profile_dir, "test_write.tmp")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✅ Profile directory is writable")
    except Exception as e:
        print(f"❌ Profile directory is not writable: {e}")
        all_files_present = False
    
    print("\n" + "=" * 50)
    if all_files_present:
        print("🎯 Profile Fix Complete!")
        print("✅ Your Chrome profile should now work as it did before")
        print("💡 Auto-login should work again")
    else:
        print("⚠️ Profile Fix Partially Complete")
        print("❌ Some essential files are still missing")
        print("💡 You may need to log in again manually")
    
    print("\n📝 Next steps:")
    print("1. Run: python app.py")
    print("2. Check if auto-login works")
    print("3. If not, try logging in manually once")
    
    return all_files_present

if __name__ == "__main__":
    if comprehensive_profile_fix():
        print("\n✅ Profile restored successfully!")
    else:
        print("\n⚠️ Profile partially restored - some issues remain")
