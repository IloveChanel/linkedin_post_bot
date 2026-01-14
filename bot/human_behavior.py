"""Human Behavior Simulation - Anti-Detection Utilities"""
import random
import time
import logging
from typing import List

logger = logging.getLogger(__name__)


class HumanBehavior:
    """Simulates human-like behavior to avoid bot detection"""
    
    # Common user agents for rotation
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]
    
    @staticmethod
    def random_delay(min_seconds: float = 2.0, max_seconds: float = 8.0):
        """
        Add random delay to simulate human behavior
        
        Args:
            min_seconds: Minimum delay in seconds
            max_seconds: Maximum delay in seconds
        """
        delay = random.uniform(min_seconds, max_seconds)
        logger.debug(f"Human delay: {delay:.2f} seconds")
        time.sleep(delay)
    
    @staticmethod
    def typing_delay():
        """Random delay between keystrokes (50-200ms)"""
        delay = random.uniform(0.05, 0.2)
        time.sleep(delay)
    
    @staticmethod
    def thinking_pause():
        """Simulate 'thinking' pause (3-5 seconds)"""
        delay = random.uniform(3.0, 5.0)
        logger.debug(f"Thinking pause: {delay:.2f} seconds")
        time.sleep(delay)
    
    @staticmethod
    def short_delay():
        """Short random delay (0.5-1.5 seconds)"""
        delay = random.uniform(0.5, 1.5)
        time.sleep(delay)
    
    @staticmethod
    def get_random_user_agent() -> str:
        """Get random user agent string"""
        return random.choice(HumanBehavior.USER_AGENTS)
    
    @staticmethod
    def get_random_viewport() -> tuple:
        """
        Get random viewport size
        
        Returns:
            Tuple of (width, height)
        """
        # Common desktop resolutions with slight variations
        base_widths = [1920, 1366, 1536, 1440, 1280]
        base_heights = [1080, 768, 864, 900, 720]
        
        width = random.choice(base_widths) + random.randint(-10, 10)
        height = random.choice(base_heights) + random.randint(-10, 10)
        
        return (width, height)
    
    @staticmethod
    def type_like_human(element, text: str):
        """
        Type text with human-like delays
        
        Args:
            element: Selenium WebElement to type into
            text: Text to type
        """
        logger.debug(f"Typing text with human-like speed (length: {len(text)})")
        
        # Type character by character with random delays
        for char in text:
            element.send_keys(char)
            HumanBehavior.typing_delay()
        
        logger.debug("Finished typing")
    
    @staticmethod
    def scroll_randomly(driver):
        """
        Perform random scroll behavior
        
        Args:
            driver: Selenium WebDriver instance
        """
        scroll_amount = random.randint(100, 400)
        direction = random.choice(['down', 'up'])
        
        if direction == 'down':
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            logger.debug(f"Scrolled down {scroll_amount}px")
        else:
            driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
            logger.debug(f"Scrolled up {scroll_amount}px")
        
        HumanBehavior.short_delay()
    
    @staticmethod
    def move_to_element_naturally(driver, element):
        """
        Move to element with human-like behavior
        
        Args:
            driver: Selenium WebDriver instance
            element: Target element
        """
        # Scroll element into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        HumanBehavior.short_delay()
        
        # Add slight random offset to mouse position
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        
        # Note: ActionChains for mouse movement can be detected
        # Simple scroll-into-view is often more natural
        logger.debug("Moved to element naturally")
    
    @staticmethod
    def get_random_minute_offset() -> int:
        """
        Get random minute offset (0-59) for scheduling randomization
        
        Returns:
            Random minute offset
        """
        return random.randint(0, 59)
