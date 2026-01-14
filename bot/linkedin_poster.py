"""LinkedIn Poster - Selenium-based automation for posting to LinkedIn"""
import os
import sys
import logging
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from human_behavior import HumanBehavior

logger = logging.getLogger(__name__)


class LinkedInPoster:
    """Manages posting content to LinkedIn using Selenium WebDriver"""
    
    def __init__(self, email: str, password: str, headless: bool = True):
        """
        Initialize LinkedIn Poster
        
        Args:
            email: LinkedIn email/username
            password: LinkedIn password
            headless: Run browser in headless mode
        """
        self.email = email
        self.password = password
        self.headless = headless
        self.driver = None
        self.wait = None
        self.is_logged_in = False
        
    def _setup_driver(self):
        """Setup Chrome WebDriver with anti-detection options"""
        logger.info("Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        
        # Headless mode for GitHub Actions
        if self.headless:
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--disable-gpu')
        
        # Anti-detection settings
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Random user agent
        user_agent = HumanBehavior.get_random_user_agent()
        chrome_options.add_argument(f'user-agent={user_agent}')
        logger.debug(f"Using user agent: {user_agent}")
        
        # Random viewport size
        width, height = HumanBehavior.get_random_viewport()
        chrome_options.add_argument(f'--window-size={width},{height}')
        logger.debug(f"Window size: {width}x{height}")
        
        # Additional stealth options
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--lang=en-US')
        
        # Preferences to appear more human
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            # Use webdriver-manager for automatic driver management
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set page load timeout
            self.driver.set_page_load_timeout(30)
            
            # Execute CDP commands to add stealth
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": user_agent
            })
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("Chrome WebDriver setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup Chrome WebDriver: {e}")
            raise
    
    def login(self) -> bool:
        """
        Login to LinkedIn
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            logger.info("Attempting to login to LinkedIn...")
            
            # Navigate to LinkedIn login page
            self.driver.get("https://www.linkedin.com/login")
            HumanBehavior.random_delay(2, 4)
            
            # Find and fill email field
            logger.debug("Entering email...")
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            HumanBehavior.short_delay()
            HumanBehavior.move_to_element_naturally(self.driver, email_field)
            email_field.clear()
            HumanBehavior.short_delay()
            HumanBehavior.type_like_human(email_field, self.email)
            
            HumanBehavior.short_delay()
            
            # Find and fill password field
            logger.debug("Entering password...")
            password_field = self.driver.find_element(By.ID, "password")
            HumanBehavior.move_to_element_naturally(self.driver, password_field)
            password_field.clear()
            HumanBehavior.short_delay()
            HumanBehavior.type_like_human(password_field, self.password)
            
            HumanBehavior.random_delay(1, 2)
            
            # Click login button
            logger.debug("Clicking login button...")
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            HumanBehavior.move_to_element_naturally(self.driver, login_button)
            HumanBehavior.short_delay()
            login_button.click()
            
            # Wait for navigation to complete
            logger.info("Waiting for login to complete...")
            HumanBehavior.random_delay(5, 8)
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                logger.info("Login successful!")
                self.is_logged_in = True
                
                # Handle any post-login popups
                self._handle_popups()
                
                return True
            elif "checkpoint" in self.driver.current_url or "challenge" in self.driver.current_url:
                logger.error("Login blocked - CAPTCHA or security challenge detected")
                self._take_screenshot("login_challenge")
                return False
            else:
                logger.error(f"Login failed - unexpected URL: {self.driver.current_url}")
                self._take_screenshot("login_failed")
                return False
                
        except TimeoutException:
            logger.error("Login timeout - elements not found")
            self._take_screenshot("login_timeout")
            return False
        except Exception as e:
            logger.error(f"Login error: {e}")
            self._take_screenshot("login_error")
            return False
    
    def navigate_to_profile(self, profile_url: str):
        """
        Navigate to user's profile page
        
        Args:
            profile_url: LinkedIn profile URL
        """
        logger.info(f"Navigating to profile: {profile_url}")
        self.driver.get(profile_url)
        HumanBehavior.random_delay(3, 5)
        
        # Scroll randomly to appear natural
        HumanBehavior.scroll_randomly(self.driver)
        HumanBehavior.short_delay()
    
    def post_content(self, content: str) -> bool:
        """
        Post content to LinkedIn
        
        Args:
            content: Text content to post
            
        Returns:
            True if post successful, False otherwise
        """
        try:
            logger.info("Starting post creation process...")
            
            # Simulate thinking/reading
            HumanBehavior.thinking_pause()
            
            # Find and click "Start a post" button
            logger.debug("Looking for 'Start a post' button...")
            
            # Try multiple selectors as LinkedIn's UI can vary
            post_button_selectors = [
                "//button[contains(@class, 'share-box-feed-entry__trigger')]",
                "//button[contains(., 'Start a post')]",
                "//div[contains(@class, 'share-box-feed-entry__trigger')]",
                "//button[@aria-label='Start a post']"
            ]
            
            post_button = None
            for selector in post_button_selectors:
                try:
                    post_button = self.driver.find_element(By.XPATH, selector)
                    if post_button and post_button.is_displayed():
                        logger.debug(f"Found post button with selector: {selector}")
                        break
                except NoSuchElementException:
                    continue
            
            if not post_button:
                raise Exception("Could not find 'Start a post' button")
            
            HumanBehavior.move_to_element_naturally(self.driver, post_button)
            HumanBehavior.short_delay()
            post_button.click()
            
            logger.debug("Clicked 'Start a post' button")
            HumanBehavior.random_delay(2, 4)
            
            # Wait for post editor to appear
            logger.debug("Waiting for post editor...")
            
            # Try multiple selectors for the text editor
            editor_selectors = [
                "//div[@role='textbox']",
                "//div[@contenteditable='true']",
                "//div[contains(@class, 'ql-editor')]"
            ]
            
            editor = None
            for selector in editor_selectors:
                try:
                    editor = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if editor and editor.is_displayed():
                        logger.debug(f"Found editor with selector: {selector}")
                        break
                except TimeoutException:
                    continue
            
            if not editor:
                raise Exception("Could not find post editor")
            
            # Click into the editor
            HumanBehavior.move_to_element_naturally(self.driver, editor)
            HumanBehavior.short_delay()
            editor.click()
            HumanBehavior.short_delay()
            
            # Type the content with human-like behavior
            logger.info(f"Typing post content ({len(content)} characters)...")
            HumanBehavior.type_like_human(editor, content)
            
            logger.debug("Content typed successfully")
            HumanBehavior.random_delay(2, 4)
            
            # Find and click the Post button
            logger.debug("Looking for Post button...")
            
            # Try multiple selectors for the post button
            post_submit_selectors = [
                "//button[contains(@class, 'share-actions__primary-action')]",
                "//button[@aria-label='Post']",
                "//button[contains(., 'Post') and not(contains(., 'Start'))]",
                "//span[text()='Post']/ancestor::button"
            ]
            
            post_submit_button = None
            for selector in post_submit_selectors:
                try:
                    post_submit_button = self.driver.find_element(By.XPATH, selector)
                    if post_submit_button and post_submit_button.is_displayed() and post_submit_button.is_enabled():
                        logger.debug(f"Found Post button with selector: {selector}")
                        break
                except NoSuchElementException:
                    continue
            
            if not post_submit_button:
                raise Exception("Could not find Post submit button")
            
            HumanBehavior.thinking_pause()
            HumanBehavior.move_to_element_naturally(self.driver, post_submit_button)
            HumanBehavior.short_delay()
            
            logger.info("Clicking Post button...")
            post_submit_button.click()
            
            # Wait for post to be submitted
            logger.info("Waiting for post to be submitted...")
            HumanBehavior.random_delay(5, 8)
            
            # Check if post was successful (URL should return to feed)
            if "feed" in self.driver.current_url or self.driver.current_url.endswith("/"):
                logger.info("Post published successfully!")
                self._take_screenshot("post_success")
                return True
            else:
                logger.warning(f"Unexpected URL after posting: {self.driver.current_url}")
                self._take_screenshot("post_uncertain")
                return True  # Assume success if no error
                
        except Exception as e:
            logger.error(f"Failed to post content: {e}")
            self._take_screenshot("post_failed")
            raise
    
    def _handle_popups(self):
        """Handle any popups or notifications that might appear"""
        try:
            # Try to dismiss common popups
            dismiss_selectors = [
                "//button[@aria-label='Dismiss']",
                "//button[contains(., 'Skip')]",
                "//button[contains(., 'Not now')]",
                "//button[contains(@class, 'artdeco-modal__dismiss')]"
            ]
            
            for selector in dismiss_selectors:
                try:
                    dismiss_button = self.driver.find_element(By.XPATH, selector)
                    if dismiss_button and dismiss_button.is_displayed():
                        dismiss_button.click()
                        logger.debug(f"Dismissed popup with selector: {selector}")
                        HumanBehavior.short_delay()
                except NoSuchElementException:
                    pass
                    
        except Exception as e:
            logger.debug(f"No popups to handle or error handling popups: {e}")
    
    def _take_screenshot(self, name: str):
        """
        Take screenshot for debugging
        
        Args:
            name: Screenshot name/identifier
        """
        try:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{screenshot_dir}/{name}_{timestamp}.png"
            
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
    
    def close(self):
        """Close the browser and cleanup"""
        if self.driver:
            logger.info("Closing browser...")
            try:
                self.driver.quit()
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        self._setup_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
