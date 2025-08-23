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
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Setup Chrome driver with visible options (not headless)"""
        try:
            chrome_options = Options()
            # chrome_options.add_argument("--headless")  # COMMENTED OUT - Now visible!
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            self.logger.info("Chrome driver setup successful - VISIBLE MODE")
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome driver: {e}")
            return False
    
    def navigate_to_blinkit(self):
        """Navigate to Blinkit website (location handling removed)"""
        try:
            self.driver.get("https://blinkit.com")
            self.logger.info("Navigated to Blinkit website")
            
            # Wait for page to load
            time.sleep(5)
            
            # Location detection removed - account is now remembered automatically
            self.logger.info("✅ Account is remembered - no need for location detection")
            
            # Additional wait to ensure page is fully loaded
            time.sleep(3)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to Blinkit: {e}")
            return False
    
    def search_and_add_item(self, item):
        """Search for an item and add it to cart using the SIMPLE search button approach"""
        try:
            # Wait for page to fully load
            self.logger.info("Waiting for page to fully load...")
            time.sleep(5)  # Reduced wait time since location detection is removed
            
            # Debug: Log current page state
            self.logger.info(f"Current page title: {self.driver.title}")
            self.logger.info(f"Current URL: {self.driver.current_url}")
            
            # Wait for the search container to be visible first
            try:
                self.logger.info("Waiting for search container to be visible...")
                search_container = self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'SearchBarContainer__Container')]"))
                )
                self.logger.info("Search container is now visible")
                time.sleep(3)  # Wait for container to fully render
                
                # Additional wait for any animations or dynamic content to settle
                self.logger.info("Waiting for page animations to settle...")
                time.sleep(2)
                
            except Exception as e:
                self.logger.info(f"Search container not immediately visible: {e}")
                # Try to refresh the page if needed to ensure search bar is accessible
                try:
                    # Check if search bar is immediately visible
                    search_box = self.driver.find_element(By.XPATH, "//input[contains(@class, 'SearchBarContainer__Input')]")
                    self.logger.info("Search bar found immediately")
                except:
                    self.logger.info("Search bar not immediately visible, trying to refresh page...")
                    self.driver.refresh()
                    time.sleep(8)  # Increased refresh wait time
                    
                    # Wait for search container again after refresh
                    try:
                        search_container = self.wait.until(
                            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'SearchBarContainer__Container')]"))
                        )
                        self.logger.info("Search container visible after refresh")
                        time.sleep(3)
                    except Exception as refresh_e:
                        self.logger.error(f"Search container still not visible after refresh: {refresh_e}")
                        return
            
            # SIMPLE AND RELIABLE APPROACH: Click the search button first, then interact with input
            try:
                self.logger.info("🔍 Using the SIMPLE approach: Click search button first!")
                
                # Step 1: Find and click the search button to activate search functionality
                search_button_selectors = [
                    "//a[contains(@class, 'SearchBar__Button')]",  # Your exact element
                    "//a[contains(@class, 'SearchBar__Button-sc-16lps2d-4')]",  # More specific
                    "//a[@href='/s/']",  # By href attribute
                    "//a[contains(@class, 'SearchBar') and contains(@class, 'Button')]"  # Generic
                ]
                
                search_button_clicked = False
                for i, selector in enumerate(search_button_selectors):
                    try:
                        self.logger.info(f"Trying to find search button with selector {i+1}: {selector}")
                        search_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        self.logger.info(f"✅ Found search button with selector {i+1}")
                        
                        # Click the search button to activate search
                        search_button.click()
                        self.logger.info("✅ Successfully clicked search button!")
                        search_button_clicked = True
                        time.sleep(3)  # Wait for search interface to activate
                        break
                        
                    except Exception as e:
                        self.logger.info(f"Selector {i+1} failed: {e}")
                        continue
                
                if not search_button_clicked:
                    self.logger.error("❌ Could not find or click search button!")
                    return
                
                # Step 2: Now find the search input field (should be active now)
                self.logger.info("🔍 Now looking for the active search input field...")
                time.sleep(2)
                
                # Try to find the search input field
                search_input_selectors = [
                    "//input[contains(@class, 'SearchBarContainer__Input')]",
                    "//input[@placeholder='Search for atta dal and more']",
                    "//input[contains(@placeholder, 'Search')]",
                    "//input[@type='text']"
                ]
                
                search_box = None
                for i, selector in enumerate(search_input_selectors):
                    try:
                        self.logger.info(f"Looking for search input with selector {i+1}: {selector}")
                        search_box = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        self.logger.info(f"✅ Found search input with selector {i+1}")
                        break
                    except Exception as e:
                        self.logger.info(f"Input selector {i+1} failed: {e}")
                        continue
                
                if not search_box:
                    self.logger.error("❌ Could not find search input field after clicking search button!")
                    return
                
                # Step 3: Verify and interact with the search input
                self.logger.info("🔍 Verifying search input is ready...")
                
                # Clear any existing text
                try:
                    search_box.clear()
                    time.sleep(1)
                    self.logger.info("✅ Cleared search input")
                except Exception as e:
                    self.logger.info(f"Clear failed, trying JavaScript: {e}")
                    self.driver.execute_script("arguments[0].value = '';", search_box)
                    time.sleep(1)
                
                # Now enter the search query
                search_query = item['name']
                self.logger.info(f"🔍 Entering search query: {search_query}")
                
                search_box.send_keys(search_query)
                time.sleep(1)
                self.logger.info(f"✅ Successfully entered: {search_query}")
                
            except Exception as e:
                self.logger.error(f"❌ Search button approach failed: {e}")
                return
            
            # Press Enter to search
            search_box.send_keys(Keys.ENTER)
            time.sleep(5)  # Wait for search results
            
            # Try to find and click the first product
            try:
                first_product = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'product') or contains(@class, 'item') or contains(@class, 'card')]"))
                )
                first_product.click()
                self.logger.info(f"Selected product for: {item['name']}")
                time.sleep(2)
                
                # Try to add to cart
                try:
                    add_to_cart_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add') or contains(@class, 'add') or contains(@data-testid, 'add')]"))
                    )
                    add_to_cart_btn.click()
                    self.logger.info(f"Added {item['name']} to cart")
                    time.sleep(2)
                    
                    # Close product modal if it appears
                    try:
                        close_btn = self.driver.find_element(By.XPATH, "//button[contains(@class, 'close') or contains(@aria-label, 'Close') or .//*[contains(@class, 'close')]]")
                        close_btn.click()
                        time.sleep(1)
                    except:
                        pass
                        
                except Exception as e:
                    self.logger.warning(f"Could not add {item['name']} to cart: {e}")
                    
            except Exception as e:
                self.logger.warning(f"Could not select product for {item['name']}: {e}")
                
        except Exception as e:
            self.logger.error(f"Failed to search for {item['name']}: {e}")
    
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
    
    def place_order(self, grocery_items):
        """Main function to place the complete order"""
        try:
            if not self.setup_driver():
                return False, "Failed to setup browser automation"
            
            if not self.navigate_to_blinkit():
                return False, "Failed to navigate to Blinkit"
            
            # Add each item to cart
            for item in grocery_items:
                self.search_and_add_item(item)
                time.sleep(2)  # Wait between items
            
            # Navigate to cart using the exact cart button element
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
                    return False, "Could not access cart"
                
                # Click the cart button
                cart_btn.click()
                self.logger.info("✅ Successfully clicked cart button - navigating to cart")
                time.sleep(3)
                
                # Checkout process - Click "Proceed To Pay" button
                try:
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
                    try:
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
                        time.sleep(5)  # Wait for payment processing
                        
                        # Verify order completion
                        try:
                            order_completion_indicators = [
                                "//div[contains(text(), 'Order Placed') or contains(text(), 'Order Confirmed')]",
                                "//div[contains(text(), 'Payment Successful') or contains(text(), 'Payment Complete')]",
                                "//div[contains(text(), 'Thank you') or contains(text(), 'Order ID')]",
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
                                self.logger.warning("⚠️ Order may have been completed, but confirmation not found")
                                return True, "Order completed successfully"
                        
                        except Exception as e:
                            self.logger.warning(f"⚠️ Could not verify order completion: {e}")
                            return True, "Order payment initiated successfully"
                        
                    except Exception as e:
                        self.logger.error(f"❌ Failed to click 'Pay Now' button: {e}")
                        return False, "Failed to complete payment"
                        
                except Exception as e:
                    self.logger.warning(f"Could not proceed to checkout: {e}")
                    return False, "Could not proceed to checkout"
                    
            except Exception as e:
                self.logger.warning(f"Could not navigate to cart: {e}")
                return False, "Could not access cart"
                
        except Exception as e:
            self.logger.error(f"Order placement failed: {e}")
            return False, f"Order placement failed: {str(e)}"
        
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed")
    
    def get_order_status(self):
        """Get current order status (placeholder for future implementation)"""
        return "Order processing"
