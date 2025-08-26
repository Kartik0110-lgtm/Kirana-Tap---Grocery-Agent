#!/usr/bin/env python3
"""
Simple test to verify Chrome profile setup
"""

import os
import sys

def test_profile():
    print("Testing Chrome profile...")
    
    # Check if profile directory exists
    profile_dir = os.path.join(os.getcwd(), "chrome-profile")
    print(f"Profile directory: {profile_dir}")
    
    if os.path.exists(profile_dir):
        print("✅ Profile directory exists")
        
        # Check for lock files
        lock_files = []
        for root, dirs, files in os.walk(profile_dir):
            for file in files:
                if file in ['LOCK', 'LOCK.old']:
                    lock_files.append(os.path.join(root, file))
        
        if lock_files:
            print(f"⚠️ Found lock files: {len(lock_files)}")
            for lock_file in lock_files:
                try:
                    os.remove(lock_file)
                    print(f"🗑️ Removed: {lock_file}")
                except:
                    print(f"❌ Could not remove: {lock_file}")
        else:
            print("✅ No lock files found")
        
        # Check essential files
        essential_files = [
            os.path.join(profile_dir, "Default", "Preferences"),
            os.path.join(profile_dir, "Default", "Login Data"),
            os.path.join(profile_dir, "Default", "Cookies"),
            os.path.join(profile_dir, "Default", "Web Data")
        ]
        
        missing = []
        for file_path in essential_files:
            if not os.path.exists(file_path):
                missing.append(os.path.basename(file_path))
        
        if missing:
            print(f"⚠️ Missing files: {missing}")
        else:
            print("✅ All essential files found")
            
    else:
        print("❌ Profile directory missing")
    
    print("Profile test complete!")

if __name__ == "__main__":
    test_profile()
