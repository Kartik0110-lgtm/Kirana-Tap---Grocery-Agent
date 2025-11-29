from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging

class BlinkitAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for automation actions"""
        # Clear any existing handlers to avoid duplicate logging
        logging.getLogger().handlers.clear()
        
        # Setup detailed logging with timestamps and Unicode support
        import sys
        
        # Create console handler with UTF-8 encoding
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        # Create file handler with UTF-8 encoding
        file_handler = logging.FileHandler('automation.log', mode='w', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        # Configure root logger
        logging.basicConfig(
            level=logging.INFO,
            handlers=[console_handler, file_handler]
        )
        
        # Set our logger to INFO level and ensure it's not filtered
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Ensure the logger propagates to root logger
        self.logger.propagate = True
        
        self.logger.info("🚀 Logging system initialized - you'll see detailed automation steps!")
    
    def setup_driver(self):
        """Setup Chrome driver with persistent profile for automatic login"""
        try:
            # OPTIMIZED: Fast startup - skip extensive debugging
            self.logger.info("🚀 Fast startup mode - skipping detailed debugging")
            
            # Only check for existing automation Chrome processes (essential)
            if self.check_existing_automation_chrome():
                self.logger.info("🔄 Found existing automation Chrome, cleaning up...")
                if not self.force_close_chrome_and_cleanup():
                    self.logger.warning("⚠️ Chrome cleanup failed, continuing anyway...")
            
            # Ensure profile directory is ready (essential)
            if not self.ensure_profile_directory():
                self.logger.error("❌ Failed to setup profile directory")
                return False
            
            chrome_options = Options()
            
            # Use absolute path for profile directory to avoid any path issues
            import os
            # Get the absolute path to the current working directory and then to chrome-profile
            current_dir = os.getcwd()
            profile_path = os.path.join(current_dir, "chrome-profile")
            profile_path = os.path.abspath(profile_path)
            
            # Ensure the profile directory exists
            if not os.path.exists(profile_path):
                os.makedirs(profile_path, exist_ok=True)
                self.logger.info(f"📁 Created profile directory: {profile_path}")
            
            chrome_options.add_argument(f"--user-data-dir={profile_path}")
            chrome_options.add_argument("--profile-directory=Default")
            
            # Prevent multiple Chrome instances and ensure single profile usage
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            
            # Anti-detection options to make Chrome appear more human-like
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Essential stability options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            
            # Window and display options
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            
            # More human-like user agent
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Remove potentially problematic options
            # chrome_options.add_argument("--remote-debugging-port=9222")  # Removed - can cause conflicts
            
            self.logger.info(f"Chrome options configured with profile: {profile_path}")
            self.logger.info("Attempting to start driver...")
            
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                self.wait = WebDriverWait(self.driver, 20)
                
                # Execute JavaScript to remove automation indicators
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
                self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
                
                # Verify profile is actually being used
                self.logger.info("🔍 Verifying profile usage...")
                if self.verify_profile_usage():
                    self.logger.info("✅ Chrome driver setup successful with persistent profile")
                    self.logger.info("📝 First run: You'll need to log in manually with OTP")
                    self.logger.info("📝 Subsequent runs: Will automatically use saved login session")
                    self.logger.info(f"📁 Profile directory: {profile_path}")
                    self.logger.info("🕵️ Anti-detection measures applied")
                else:
                    self.logger.warning("⚠️ Profile verification failed - login may not persist")
                
                return True
                
            except Exception as driver_error:
                self.logger.error(f"❌ Chrome driver creation failed: {driver_error}")
                
                # Try to repair the profile and retry once
                self.logger.info("🔄 Profile may be corrupted, attempting repair and retry...")
                if self.repair_broken_profile():
                    try:
                        self.logger.info("🔄 Retrying with repaired profile...")
                        self.driver = webdriver.Chrome(options=chrome_options)
                        self.wait = WebDriverWait(self.driver, 20)
                        
                        # Execute JavaScript to remove automation indicators
                        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                        self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
                        self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
                        
                        self.logger.info("✅ Chrome driver started successfully after profile repair!")
                        return True
                        
                    except Exception as retry_error:
                        self.logger.error(f"❌ Retry with repaired profile failed: {retry_error}")
                
                # Try fallback without persistent profile
                self.logger.info("🔄 Trying fallback setup without persistent profile...")
                try:
                    fallback_options = Options()
                    fallback_options.add_argument("--no-sandbox")
                    fallback_options.add_argument("--disable-dev-shm-usage")
                    fallback_options.add_argument("--disable-gpu")
                    fallback_options.add_argument("--start-maximized")
                    
                    self.driver = webdriver.Chrome(options=fallback_options)
                    self.wait = WebDriverWait(self.driver, 20)
                    
                    self.logger.warning("⚠️ Chrome driver started without persistent profile")
                    self.logger.warning("⚠️ You'll need to log in manually each time")
                    self.logger.info("✅ Fallback setup successful")
                    
                    return True
                    
                except Exception as fallback_error:
                    self.logger.error(f"❌ Fallback setup also failed: {fallback_error}")
                    
                    # Last resort: try to kill Chrome processes and retry
                    self.logger.info("🔄 Last resort: attempting to kill Chrome processes...")
                    if self.force_kill_chrome():
                        try:
                            time.sleep(3)  # Wait a bit more
                            self.driver = webdriver.Chrome(options=fallback_options)
                            self.wait = WebDriverWait(self.driver, 20)
                            self.logger.info("✅ Chrome driver started after killing processes")
                            return True
                        except Exception as final_error:
                            self.logger.error(f"❌ Final attempt failed: {final_error}")
                    
                    return False
            
        except Exception as e:
            self.logger.error(f"❌ Failed to setup Chrome driver: {e}")
            return False
    
    def check_chrome_status(self):
        """Check if Chrome is running and handle potential conflicts"""
        import psutil
        import os
        
        try:
            # Check if Chrome is already running
            chrome_processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if 'chrome' in proc.info['name'].lower():
                        chrome_processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if chrome_processes:
                self.logger.info(f"📊 Found {len(chrome_processes)} Chrome processes running")
                self.logger.info("💡 This is normal and shouldn't cause issues")
            
            # Check if profile directory exists and is accessible
            profile_dir = os.path.join(os.getcwd(), "chrome-profile")
            if os.path.exists(profile_dir):
                try:
                    # Test if we can write to the profile directory
                    test_file = os.path.join(profile_dir, "test_write.tmp")
                    with open(test_file, 'w') as f:
                        f.write("test")
                    os.remove(test_file)
                    self.logger.info("✅ Profile directory is accessible and writable")
                except Exception as e:
                    self.logger.warning(f"⚠️ Profile directory access issue: {e}")
                    self.logger.info("🔄 Will try to create new profile directory")
            else:
                self.logger.info("📁 Profile directory doesn't exist yet - will be created")
            
            return True
            
        except Exception as e:
            self.logger.warning(f"⚠️ Could not check Chrome status: {e}")
            return True  # Continue anyway
    
    def force_kill_chrome(self):
        """Force kill only automation-related Chrome processes, preserve user's personal Chrome tabs"""
        import psutil
        
        try:
            killed_count = 0
            preserved_count = 0
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'chrome' in proc.info['name'].lower():
                        # Check if this is an automation-related Chrome process
                        cmdline = proc.info.get('cmdline', [])
                        is_automation = any('--user-data-dir' in str(arg) for arg in cmdline)
                        
                        if is_automation:
                            # This is our automation Chrome - kill it
                            proc.kill()
                            killed_count += 1
                            self.logger.info(f"🔄 Killed automation Chrome process (PID: {proc.info['pid']})")
                        else:
                            # This is user's personal Chrome - preserve it
                            preserved_count += 1
                            self.logger.info(f"💾 Preserved personal Chrome process (PID: {proc.info['pid']})")
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if killed_count > 0:
                self.logger.info(f"🔄 Killed {killed_count} automation Chrome processes")
                self.logger.info(f"💾 Preserved {preserved_count} personal Chrome processes")
                time.sleep(2)  # Wait for processes to fully terminate
                return True
            else:
                self.logger.info("ℹ️ No automation Chrome processes found to kill")
                self.logger.info(f"💾 {preserved_count} personal Chrome processes preserved")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Failed to kill Chrome processes: {e}")
            return False
    
    def force_close_chrome_and_cleanup(self):
        """Force close only automation Chrome and ensure clean profile usage, preserve user's personal Chrome"""
        try:
            self.logger.info("🔄 Force closing automation Chrome and cleaning up...")
            self.logger.info("💾 Preserving your personal Chrome tabs...")
            
            # Kill only automation-related Chrome processes
            self.force_kill_chrome()
            
            # Wait a bit for processes to fully terminate
            time.sleep(3)
            
            # Check if profile directory is locked
            import os
            profile_dir = os.path.join(os.getcwd(), "chrome-profile")
            
            if os.path.exists(profile_dir):
                try:
                    # Try to rename the profile directory temporarily to check if it's locked
                    temp_name = profile_dir + "_temp"
                    if os.path.exists(temp_name):
                        import shutil
                        shutil.rmtree(temp_name)
                    
                    os.rename(profile_dir, temp_name)
                    os.rename(temp_name, profile_dir)
                    self.logger.info("✅ Profile directory is not locked")
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ Profile directory may be locked: {e}")
                    # Try to remove and recreate the profile
                    try:
                        import shutil
                        shutil.rmtree(profile_dir)
                        os.makedirs(profile_dir, exist_ok=True)
                        self.logger.info("✅ Profile directory recreated")
                    except Exception as recreate_e:
                        self.logger.error(f"❌ Failed to recreate profile directory: {recreate_e}")
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Chrome cleanup failed: {e}")
            return False
    
    def check_profile_integrity(self):
        """Check if the Chrome profile is intact and usable"""
        try:
            import os
            
            profile_dir = os.path.join(os.getcwd(), "chrome-profile")
            if not os.path.exists(profile_dir):
                self.logger.warning("⚠️ Profile directory doesn't exist")
                return False
            
            # Check for essential Chrome profile files
            essential_files = [
                os.path.join(profile_dir, "Default", "Preferences"),
                os.path.join(profile_dir, "Default", "Cookies"),
                os.path.join(profile_dir, "Default", "Login Data"),
                os.path.join(profile_dir, "Default", "Web Data")
            ]
            
            missing_files = []
            for file_path in essential_files:
                if not os.path.exists(file_path):
                    missing_files.append(os.path.basename(file_path))
            
            if missing_files:
                self.logger.warning(f"⚠️ Missing essential profile files: {missing_files}")
                # Don't fail completely - some files might be created later
                if len(missing_files) >= 3:  # If more than 3 files missing, profile is broken
                    self.logger.error("❌ Too many essential files missing - profile is broken")
                    return False
                else:
                    self.logger.warning("⚠️ Some files missing but profile may still work")
                    return True
            else:
                self.logger.info("✅ All essential profile files found")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Profile integrity check failed: {e}")
            return False
    
    def repair_broken_profile(self):
        """Attempt to repair a broken Chrome profile"""
        try:
            import os
            import shutil
            
            profile_dir = os.path.join(os.getcwd(), "chrome-profile")
            
            if not os.path.exists(profile_dir):
                self.logger.info("📁 Profile directory doesn't exist - nothing to repair")
                return True
            
            # Check if profile is actually broken
            if self.check_profile_integrity():
                self.logger.info("✅ Profile is healthy - no repair needed")
                return True
            
            self.logger.warning("🔧 Profile appears to be broken, attempting repair...")
            
            # Create backup of current profile
            backup_dir = profile_dir + "_backup_" + str(int(time.time()))
            try:
                shutil.copytree(profile_dir, backup_dir)
                self.logger.info(f"💾 Created backup: {backup_dir}")
            except Exception as e:
                self.logger.warning(f"⚠️ Could not create backup: {e}")
            
            # Remove broken profile
            try:
                shutil.rmtree(profile_dir)
                self.logger.info("🗑️ Removed broken profile directory")
            except Exception as e:
                self.logger.error(f"❌ Could not remove broken profile: {e}")
                return False
            
            # Create fresh profile directory
            try:
                os.makedirs(profile_dir, exist_ok=True)
                self.logger.info("📁 Created fresh profile directory")
                return True
            except Exception as e:
                self.logger.error(f"❌ Could not create fresh profile: {e}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Profile repair failed: {e}")
            return False
    
    def check_existing_automation_chrome(self):
        """Check if there are existing automation Chrome processes that need cleanup"""
        try:
            import psutil
            
            automation_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'chrome' in proc.info['name'].lower():
                        cmdline = proc.info.get('cmdline', [])
                        if any('--user-data-dir' in str(arg) for arg in cmdline):
                            automation_processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if automation_processes:
                self.logger.info(f"🔍 Found {len(automation_processes)} existing automation Chrome processes")
                for proc in automation_processes:
                    self.logger.info(f"   - PID: {proc['pid']}")
                return True
            else:
                self.logger.info("✅ No existing automation Chrome processes found")
                return False
                
        except Exception as e:
            self.logger.warning(f"⚠️ Could not check for existing automation Chrome: {e}")
            return False
    
    def verify_profile_usage(self):
        """Verify that the Chrome profile is actually being used"""
        try:
            import os
            if not self.driver:
                self.logger.warning("⚠️ No driver available to verify profile")
                return False
            
            # Check if the profile directory is being used
            profile_dir = os.path.join(os.getcwd(), "chrome-profile")
            
            if not os.path.exists(profile_dir):
                self.logger.warning("⚠️ Profile directory doesn't exist yet")
                return False
            
            # Check if Chrome is actually using the profile
            try:
                # Get Chrome's user data directory from the running instance
                chrome_data_dir = self.driver.execute_script("""
                    return window.chrome && window.chrome.runtime && 
                           window.chrome.runtime.getManifest && 
                           window.chrome.runtime.getManifest().name ? 'Chrome Profile Active' : 'No Chrome Profile';
                """)
                
                self.logger.info(f"🔍 Chrome profile status: {chrome_data_dir}")
                
                # Check if cookies are being saved
                cookies = self.driver.get_cookies()
                self.logger.info(f"🍪 Found {len(cookies)} cookies in current session")
                
                # Check if localStorage is accessible (indicates profile is working)
                try:
                    self.driver.execute_script("localStorage.setItem('test', 'value')")
                    test_value = self.driver.execute_script("return localStorage.getItem('test')")
                    self.driver.execute_script("localStorage.removeItem('test')")
                    
                    if test_value == 'value':
                        self.logger.info("✅ Local storage is working - profile is active")
                        return True
                    else:
                        self.logger.warning("⚠️ Local storage test failed")
                        return False
                        
                except Exception as e:
                    self.logger.warning(f"⚠️ Local storage test failed: {e}")
                    return False
                
            except Exception as e:
                self.logger.warning(f"⚠️ Could not verify profile usage: {e}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Profile verification failed: {e}")
            return False
    
    def ensure_profile_directory(self):
        """Ensure the Chrome profile directory exists and is properly set up"""
        try:
            import os
            
            profile_dir = os.path.join(os.getcwd(), "chrome-profile")
            
            # Create profile directory if it doesn't exist
            if not os.path.exists(profile_dir):
                os.makedirs(profile_dir, exist_ok=True)
                self.logger.info(f"📁 Created Chrome profile directory: {profile_dir}")
            else:
                self.logger.info(f"📁 Chrome profile directory exists: {profile_dir}")
            
            # Check profile directory permissions
            try:
                test_file = os.path.join(profile_dir, "test_write.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                self.logger.info("✅ Profile directory is writable")
                return True
            except Exception as e:
                self.logger.error(f"❌ Profile directory is not writable: {e}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Failed to ensure profile directory: {e}")
            return False
    
    def close_popups_and_modals(self):
        """Close any popups, modals, or overlays that might be blocking the page"""
        try:
            # Common selectors for Blinkit popups and modals
            popup_selectors = [
                # Modal close buttons
                "//button[contains(@class, 'close') or contains(@class, 'Close')]",
                "//div[contains(@class, 'close') or contains(@class, 'Close')]",
                # Modal overlays (click to close)
                "//div[contains(@class, 'modal-overlay') or contains(@class, 'Modal')]",
                "//div[contains(@class, 'overlay')]",
                # Specific Blinkit modals
                "//div[contains(@class, 'ReactModal__Overlay')]",
                # Close icons
                "//button[@aria-label='Close']",
                "//button[@aria-label='close']",
                # X buttons
                "//button[text()='×']",
                "//span[text()='×']"
            ]

            closed_any = False
            for selector in popup_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        for element in elements:
                            try:
                                if element.is_displayed():
                                    element.click()
                                    self.logger.info(f"✅ Closed popup/modal using selector: {selector}")
                                    closed_any = True
                                    time.sleep(0.5)
                                    break
                            except:
                                pass
                except:
                    pass

            # Also try pressing Escape key to close modals
            try:
                from selenium.webdriver.common.keys import Keys
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.ESCAPE).perform()
                if not closed_any:
                    self.logger.info("🔑 Pressed ESC to close any modals")
                time.sleep(0.5)
            except:
                pass

            return True
        except Exception as e:
            self.logger.debug(f"Popup closing attempt: {e}")
            return False

    def navigate_to_blinkit(self):
        """Navigate to Blinkit website and check login status (location handling removed)"""
        try:
            self.driver.get("https://blinkit.com")
            self.logger.info("Navigated to Blinkit website")

            # Wait for page to load
            time.sleep(5)

            # Close any popups or modals that might be blocking
            self.close_popups_and_modals()
            
            # Check if user is already logged in
            if self.is_user_logged_in():
                self.logger.info("✅ User is already logged in - no need for manual login!")
                self.logger.info("Proceeding with automation...")
            else:
                self.logger.warning("⚠️ User is NOT logged in")
                self.logger.info("📝 INSTRUCTIONS: Please log in manually with OTP on this first run")
                self.logger.info("📝 After login, the session will be saved for future runs")
                self.logger.info("📝 Waiting for manual login to complete...")
                
                # Wait for user to manually log in
                max_login_wait = 120  # 2 minutes for manual login
                start_time = time.time()
                
                while time.time() - start_time < max_login_wait:
                    if self.is_user_logged_in():
                        self.logger.info("✅ Manual login successful! Session saved for future runs")
                        break
                    time.sleep(5)
                else:
                    self.logger.warning("⚠️ Login timeout - continuing anyway, but cart operations may fail")
            
            # Location detection removed - account is now remembered automatically
            self.logger.info("✅ Account is remembered - no need for location detection")
            
            # Additional wait to ensure page is fully loaded
            time.sleep(3)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to Blinkit: {e}")
            return False
    
    def is_user_logged_in(self):
        """Check if user is already logged in by looking for profile/user elements"""
        try:
            # Wait a moment for page to load
            time.sleep(2)
            
            # Look for elements that indicate user is logged in
            logged_in_indicators = [
                "//div[contains(@class, 'profile') or contains(@class, 'Profile')]",
                "//div[contains(@class, 'user') or contains(@class, 'User')]",
                "//div[contains(@class, 'account') or contains(@class, 'Account')]",
                "//img[contains(@alt, 'profile') or contains(@alt, 'Profile')]",
                "//div[contains(@data-testid, 'profile') or contains(@data-testid, 'user')]",
                "//span[contains(text(), 'Hi') or contains(text(), 'Hello')]",
                "//div[contains(text(), 'Hi') or contains(text(), 'Hello')]"
            ]
            
            for selector in logged_in_indicators:
                try:
                    element = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if element.is_displayed():
                        self.logger.info(f"✅ Login detected (found: {selector})")
                        return True
                except:
                    continue
            
            # Also check if login/signup buttons are NOT present (negative check)
            login_indicators = [
                "//button[contains(text(), 'Login') or contains(text(), 'Sign In')]",
                "//a[contains(text(), 'Login') or contains(text(), 'Sign In')]",
                "//div[contains(text(), 'Login') or contains(text(), 'Sign In')]"
            ]
            
            for selector in login_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element.is_displayed():
                        self.logger.info(f"❌ Login button found - user NOT logged in")
                        return False
                except:
                    continue
            
            # If we can't determine, assume not logged in for safety
            self.logger.warning("⚠️ Could not determine login status, assuming not logged in")
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking login status: {e}")
            return False
    
    def clear_chrome_profile(self):
        """Clear the Chrome profile to force fresh login (useful if login issues occur)"""
        import shutil
        import os
        
        try:
            profile_dir = os.path.join(os.getcwd(), "chrome-profile")
            if os.path.exists(profile_dir):
                shutil.rmtree(profile_dir)
                self.logger.info(f"✅ Successfully cleared Chrome profile: {profile_dir}")
                self.logger.info("📝 Next run will require fresh manual login")
                return True
            else:
                self.logger.info(f"ℹ️ No Chrome profile found to clear: {profile_dir}")
                return True
        except Exception as e:
            self.logger.error(f"❌ Failed to clear Chrome profile: {e}")
            return False
    
    def get_profile_info(self):
        """Get information about the current Chrome profile"""
        import os
        
        try:
            profile_dir = os.path.join(os.getcwd(), "chrome-profile")
            if os.path.exists(profile_dir):
                profile_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                    for dirpath, dirnames, filenames in os.walk(profile_dir)
                    for filename in filenames)
                
                self.logger.info(f"📁 Chrome profile directory: {profile_dir}")
                self.logger.info(f"📊 Profile size: {profile_size / (1024*1024):.2f} MB")
                self.logger.info(f"✅ Profile exists and is ready for use")
                
                # Check for lock files
                lock_files = []
                for root, dirs, files in os.walk(profile_dir):
                    for file in files:
                        if file in ['LOCK', 'LOCK.old']:
                            lock_files.append(os.path.join(root, file))
                
                if lock_files:
                    self.logger.warning(f"⚠️ Found {len(lock_files)} lock files: {lock_files}")
                    self.logger.warning("⚠️ These may prevent profile from being used")
                else:
                    self.logger.info("✅ No lock files found")
                
                return True
            else:
                self.logger.info(f"📁 Chrome profile directory: {profile_dir}")
                self.logger.info(f"❌ Profile does not exist yet")
                self.logger.info(f"📝 First run will create the profile")
                return False
        except Exception as e:
            self.logger.error(f"❌ Error getting profile info: {e}")
            return False
    
    def debug_profile_issues(self):
        """Debug profile issues and provide solutions"""
        import os
        
        try:
            profile_dir = os.path.join(os.getcwd(), "chrome-profile")
            self.logger.info("🔍 Debugging Chrome profile issues...")
            
            # Check if profile directory exists
            if not os.path.exists(profile_dir):
                self.logger.error(f"❌ Profile directory missing: {profile_dir}")
                self.logger.info("💡 Solution: Profile will be created automatically")
                return False
            
            # Check for lock files
            lock_files = []
            for root, dirs, files in os.walk(profile_dir):
                for file in files:
                    if file in ['LOCK', 'LOCK.old']:
                        lock_files.append(os.path.join(root, file))
            
            if lock_files:
                self.logger.warning(f"⚠️ Found lock files: {lock_files}")
                self.logger.info("💡 Solution: Run fix_profile.py to remove lock files")
                return False
            
            # Check essential files
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
                self.logger.warning(f"⚠️ Missing essential files: {missing_files}")
                self.logger.info("💡 Solution: Profile may be corrupted, run fix_profile.py")
                return False
            
            # Check permissions
            try:
                test_file = os.path.join(profile_dir, "test_write.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                self.logger.info("✅ Profile directory is writable")
            except Exception as e:
                self.logger.error(f"❌ Profile directory is not writable: {e}")
                self.logger.info("💡 Solution: Check folder permissions or run as administrator")
                return False
            
            self.logger.info("✅ Profile appears to be healthy")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error debugging profile: {e}")
            return False
    
    def search_blinkit_item(self, query, timeout=20):
        """
        Helper function to search for items on Blinkit using the correct approach:
        1. Click fake search bar → 2. Navigate to search page → 3. Find real input → 4. Type and search
        """
        try:
            self.logger.info(f"🔍 Starting search for: {query}")

            # STEP 0: Close any popups or modals that might be blocking
            self.logger.info("🔍 STEP 0: Closing any popups/modals...")
            self.close_popups_and_modals()
            time.sleep(1)

            # STEP 1: Find and click the fake search bar (anchor tag)
            self.logger.info("🔍 STEP 1: Looking for the fake search bar...")
            
            fake_search_selectors = [
                "//a[contains(@class, 'SearchBar__Button-sc-16lps2d-4')]",  # Most specific
                "//a[contains(@class, 'SearchBar__Button')]",  # Generic
                "//a[@href='/s/']",  # By href attribute
                "//a[contains(@class, 'SearchBar') and contains(@class, 'Button')]"  # Combined
            ]
            
            fake_search_clicked = False
            for selector in fake_search_selectors:
                try:
                    fake_search_bar = WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    self.logger.info(f"✅ Found fake search bar with selector: {selector}")
                    
                    # Click the fake search bar to navigate to search page
                    fake_search_bar.click()
                    self.logger.info("✅ Successfully clicked fake search bar! Navigating to search page...")
                    fake_search_clicked = True
                    break
                    
                except Exception as e:
                    self.logger.info(f"Selector failed: {e}")
                    continue
            
            if not fake_search_clicked:
                self.logger.error("❌ Could not find or click fake search bar!")
                return False
            
            # STEP 2: Wait for navigation to search page
            self.logger.info("🔍 STEP 2: Waiting for navigation to search page...")
            time.sleep(2)  # OPTIMIZED: Reduced wait for page navigation
            
            # Check if we're on the search page
            current_url = self.driver.current_url
            self.logger.info(f"Current URL after click: {current_url}")
            
            if '/s/' not in current_url:
                self.logger.warning("⚠️ Not redirected to search page, waiting longer...")
                time.sleep(2)  # OPTIMIZED: Reduced wait
                current_url = self.driver.current_url
                self.logger.info(f"Current URL after additional wait: {current_url}")
            
            # STEP 3: Find the real search input field on the search page
            self.logger.info("🔍 STEP 3: Looking for the real search input field...")
            
            real_input_selectors = [
                "//input[@type='text']",  # Most generic
                "//input[contains(@placeholder, 'Search')]",  # By placeholder
                "//input[contains(@class, 'search')]",  # By class
                "//input[contains(@class, 'input')]",  # By class
                "//input[@name='search']",  # By name
                "//input[@id='search']"  # By ID
            ]
            
            search_input = None
            for selector in real_input_selectors:
                try:
                    search_input = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    self.logger.info(f"✅ Found real search input with selector: {selector}")
                    break
                except Exception as e:
                    self.logger.info(f"Input selector failed: {e}")
                    continue
            
            # STEP 4: If still no input found, try JavaScript approach
            if not search_input:
                self.logger.info("🔍 STEP 4: Trying JavaScript approach...")
                try:
                    search_input = self.driver.execute_script("""
                        return document.querySelector('input[type="text"]') || 
                               document.querySelector('input[placeholder*="Search"]') ||
                               document.querySelector('input[class*="search"]') ||
                               document.querySelector('input[class*="input"]') ||
                               document.querySelector('input[name="search"]') ||
                               document.querySelector('input[id="search"]');
                    """)
                    
                    if search_input:
                        self.logger.info("✅ Found search input using JavaScript")
                    else:
                        self.logger.error("❌ No search input found on search page!")
                        return False
                        
                except Exception as e:
                    self.logger.error(f"JavaScript approach failed: {e}")
                    return False
            
            # STEP 5: Interact with the search input
            if search_input:
                self.logger.info("🔍 STEP 5: Interacting with search input...")
                
                # Focus the input
                try:
                    search_input.click()
                    time.sleep(1)
                except:
                    self.driver.execute_script("arguments[0].focus();", search_input)
                    time.sleep(1)
                
                # Clear any existing text
                try:
                    search_input.clear()
                except:
                    self.driver.execute_script("arguments[0].value = '';", search_input)
                
                # Type the query
                try:
                    search_input.send_keys(query)
                    time.sleep(1)
                except:
                    self.driver.execute_script("arguments[0].value = arguments[1];", search_input, query)
                    time.sleep(1)
                
                # Press Enter to search
                try:
                    search_input.send_keys(Keys.RETURN)
                    self.logger.info("✅ Pressed Enter to search")
                except:
                    self.driver.execute_script("arguments[0].dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter'}));", search_input)
                    self.logger.info("✅ JavaScript Enter key successful")
                
                time.sleep(2)  # OPTIMIZED: Reduced wait for search results
                self.logger.info(f"✅ Successfully searched for: {query}")
                return True
                
            else:
                self.logger.error("❌ Could not find or interact with search input!")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Search failed: {e}")
            return False
    
    def search_and_add_item(self, item):
        """Search for an item using the correct Blinkit approach: click fake search bar → navigate to search page → find real input"""
        try:
            self.logger.info(f"🛒 Starting search and add process for: {item['name']}")
            self.logger.info(f"📝 Item details: {item}")
            
            # Wait for page to fully load
            self.logger.info("⏳ Waiting for page to fully load...")
            time.sleep(2)  # OPTIMIZED: Further reduced wait time
            
            # Debug: Log current page state
            self.logger.info(f"📄 Current page title: {self.driver.title}")
            self.logger.info(f"🌐 Current URL: {self.driver.current_url}")
            
            # Use the helper function to perform the search
            self.logger.info("🔍 STEP 1: Searching for item on Blinkit...")
            search_success = self.search_blinkit_item(item['name'])
            
            if not search_success:
                self.logger.error("❌ Search failed, cannot proceed with adding item to cart")
                return False
            
            self.logger.info("✅ Search completed successfully, now looking for products...")
            
            # Wait for search results to load (REDUCED from 3s to 1s)
            self.logger.info("⏳ Waiting for search results to load...")
            time.sleep(1)
            
            # OPTIMIZED: Skip debugging for faster performance
            
            # Use the OPTIMIZED cart addition function
            self.logger.info("🛒 STEP 2: Adding item to cart...")
            cart_success = self.add_first_item_to_cart(self.driver, timeout=10)
            
            if cart_success:
                self.logger.info(f"🎉 Successfully added {item['name']} to cart!")
                self.logger.info("🎯 Item search and add process completed successfully!")
                return True  # Return success to indicate item was added
            else:
                self.logger.error(f"❌ Failed to add {item['name']} to cart")
                return False
            
        except Exception as e:
            self.logger.error(f"❌ Error in search and add process: {e}")
            return False
    
    def check_alternatives(self, item_name):
        """Check for alternative products if the main item is not available"""
        try:
            # Look for alternative suggestions on the page
            alternatives = []
            
            # Try to find alternative product suggestions
            try:
                alt_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'alternative') or contains(@class, 'suggestion') or contains(@class, 'similar')]")
                for alt in alt_elements:
                    alt_text = alt.text.strip()
                    if alt_text and len(alt_text) > 3:
                        alternatives.append(alt_text)
            except:
                pass
            
            # If no alternatives found, try to find any products on the page
            if not alternatives:
                try:
                    product_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'product') or contains(@class, 'item')]")
                    for product in product_elements[:3]:  # Get first 3 products
                        product_text = product.text.strip()
                        if product_text and len(product_text) > 3:
                            alternatives.append(product_text)
                except:
                    pass
            
            return alternatives
            
        except Exception as e:
            self.logger.error(f"Error checking alternatives: {e}")
            return []
    
    def search_next_item(self, item):
        """Search for next item by clearing search bar and searching again"""
        try:
            self.logger.info(f"🛒 Starting search for next item: {item['name']}")
            
            # Find the search bar using the provided selector
            search_bar_selector = "//input[contains(@class, 'SearchBarContainer__Input')]"
            search_box = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, search_bar_selector))
            )
            
            # Clear the search bar
            self.logger.info("🧹 Clearing search bar...")
            search_box.clear()
            time.sleep(1)
            
            # Type the new item name
            self.logger.info(f"⌨️ Typing new item: {item['name']}")
            search_box.send_keys(item['name'])
            time.sleep(1)
            
            # Press Enter to search
            search_box.send_keys(Keys.ENTER)
            time.sleep(2)  # OPTIMIZED: Reduced wait for search results
            
            # Use the same cart addition logic as the main function
            self.logger.info("🛒 Adding item to cart...")
            cart_success = self.add_first_item_to_cart(self.driver, timeout=10)
            
            if cart_success:
                self.logger.info(f"🎉 Successfully added {item['name']} to cart!")
                return True
            else:
                self.logger.error(f"❌ Failed to add {item['name']} to cart")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error in search_next_item process: {e}")
            return False
    
    def place_order(self, grocery_items):
        """Main function to place the complete order"""
        try:
            if not self.setup_driver():
                return False, "Failed to setup browser automation"
            
            # Navigate to Blinkit once for the first item
            if not self.navigate_to_blinkit():
                return False, "Failed to navigate to Blinkit"
            
            # Add each item to cart using search bar
            for i, item in enumerate(grocery_items):
                self.logger.info(f"🛒 Processing item {i+1}/{len(grocery_items)}: {item['name']}")
                
                if i == 0:
                    # First item - search and add
                    if self.search_and_add_item(item):
                        self.logger.info(f"✅ Successfully added {item['name']} to cart")
                    else:
                        self.logger.error(f"❌ Failed to add {item['name']} to cart")
                        return False, f"Failed to add {item['name']} to cart"
                else:
                    # Subsequent items - clear search bar and search for next item
                    self.logger.info(f"🔄 Clearing search bar and searching for item {i+1}")
                    if self.search_next_item(item):
                        self.logger.info(f"✅ Successfully added {item['name']} to cart")
                    else:
                        self.logger.error(f"❌ Failed to add {item['name']} to cart")
                        return False, f"Failed to add {item['name']} to cart"
                
                time.sleep(2)  # Wait between items
            
            # All items added, now navigate to cart for checkout
            self.logger.info("🛒 All items added! Now navigating to cart for checkout...")
            if self.navigate_to_cart():
                self.logger.info("✅ Successfully navigated to cart - ready for checkout!")
            else:
                self.logger.warning("⚠️ Failed to navigate to cart, but proceeding with checkout attempt")
            
            # Proceed with checkout
            try:
                # Checkout process - Click "Proceed To Pay" button
                self.logger.info("🔍 Looking for 'Proceed To Pay' button on checkout page...")
                
                # Try multiple selectors for the "Proceed To Pay" button based on the element you provided
                proceed_to_pay_selectors = [
                    "//div[contains(@class, 'CheckoutStrip__CTAText') and contains(text(), 'Proceed To Pay')]",
                    "//div[contains(@class, 'CheckoutStrip__Container')]//div[contains(text(), 'Proceed To Pay')]",
                    "//div[contains(@class, 'CheckoutStrip__TitleText') and contains(text(), 'Proceed To Pay')]",
                    "//div[contains(text(), 'Proceed To Pay')]",
                    "//div[contains(@class, 'CheckoutStrip__Container')]//div[contains(@class, 'CheckoutStrip__CTAText')]",
                    "//div[contains(@class, 'CheckoutStrip__StripContainer')]//div[contains(text(), 'Proceed To Pay')]"
                ]
                
                proceed_btn = None
                for i, selector in enumerate(proceed_to_pay_selectors):
                    try:
                        self.logger.info(f"Trying 'Proceed To Pay' selector {i+1}: {selector}")
                        proceed_btn = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        self.logger.info(f"✅ Found 'Proceed To Pay' button with selector {i+1}")
                        break
                    except Exception as e:
                        self.logger.info(f"'Proceed To Pay' selector {i+1} failed: {e}")
                        continue
                
                if not proceed_btn:
                    self.logger.error("❌ Could not find 'Proceed To Pay' button!")
                    return False, "Could not proceed to payment"
                
                # Click the "Proceed To Pay" button
                proceed_btn.click()
                self.logger.info("✅ Successfully clicked 'Proceed To Pay' button - navigating to payment page")
                time.sleep(5)  # Wait for payment page to load
                
                # Verify we're on the payment page
                try:
                    payment_page_indicators = [
                        "//div[contains(text(), 'Payment') or contains(text(), 'payment')]",
                        "//div[contains(@class, 'payment') or contains(@class, 'Payment')]",
                        "//div[contains(text(), 'Select Payment') or contains(text(), 'Choose Payment')]",
                        "//div[contains(text(), 'Cash on Delivery') or contains(text(), 'COD')]"
                    ]
                    
                    payment_page_found = False
                    for selector in payment_page_indicators:
                        try:
                            element = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, selector))
                            )
                            if element.is_displayed():
                                self.logger.info("✅ Successfully navigated to payment page")
                                payment_page_found = True
                                break
                        except:
                            continue
                    
                    if not payment_page_found:
                        self.logger.warning("⚠️ May not be on payment page, but continuing...")
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ Could not verify payment page: {e}")
                
                # Now proceed with payment selection
                self.logger.info("💳 Payment method already selected (UPI) - proceeding to final payment...")
                
                # Click "Pay Now" button to complete the order
                self.logger.info("🔍 Looking for 'Pay Now' button to complete the order...")
                
                # Try multiple selectors for the "Pay Now" button based on the element you provided
                pay_now_selectors = [
                    "//div[contains(@class, 'Zpayments__PayNowButtonContainer')]//div[contains(@class, 'Zpayments__Button') and contains(text(), 'Pay Now')]",
                    "//div[contains(@class, 'Zpayments__PayNowButtonContainer')]//div[contains(text(), 'Pay Now')]",
                    "//div[contains(@class, 'Zpayments__Button') and contains(text(), 'Pay Now')]",
                    "//div[contains(text(), 'Pay Now')]",
                    "//div[contains(@class, 'Zpayments__PayNowButtonContainer')]//div[contains(@class, 'Zpayments__Button')]"
                ]
                
                pay_now_btn = None
                for i, selector in enumerate(pay_now_selectors):
                    try:
                        self.logger.info(f"Trying 'Pay Now' selector {i+1}: {selector}")
                        pay_now_btn = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        self.logger.info(f"✅ Found 'Pay Now' button with selector {i+1}")
                        break
                    except Exception as e:
                        self.logger.info(f"'Pay Now' selector {i+1} failed: {e}")
                        continue
                
                if not pay_now_btn:
                    self.logger.error("❌ Could not find 'Pay Now' button!")
                    return False, "Could not complete payment"
                
                # Click the "Pay Now" button to execute the order
                pay_now_btn.click()
                self.logger.info("✅ Successfully clicked 'Pay Now' button - executing order!")
                
                # Wait for payment processing with timeout
                start_time = time.time()
                timeout = 30  # 30 seconds timeout
                
                while time.time() - start_time < timeout:
                    time.sleep(2)
                    # Check if we've moved away from payment page
                    try:
                        current_url = self.driver.current_url
                        if 'payment' not in current_url.lower() and 'checkout' not in current_url.lower():
                            break
                    except:
                        pass
                
                self.logger.info("⏳ Payment processing completed, checking order status...")
                
                # Check for cancellation or failure indicators first
                cancellation_indicators = [
                    "//div[contains(text(), 'Order Cancelled') or contains(text(), 'Order Cancelled')]",
                    "//div[contains(text(), 'Payment Failed') or contains(text(), 'Payment Unsuccessful')]",
                    "//div[contains(text(), 'Transaction Failed') or contains(text(), 'Failed')]",
                    "//div[contains(text(), 'Error') or contains(text(), 'error')]",
                    "//div[contains(@class, 'error') or contains(@class, 'Error')]",
                    "//div[contains(text(), 'Cancelled') or contains(text(), 'cancelled')]",
                    "//div[contains(text(), 'Declined') or contains(text(), 'declined')]",
                    "//div[contains(text(), 'Insufficient') or contains(text(), 'insufficient')]"
                ]
                
                order_cancelled = False
                for selector in cancellation_indicators:
                    try:
                        element = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        if element.is_displayed():
                            self.logger.warning("⚠️ Order appears to have been cancelled or failed")
                            order_cancelled = True
                            break
                    except:
                        continue
                
                if order_cancelled:
                    return False, "Order was cancelled or payment failed - please try again"
                
                # Also check if we're back to cart (indicates order didn't go through)
                try:
                    cart_indicators = [
                        "//div[contains(text(), 'Cart') or contains(text(), 'cart')]",
                        "//div[contains(text(), 'items') and contains(text(), '₹')]"
                    ]
                    
                    back_to_cart = False
                    for selector in cart_indicators:
                        try:
                            element = self.driver.find_element(By.XPATH, selector)
                            if element.is_displayed():
                                back_to_cart = True
                                break
                        except:
                            continue
                    
                    if back_to_cart:
                        self.logger.warning("⚠️ Back to cart page - order may not have been processed")
                        return False, "Order was not processed - you were returned to cart"
                        
                except Exception as e:
                    self.logger.warning(f"⚠️ Could not check cart status: {e}")
                
                # Verify order completion
                try:
                    order_completion_indicators = [
                        "//div[contains(text(), 'Order Placed') or contains(text(), 'Order Confirmed')]",
                        "//div[contains(text(), 'Payment Successful') or contains(text(), 'Payment Complete')]",
                        "//div[contains(text(), 'Thank you') or contains(text(), 'Thank You')]",
                        "//div[contains(text(), 'Order Successfully') or contains(text(), 'Order Received')]",
                        "//div[contains(@class, 'success') or contains(@class, 'Success')]"
                    ]
                    
                    order_completed = False
                    for selector in order_completion_indicators:
                        try:
                            element = WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, selector))
                            )
                            if element.is_displayed():
                                self.logger.info("🎉 Order completed successfully!")
                                order_completed = True
                                break
                        except:
                            continue
                    
                    if order_completed:
                        self.logger.info("✅ Order executed successfully with UPI payment!")
                        return True, "Order placed successfully on Blinkit with UPI payment!"
                    else:
                        # Additional check for ambiguous states
                        self.logger.warning("⚠️ Order completion could not be verified")
                        
                        # Check if we're still on payment page (might indicate payment didn't go through)
                        try:
                            payment_page_indicators = [
                                "//div[contains(text(), 'Payment') or contains(text(), 'payment')]",
                                "//div[contains(text(), 'Select Payment') or contains(text(), 'Choose Payment')]"
                            ]
                            
                            still_on_payment = False
                            for selector in payment_page_indicators:
                                try:
                                    element = self.driver.find_element(By.XPATH, selector)
                                    if element.is_displayed():
                                        still_on_payment = True
                                        break
                                except:
                                    continue
                            
                            if still_on_payment:
                                self.logger.warning("⚠️ Still on payment page - payment may not have been processed")
                                return False, "Payment was not processed - please try again or check your payment method"
                            
                        except Exception as e:
                            self.logger.warning(f"⚠️ Could not check payment page status: {e}")
                        
                        return False, "Order completion could not be verified - please check your Blinkit account"
                
                except Exception as e:
                    self.logger.warning(f"⚠️ Could not verify order completion: {e}")
                    return False, "Order completion verification failed - please check your Blinkit account"
                
            except Exception as e:
                self.logger.warning(f"Could not proceed to checkout: {e}")
                return False, "Could not proceed to checkout"
                
        except Exception as e:
            self.logger.error(f"Order placement failed: {e}")
            return False, f"Order placement failed: {str(e)}"
        
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed")
    
    def navigate_to_cart(self):
        """Navigate to the cart page after adding items"""
        try:
            self.logger.info("🔍 Looking for cart button to proceed to checkout...")
            
            # Try multiple selectors for the cart button based on the element you provided
            cart_selectors = [
                "//div[contains(@class, 'CartButton__Container')]//div[contains(@class, 'CartButton__Button')]",
                "//div[contains(@class, 'CartButton__Container')]",
                "//div[contains(@class, 'CartButton__Button')]",
                "//div[contains(@class, 'CartButton__Text') and contains(text(), 'items')]/ancestor::div[contains(@class, 'CartButton__Button')]",
                "//div[contains(text(), 'items')]/ancestor::div[contains(@class, 'CartButton__Button')]"
            ]
            
            cart_btn = None
            for i, selector in enumerate(cart_selectors):
                try:
                    self.logger.info(f"Trying cart selector {i+1}: {selector}")
                    cart_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    self.logger.info(f"✅ Found cart button with selector {i+1}")
                    break
                except Exception as e:
                    self.logger.info(f"Cart selector {i+1} failed: {e}")
                    continue
            
            if not cart_btn:
                self.logger.error("❌ Could not find cart button!")
                return False
            
            # Click the cart button
            cart_btn.click()
            self.logger.info("✅ Successfully clicked cart button - navigating to cart")
            time.sleep(3)
            
            # Verify we're on the cart page
            try:
                # Wait for cart page to load
                cart_page_indicators = [
                    "//div[contains(text(), 'Cart') or contains(text(), 'cart')]",
                    "//div[contains(@class, 'cart') or contains(@class, 'Cart')]",
                    "//div[contains(text(), 'items') and contains(text(), '₹')]"
                ]
                
                cart_page_found = False
                for selector in cart_page_indicators:
                    try:
                        element = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        if element.is_displayed():
                            self.logger.info("✅ Successfully navigated to cart page")
                            cart_page_found = True
                            break
                    except:
                        continue
                
                if not cart_page_found:
                    self.logger.warning("⚠️ May not be on cart page, but continuing...")
                
                return True
                
            except Exception as e:
                self.logger.warning(f"⚠️ Could not verify cart page: {e}")
                return True  # Continue anyway
            
        except Exception as e:
            self.logger.error(f"❌ Failed to navigate to cart: {e}")
            return False
    
    def get_order_status(self):
        """Get current order status (placeholder for future implementation)"""
        return "Order processing"

    def debug_page_state(self):
        """Debug method to identify all available elements on the current page"""
        try:
            self.logger.info("🔍 DEBUGGING PAGE STATE...")
            self.logger.info(f"Page Title: {self.driver.title}")
            self.logger.info(f"Current URL: {self.driver.current_url}")
            
            # Find all input elements
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            self.logger.info(f"Found {len(inputs)} input elements:")
            for i, inp in enumerate(inputs):
                try:
                    input_info = {
                        'type': inp.get_attribute('type'),
                        'class': inp.get_attribute('class'),
                        'placeholder': inp.get_attribute('placeholder'),
                        'id': inp.get_attribute('id'),
                        'name': inp.get_attribute('name'),
                        'visible': inp.is_displayed(),
                        'enabled': inp.is_enabled()
                    }
                    self.logger.info(f"  Input {i+1}: {input_info}")
                except Exception as e:
                    self.logger.info(f"  Input {i+1}: Error getting info - {e}")
            
            # Find all search-related elements
            search_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'search') or contains(@class, 'Search') or contains(@placeholder, 'Search') or contains(@placeholder, 'atta')]")
            self.logger.info(f"Found {len(search_elements)} search-related elements:")
            for i, elem in enumerate(search_elements):
                try:
                    elem_info = {
                        'tag': elem.tag_name,
                        'class': elem.get_attribute('class'),
                        'placeholder': elem.get_attribute('placeholder'),
                        'text': elem.text[:100] if elem.text else '',
                        'visible': elem.is_displayed(),
                        'clickable': elem.is_enabled()
                    }
                    self.logger.info(f"  Search Element {i+1}: {elem_info}")
                except Exception as e:
                    self.logger.info(f"  Search Element {i+1}: Error getting info - {e}")
            
            # Find all buttons and clickable elements
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            links = self.driver.find_elements(By.TAG_NAME, "a")
            self.logger.info(f"Found {len(buttons)} buttons and {len(links)} links")
            
            # Check for search button specifically
            search_buttons = []
            for btn in buttons:
                try:
                    btn_text = btn.text.lower()
                    btn_class = btn.get_attribute('class') or ''
                    if any(word in btn_text for word in ['search', 'find', 'go']) or any(word in btn_class for word in ['search', 'Search']):
                        search_buttons.append(btn)
                except:
                    continue
            
            self.logger.info(f"Found {len(search_buttons)} potential search buttons:")
            for i, btn in enumerate(search_buttons):
                try:
                    btn_info = {
                        'text': btn.text,
                        'class': btn.get_attribute('class'),
                        'visible': btn.is_displayed(),
                        'clickable': btn.is_enabled()
                    }
                    self.logger.info(f"  Search Button {i+1}: {btn_info}")
                except Exception as e:
                    self.logger.info(f"  Search Button {i+1}: Error getting info - {e}")
            
            # Check page source for search-related content
            page_source = self.driver.page_source
            if 'search' in page_source.lower() or 'Search' in page_source:
                self.logger.info("✅ Page contains search-related content")
            else:
                self.logger.warning("❌ Page does not contain search-related content")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Debug page state failed: {e}")
            return False

    def debug_search_results_page(self):
        """Debug method to identify all available elements on the search results page (OPTIMIZED)"""
        try:
            self.logger.info("🔍 DEBUGGING SEARCH RESULTS PAGE (FAST)...")
            self.logger.info(f"Page Title: {self.driver.title}")
            self.logger.info(f"Current URL: {self.driver.current_url}")
            
            # Minimal wait for page to settle (REDUCED from 2s to 0.5s)
            time.sleep(0.5)
            
            # Find all div elements (potential product containers)
            divs = self.driver.find_elements(By.TAG_NAME, "div")
            self.logger.info(f"Found {len(divs)} div elements")
            
            # Look for potential product containers
            potential_products = []
            for i, div in enumerate(divs[:50]):  # Check first 50 divs
                try:
                    if div.is_displayed():
                        div_class = div.get_attribute('class') or ''
                        div_text = div.text.strip()
                        
                        # Check if this div looks like a product
                        if any(word in div_class.lower() for word in ['product', 'item', 'card', 'search', 'result']) or \
                           len(div_text) > 10:  # Has substantial text content
                            
                            potential_products.append({
                                'index': i,
                                'class': div_class,
                                'text': div_text[:100],
                                'visible': div.is_displayed(),
                                'enabled': div.is_enabled()
                            })
                except:
                    continue
            
            self.logger.info(f"Found {len(potential_products)} potential product containers:")
            for product in potential_products[:10]:  # Show first 10
                self.logger.info(f"  Product {product['index']}: {product}")
            
            # Find all buttons
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            self.logger.info(f"Found {len(buttons)} buttons:")
            for i, btn in enumerate(buttons[:20]):  # Show first 20
                try:
                    btn_info = {
                        'text': btn.text.strip(),
                        'class': btn.get_attribute('class') or '',
                        'visible': btn.is_displayed(),
                        'enabled': btn.is_enabled()
                    }
                    self.logger.info(f"  Button {i+1}: {btn_info}")
                except:
                    continue
            
            # Find all links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            self.logger.info(f"Found {len(links)} links:")
            for i, link in enumerate(links[:20]):  # Show first 20
                try:
                    link_info = {
                        'text': link.text.strip(),
                        'class': link.get_attribute('class') or '',
                        'href': link.get_attribute('href') or '',
                        'visible': link.is_displayed(),
                        'enabled': link.is_enabled()
                    }
                    self.logger.info(f"  Link {i+1}: {link_info}")
                except:
                    continue
            
            # Check page source for specific keywords
            page_source = self.driver.page_source.lower()
            keywords = ['product', 'item', 'card', 'add', 'cart', 'buy', 'search', 'result']
            for keyword in keywords:
                if keyword in page_source:
                    self.logger.info(f"✅ Page contains '{keyword}' content")
                else:
                    self.logger.info(f"❌ Page does not contain '{keyword}' content")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Debug search results page failed: {e}")
            return False

    def add_first_item_to_cart(self, driver, timeout=10):
        """
        Add the first product from Blinkit search results into the cart.
        FIXED VERSION: Uses exact CSS selector for Blinkit's Add button based on actual HTML structure.
        """
        try:
            self.logger.info("🛒 Starting add_first_item_to_cart function")
            
            # Wait for search results to fully load (small buffer as suggested)
            self.logger.info("⏳ Waiting for search results to load (2s buffer)...")
            time.sleep(2)
            
            # Check if this is a fruit (banana, apple, etc.) - click second product to avoid ads
            # We need to get the item name from the current context
            try:
                # Try to get the item name from the page title or URL
                page_title = driver.title.lower()
                current_url = driver.current_url.lower()
                
                # Comprehensive fruit list including common fruits that often have sponsored results
                fruit_keywords = [
                    'banana', 'apple', 'orange', 'mango', 'grapes', 'strawberry', 'kiwi', 'pear', 'peach', 'plum',
                    'guava', 'papaya', 'pineapple', 'watermelon', 'pomegranate', 'cherry', 'blueberry', 'raspberry',
                    'blackberry', 'cranberry', 'lemon', 'lime', 'coconut', 'avocado', 'fig', 'date', 'apricot',
                    'nectarine', 'cantaloupe', 'honeydew', 'dragon fruit', 'passion fruit', 'lychee', 'jackfruit',
                    'custard apple', 'sapodilla', 'jamun', 'chikoo', 'wood apple', 'star fruit', 'persimmon'
                ]
                
                is_fruit = any(fruit in page_title or fruit in current_url for fruit in fruit_keywords)
                
                if is_fruit:
                    self.logger.info(f"🍎 Fruit detected - selecting second product to avoid ads")
                    # For fruits, we'll try to find the second Add button
                    add_button_index = 1  # Second button (index 1)
                else:
                    self.logger.info(f"✅ Non-fruit item - selecting first product as usual")
                    add_button_index = 0  # First button (index 0)
                    
            except Exception as e:
                self.logger.info(f"⚠️ Could not determine item type, using first product: {e}")
                add_button_index = 0
            
            # Step 1: Find the Add button using multiple selectors (Blinkit changes their HTML frequently)
            self.logger.info(f"🔍 Looking for Add button #{add_button_index + 1}...")

            # Multiple selectors to try (in order of preference)
            add_button_selectors = [
                # Current Blinkit selector (as of 2024)
                "div.tw-rounded-md.tw-font-okra.tw-flex.tw-justify-center.tw-font-semibold.tw-items-center.tw-relative.tw-text-300.tw-py-2.tw-px-0.tw-gap-0\\.5.tw-min-w-\\[66px\\].tw-bg-green-050.tw-border.tw-border-base-green.tw-text-base-green",
                # Shorter variations
                "div.tw-bg-green-050.tw-text-base-green",
                "div[class*='tw-bg-green'][class*='tw-text-base-green']",
                # Generic "Add" button patterns
                "button:contains('Add')",
                "div:contains('Add')[class*='tw-']",
                # XPath fallbacks
                "//div[contains(text(), 'Add') and contains(@class, 'tw-')]",
                "//button[contains(text(), 'Add')]",
                "//div[contains(@class, 'Product')]//*[contains(text(), 'Add')]"
            ]

            add_buttons = []
            successful_selector = None

            for selector in add_button_selectors:
                try:
                    # Determine if it's CSS or XPath
                    if selector.startswith('//'):
                        elements = driver.find_elements(By.XPATH, selector)
                    else:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)

                    if elements:
                        add_buttons = elements
                        successful_selector = selector
                        self.logger.info(f"✅ Found {len(add_buttons)} Add buttons using: {selector[:50]}...")
                        break
                except Exception as e:
                    self.logger.debug(f"Selector failed: {selector[:50]}...")
                    continue

            if not add_buttons:
                self.logger.error("❌ No Add buttons found with any selector")
                return False

            try:
                # Find all Add buttons and select the appropriate one based on index
                # add_buttons already populated above
                
                if len(add_buttons) > add_button_index:
                    add_button = add_buttons[add_button_index]
                    self.logger.info(f"✅ Found {len(add_buttons)} Add buttons, using button #{add_button_index + 1}")
                else:
                    # Fallback to first button if the desired index doesn't exist
                    add_button = add_buttons[0]
                    self.logger.info(f"⚠️ Desired button #{add_button_index + 1} not found, using first button instead")
                
                # Wait for the selected button to be clickable
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(add_button)
                )
                self.logger.info(f"✅ Selected Add button is clickable")

            except Exception as e:
                self.logger.warning(f"⚠️ Add button selection failed: {e}")
                # If indexing fails, just use first button
                add_button = add_buttons[0]
                self.logger.info(f"⚠️ Using first button as fallback")
            
            # Step 2: Click the Add button immediately
            self.logger.info("🖱️ Clicking Add button...")
            try:
                # Click the button directly
                add_button.click()
                self.logger.info("✅ Successfully clicked Add button")
                
                # Wait a moment for cart update
                time.sleep(1)
                
                self.logger.info("🎉 Added first item to cart")
                return True
                
            except Exception as click_e:
                self.logger.error(f"❌ Failed to click Add button: {click_e}")
                
                # Try JavaScript click as fallback
                try:
                    driver.execute_script("arguments[0].click();", add_button)
                    self.logger.info("✅ Successfully clicked Add button using JavaScript")
                    time.sleep(1)
                    self.logger.info("🎉 Added first item to cart (JavaScript fallback)")
                    return True
                except Exception as js_e:
                    self.logger.error(f"❌ JavaScript click also failed: {js_e}")
                    return False
            
        except Exception as e:
            self.logger.error(f"❌ add_first_item_to_cart failed: {e}")
            return False
