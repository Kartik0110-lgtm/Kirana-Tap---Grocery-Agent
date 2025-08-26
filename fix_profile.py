#!/usr/bin/env python3
"""
Fix Chrome Profile Issues
This script will clean up the Chrome profile and remove any lock files
"""

import os
import shutil
import time
import psutil

def fix_chrome_profile():
    """Fix Chrome profile issues by cleaning up lock files and corrupted data"""
    print("🔧 Fixing Chrome Profile Issues...")
    print("=" * 50)
    
    profile_dir = os.path.join(os.getcwd(), "chrome-profile")
    
    # Step 1: Kill any existing Chrome processes
    print("\n1️⃣ Killing existing Chrome processes...")
    try:
        killed_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    proc.kill()
                    killed_count += 1
                    print(f"🔄 Killed Chrome process (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if killed_count > 0:
            print(f"✅ Killed {killed_count} Chrome processes")
            time.sleep(3)  # Wait for processes to fully terminate
        else:
            print("ℹ️ No Chrome processes found")
    except Exception as e:
        print(f"⚠️ Error killing Chrome processes: {e}")
    
    # Step 2: Remove lock files
    print("\n2️⃣ Removing lock files...")
    lock_files = []
    for root, dirs, files in os.walk(profile_dir):
        for file in files:
            if file in ['LOCK', 'LOCK.old']:
                lock_path = os.path.join(root, file)
                try:
                    os.remove(lock_path)
                    lock_files.append(lock_path)
                    print(f"🗑️ Removed lock file: {lock_path}")
                except Exception as e:
                    print(f"⚠️ Could not remove {lock_path}: {e}")
    
    if lock_files:
        print(f"✅ Removed {len(lock_files)} lock files")
    else:
        print("ℹ️ No lock files found")
    
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
                    print(f"🗑️ Removed journal file: {journal_path}")
                except Exception as e:
                    print(f"⚠️ Could not remove {journal_path}: {e}")
    
    if journal_files:
        print(f"✅ Removed {len(journal_files)} journal files")
    else:
        print("ℹ️ No journal files found")
    
    # Step 4: Check profile integrity
    print("\n4️⃣ Checking profile integrity...")
    essential_files = [
        os.path.join(profile_dir, "Default", "Preferences"),
        os.path.join(profile_dir, "Default", "Login Data"),
        os.path.join(profile_dir, "Default", "Cookies"),
        os.path.join(profile_dir, "Default", "Web Data")
    ]
    
    missing_files = []
    for file_path in essential_files:
        if not os.path.exists(file_path):
            missing_files.append(os.path.basename(file_path))
    
    if missing_files:
        print(f"⚠️ Missing essential files: {missing_files}")
        print("🔄 Profile may need to be recreated")
        
        # Create backup and recreate profile
        backup_dir = profile_dir + "_backup_" + str(int(time.time()))
        try:
            shutil.copytree(profile_dir, backup_dir)
            print(f"💾 Created backup: {backup_dir}")
            
            # Remove and recreate profile
            shutil.rmtree(profile_dir)
            os.makedirs(profile_dir, exist_ok=True)
            print("✅ Recreated fresh profile directory")
            
        except Exception as e:
            print(f"❌ Failed to recreate profile: {e}")
            return False
    else:
        print("✅ All essential profile files found")
    
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
        return False
    
    print("\n" + "=" * 50)
    print("🎯 Profile Fix Complete!")
    print("💡 You can now try running your app again")
    print("📝 Note: You may need to log in again if the profile was recreated")
    
    return True

if __name__ == "__main__":
    if fix_chrome_profile():
        print("\n✅ Profile issues fixed successfully!")
    else:
        print("\n❌ Failed to fix profile issues!")
