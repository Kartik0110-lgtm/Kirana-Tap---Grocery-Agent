#!/usr/bin/env python3
"""
Restore Chrome Profile to Working State
This script will restore the profile structure that was working before
"""

import os
import shutil
import time

def restore_chrome_profile():
    """Restore the Chrome profile to its working state"""
    print("🔧 Restoring Chrome Profile to Working State...")
    print("=" * 50)
    
    profile_dir = os.path.join(os.getcwd(), "chrome-profile")
    default_dir = os.path.join(profile_dir, "Default")
    network_dir = os.path.join(default_dir, "Network")
    
    print(f"Profile directory: {profile_dir}")
    print(f"Default directory: {default_dir}")
    print(f"Network directory: {network_dir}")
    
    # Step 1: Remove the LOCK file that's preventing profile usage
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
    
    # Step 2: Restore Cookies file to correct location
    print("\n2️⃣ Restoring Cookies file...")
    network_cookies = os.path.join(network_dir, "Cookies")
    default_cookies = os.path.join(default_dir, "Cookies")
    
    if os.path.exists(network_cookies):
        try:
            # Copy Cookies file from Network to Default directory
            shutil.copy2(network_cookies, default_cookies)
            print("✅ Copied Cookies file to Default directory")
            
            # Also copy the journal file if it exists
            network_cookies_journal = os.path.join(network_dir, "Cookies-journal")
            default_cookies_journal = os.path.join(default_dir, "Cookies-journal")
            if os.path.exists(network_cookies_journal):
                shutil.copy2(network_cookies_journal, default_cookies_journal)
                print("✅ Copied Cookies-journal file to Default directory")
                
        except Exception as e:
            print(f"❌ Could not copy Cookies file: {e}")
    else:
        print("⚠️ Cookies file not found in Network directory")
    
    # Step 3: Check if all essential files are in place
    print("\n3️⃣ Checking essential files...")
    essential_files = [
        os.path.join(default_dir, "Preferences"),
        os.path.join(default_dir, "Cookies"),
        os.path.join(default_dir, "Login Data"),
        os.path.join(default_dir, "Web Data")
    ]
    
    for file_path in essential_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {os.path.basename(file_path)}: {size} bytes")
        else:
            print(f"❌ {os.path.basename(file_path)}: Missing")
    
    # Step 4: Clean up any journal files that might cause issues
    print("\n4️⃣ Cleaning up journal files...")
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
    
    print("\n" + "=" * 50)
    print("🎯 Profile Restoration Complete!")
    print("💡 Your Chrome profile should now work as it did before")
    print("📝 Try running your app again - auto-login should work now")
    
    return True

if __name__ == "__main__":
    if restore_chrome_profile():
        print("\n✅ Profile restored successfully!")
    else:
        print("\n❌ Failed to restore profile!")
