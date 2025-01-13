import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import time

class LinkedInAuth:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv('LINKEDIN_EMAIL')
        self.password = os.getenv('LINKEDIN_PASSWORD')
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        options = Options()
        options.add_argument('--disable-notifications')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Mask selenium automation
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def wait_and_find_element(self, by, value, timeout=10):
        """Wait for element and return it when found"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"Timeout waiting for element: {value}")
            return None
        
    def login(self):
        """Login to LinkedIn"""
        try:
            self.setup_driver()
            
            # Navigate to login page
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(2)  # Wait for page to load completely
            
            # Enter email
            email_field = self.wait_and_find_element(By.ID, "username")
            if not email_field:
                return False
            email_field.send_keys(self.email)
            time.sleep(1)
            
            # Enter password
            password_field = self.wait_and_find_element(By.ID, "password")
            if not password_field:
                return False
            password_field.send_keys(self.password)
            time.sleep(1)
            
            # Click sign in
            try:
                sign_in_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                sign_in_button.click()
            except NoSuchElementException:
                print("Could not find sign in button")
                return False
            
            # Wait for successful login
            time.sleep(5)  # Give time for login to complete
            
            # Check if we're logged in by looking for common elements
            try:
                self.driver.find_element(By.CSS_SELECTOR, "div[class*='feed-identity']")
                print("Successfully logged in to LinkedIn")
                return True
            except NoSuchElementException:
                print("Login unsuccessful - could not verify login status")
                return False
            
        except Exception as e:
            print(f"Error during login: {str(e)}")
            if self.driver:
                self.driver.save_screenshot("login_error.png")
            return False
    
    def get_company_page(self, company_name):
        """Navigate to company page and get information"""
        try:
            # Search for company
            search_url = f"https://www.linkedin.com/company/{company_name.lower().replace(' ', '-')}/about/"
            self.driver.get(search_url)
            time.sleep(3)  # Wait for page load
            
            # Extract company information
            company_info = {
                'recent_news': None,
                'specialties': None,
                'industry': None,
                'about': None
            }
            
            try:
                # Try different selectors for company information
                selectors = {
                    'specialties': ["div[class*='specialties']", "section[class*='specialties']"],
                    'industry': ["div[class*='industry']", "section[class*='industry']"],
                    'about': ["div[class*='description']", "section[class*='description']"]
                }
                
                for field, selector_list in selectors.items():
                    for selector in selector_list:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            company_info[field] = elements[0].text.strip()
                            break
                
            except Exception as e:
                print(f"Error extracting company info: {str(e)}")
            
            return company_info
            
        except Exception as e:
            print(f"Error accessing company page: {str(e)}")
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit() 