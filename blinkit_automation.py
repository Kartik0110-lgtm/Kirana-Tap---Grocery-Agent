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
        """Navigate to Blinkit website and handle location popup"""
        try:
            self.driver.get("https://blinkit.com")
            self.logger.info("Navigated to Blinkit website")
            
            # Wait for page to load
            time.sleep(5)
            
            # Handle location popup if it appears
            try:
                # Look for the "Change Location" popup
                location_popup = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Change Location') or contains(@class, 'location-popup') or contains(@class, 'modal')]"))
                )
                self.logger.info("Location popup detected, handling it...")
                
                # Try multiple strategies to find and click "Detect my location" button
                detect_clicked = False
                
                # Strategy 1: Look for button with exact text
                try:
                    detect_location_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[text()='Detect my location' or contains(text(), 'Detect my location')]"))
                    )
                    detect_location_btn.click()
                    self.logger.info("Clicked 'Detect my location' button (Strategy 1)")
                    detect_clicked = True
                    time.sleep(3)
                except Exception as e:
                    self.logger.info(f"Strategy 1 failed: {e}")
                
                # Strategy 2: Look for green button (common styling)
                if not detect_clicked:
                    try:
                        detect_location_btn = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'green') or contains(@style, 'green') or contains(@class, 'primary') or contains(@class, 'btn-primary')]"))
                        )
                        detect_location_btn.click()
                        self.logger.info("Clicked green button (Strategy 2)")
                        detect_clicked = True
                        time.sleep(3)
                    except Exception as e:
                        self.logger.info(f"Strategy 2 failed: {e}")
                
                # Strategy 3: Look for any button in the popup that might be detect location
                if not detect_clicked:
                    try:
                        # Find all buttons in the popup
                        buttons = location_popup.find_elements(By.TAG_NAME, "button")
                        for button in buttons:
                            button_text = button.text.lower()
                            if any(word in button_text for word in ['detect', 'location', 'auto', 'current']):
                                button.click()
                                self.logger.info(f"Clicked button with text: {button.text} (Strategy 3)")
                                detect_clicked = True
                                time.sleep(3)
                                break
                    except Exception as e:
                        self.logger.info(f"Strategy 3 failed: {e}")
                
                # Strategy 4: Look for button by position (usually the first button in popup)
                if not detect_clicked:
                    try:
                        first_button = location_popup.find_element(By.TAG_NAME, "button")
                        first_button.click()
                        self.logger.info("Clicked first button in popup (Strategy 4)")
                        detect_clicked = True
                        time.sleep(3)
                    except Exception as e:
                        self.logger.info(f"Strategy 4 failed: {e}")
                
                if detect_clicked:
                    # Wait for location detection to complete
                    self.logger.info("Waiting for location detection to complete...")
                    time.sleep(8)  # Increased wait time
                else:
                    self.logger.warning("Could not click detect location button, trying to close popup...")
                    
                    # Fallback: Try to close the popup and continue
                    try:
                        close_btn = self.driver.find_element(By.XPATH, "//button[contains(@class, 'close') or contains(@aria-label, 'Close') or .//*[contains(@class, 'close')] or contains(@class, 'cross')]")
                        close_btn.click()
                        self.logger.info("Closed location popup")
                        time.sleep(2)
                    except:
                        self.logger.info("Could not close location popup, continuing...")
                
            except Exception as e:
                self.logger.info("No location popup found or already handled, continuing...")
            
            # Additional wait to ensure page is fully loaded
            time.sleep(3)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to Blinkit: {e}")
            return False
    
    def search_and_add_item(self, item):
        """Search for an item and add it to cart"""
        try:
            # Wait longer for page to fully load after location detection
            self.logger.info("Waiting for page to fully load after location detection...")
            time.sleep(8)
            
            # Debug: Log current page state
            self.logger.info(f"Current page title: {self.driver.title}")
            self.logger.info(f"Current URL: {self.driver.current_url}")
            
            # Try to refresh the page if needed to ensure search bar is accessible
            try:
                # Check if search bar is immediately visible
                search_box = self.driver.find_element(By.XPATH, "//input[@placeholder='Search' or contains(@placeholder, 'Search')]")
                self.logger.info("Search bar found immediately")
            except:
                self.logger.info("Search bar not immediately visible, trying to refresh page...")
                self.driver.refresh()
                time.sleep(5)
            
            # AGGRESSIVE SEARCH BAR DETECTION - Try everything possible
            search_box = None
            search_strategies = [
                # Strategy 1: Direct placeholder search
                "//input[@placeholder='Search' or contains(@placeholder, 'Search')]",
                
                # Strategy 2: Search by class names
                "//input[contains(@class, 'search') or contains(@class, 'Search')]",
                
                # Strategy 3: Search by data attributes
                "//input[@data-testid='search' or @data-testid='Search']",
                
                # Strategy 4: Search by aria-label
                "//input[@aria-label='Search' or contains(@aria-label, 'Search')]",
                
                # Strategy 5: Search by name attribute
                "//input[@name='search' or @name='Search' or @name='q']",
                
                # Strategy 6: Search by ID
                "//input[@id='search' or @id='Search' or @id='searchInput']",
                
                # Strategy 7: Any input that's not location-related
                "//input[@type='text' and not(contains(@placeholder, 'location') or contains(@placeholder, 'address') or contains(@placeholder, 'pincode'))]",
                
                # Strategy 8: Look for search container and find input inside
                "//div[contains(@class, 'search') or contains(@class, 'Search')]//input",
                
                # Strategy 9: Look for header search area
                "//header//input[@type='text']",
                
                # Strategy 10: Look for any input in the top section
                "//div[contains(@class, 'header') or contains(@class, 'top')]//input[@type='text']"
            ]
            
            # Try each strategy
            for i, strategy in enumerate(search_strategies):
                try:
                    self.logger.info(f"Trying search strategy {i+1}: {strategy}")
                    search_box = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, strategy))
                    )
                    self.logger.info(f"Search box found with strategy {i+1}")
                    break
                except Exception as e:
                    self.logger.info(f"Strategy {i+1} failed: {e}")
                    continue
            
            # If still no search box, try to find ANY input field and analyze it
            if not search_box:
                self.logger.info("All strategies failed, analyzing all input fields...")
                all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
                self.logger.info(f"Found {len(all_inputs)} input fields on the page")
                
                for i, input_field in enumerate(all_inputs):
                    try:
                        placeholder = input_field.get_attribute("placeholder") or ""
                        input_type = input_field.get_attribute("type") or ""
                        input_class = input_field.get_attribute("class") or ""
                        input_id = input_field.get_attribute("id") or ""
                        input_name = input_field.get_attribute("name") or ""
                        
                        self.logger.info(f"Input {i+1}: type='{input_type}', placeholder='{placeholder}', class='{input_class}', id='{input_id}', name='{input_name}'")
                        
                        # Skip location-related inputs
                        if any(word in placeholder.lower() for word in ['location', 'address', 'pincode', 'delivery']):
                            continue
                        
                        # Look for search-related inputs
                        if any(word in placeholder.lower() for word in ['search', 'Search']) or input_type == "text":
                            search_box = input_field
                            self.logger.info(f"Found search box by analyzing inputs: {placeholder}")
                            break
                    except Exception as e:
                        self.logger.info(f"Error analyzing input {i+1}: {e}")
            
            # If still no search box, try to click on the page to activate search functionality
            if not search_box:
                self.logger.info("Still no search box, trying to click on page to activate search...")
                try:
                    # Click on the center of the page to activate any hidden elements
                    actions = ActionChains(self.driver)
                    actions.move_by_offset(500, 300).click().perform()
                    time.sleep(2)
                    
                    # Try to find search box again
                    search_box = self.driver.find_element(By.XPATH, "//input[@placeholder='Search' or contains(@placeholder, 'Search')]")
                    self.logger.info("Found search box after clicking on page")
                except Exception as e:
                    self.logger.error(f"Could not find search box even after clicking: {e}")
                    return
            
            # Debug: Log search box details
            placeholder = search_box.get_attribute("placeholder") or ""
            self.logger.info(f"Using search box with placeholder: '{placeholder}'")
            
            # Try to click on the search box first to ensure it's active
            try:
                search_box.click()
                time.sleep(1)
                self.logger.info("Clicked on search box to activate it")
            except Exception as e:
                self.logger.info(f"Could not click search box: {e}")
            
            # Clear any existing text
            search_box.clear()
            time.sleep(1)
            
            # Search for the item (only the name, not quantity/unit)
            search_query = item['name']  # Just the name, e.g., "amul toned milk"
            search_box.send_keys(search_query)
            self.logger.info(f"Searching for: {search_query}")
            
            # Press Enter to search
            search_box.send_keys(Keys.ENTER)
            time.sleep(5)  # Increased wait time for search results
            
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
            
            # Navigate to cart
            try:
                cart_btn = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart-icon, .cart-button, [data-testid*='cart']"))
                )
                cart_btn.click()
                self.logger.info("Navigated to cart")
                time.sleep(3)
                
                # Checkout process
                try:
                    checkout_btn = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".checkout, .proceed, .place-order"))
                    )
                    checkout_btn.click()
                    self.logger.info("Clicked checkout")
                    time.sleep(3)
                    
                    # Select cash on delivery
                    try:
                        cod_option = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='cod'], .cod-option, [data-payment='cod']"))
                        )
                        cod_option.click()
                        self.logger.info("Selected cash on delivery")
                        time.sleep(2)
                        
                        # Final place order button
                        place_order_btn = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, ".place-order, .confirm-order, .final-checkout"))
                        )
                        place_order_btn.click()
                        self.logger.info("Order placed successfully!")
                        
                        return True, "Order placed successfully on Blinkit with cash on delivery!"
                        
                    except Exception as e:
                        self.logger.warning(f"Could not select COD: {e}")
                        return False, "Could not complete checkout process"
                        
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
