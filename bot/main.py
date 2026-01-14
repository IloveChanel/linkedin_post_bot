"""Main orchestration script for LinkedIn Automation Bot"""
import os
import sys
import logging
import argparse
import time
import random
from datetime import datetime
from dotenv import load_dotenv

# Add bot directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bot.linkedin_poster import LinkedInPoster
from bot.drive_reader import DriveReader
from bot.post_tracker import PostTracker
from bot.human_behavior import HumanBehavior


def setup_logging(debug: bool = False):
    """Configure logging for the application"""
    level = logging.DEBUG if debug else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)


def add_random_delay():
    """Add random delay at start (0-59 minutes) for scheduling randomization"""
    random_minutes = HumanBehavior.get_random_minute_offset()
    delay_seconds = random_minutes * 60
    
    logger = logging.getLogger(__name__)
    logger.info(f"Adding random delay: {random_minutes} minutes ({delay_seconds} seconds)")
    logger.info(f"Will start posting at: {datetime.now()}")
    
    time.sleep(delay_seconds)
    logger.info("Random delay complete - starting bot...")


def main():
    """Main execution function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='LinkedIn Automation Bot with Selenium'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without actually posting to LinkedIn'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '--no-random-delay',
        action='store_true',
        help='Skip random delay (for testing)'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        default=True,
        help='Run browser in headless mode (default: True)'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset post rotation state'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(debug=args.debug)
    logger.info("=" * 70)
    logger.info("🤖 LinkedIn Automation Bot - Selenium Edition")
    logger.info(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    logger.info(f"🧪 Dry Run Mode: {args.dry_run}")
    logger.info(f"🎭 Headless Mode: {args.headless}")
    logger.info("=" * 70)
    
    try:
        # Add random delay for scheduling (unless disabled)
        if not args.no_random_delay and not args.dry_run and not args.reset:
            add_random_delay()
        
        # Load environment variables
        load_dotenv('.env')
        load_dotenv('config/.env')
        logger.info("✅ Environment variables loaded")
        
        # Get credentials from environment
        linkedin_email = os.getenv('LINKEDIN_EMAIL')
        linkedin_password = os.getenv('LINKEDIN_PASSWORD')
        google_credentials = os.getenv('GOOGLE_CREDENTIALS')  # Base64 encoded JSON
        google_credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        google_folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        profile_url = os.getenv('LINKEDIN_PROFILE_URL', 'https://www.linkedin.com/in/michelle-vance-ai-engineer/')
        
        # Validate credentials
        missing_vars = []
        if not linkedin_email:
            missing_vars.append('LINKEDIN_EMAIL')
        if not linkedin_password:
            missing_vars.append('LINKEDIN_PASSWORD')
        if not google_folder_id:
            missing_vars.append('GOOGLE_DRIVE_FOLDER_ID')
        if not google_credentials and not google_credentials_path:
            missing_vars.append('GOOGLE_CREDENTIALS or GOOGLE_CREDENTIALS_PATH')
        
        if missing_vars:
            logger.error("❌ Missing required environment variables:")
            for var in missing_vars:
                logger.error(f"   - {var}")
            return 1
        
        logger.info("✅ All required credentials found")
        
        # Initialize components
        logger.info("🔧 Initializing components...")
        
        # Initialize Google Drive reader
        drive_reader = DriveReader(
            credentials_json=google_credentials,
            credentials_path=google_credentials_path,
            folder_id=google_folder_id
        )
        logger.info("✅ Google Drive reader initialized")
        
        # Initialize post tracker
        post_tracker = PostTracker(state_file='posted.json')
        logger.info("✅ Post tracker initialized")
        
        # Reset rotation if requested
        if args.reset:
            logger.info("🔄 Resetting post rotation state...")
            post_tracker.reset()
            logger.info("✅ Rotation state reset complete")
            return 0
        
        # Get available posts from Google Drive
        logger.info("📥 Fetching posts from Google Drive...")
        available_posts = drive_reader.list_posts()
        
        if not available_posts:
            logger.warning("⚠️  No posts found in Google Drive folder")
            return 1
        
        logger.info(f"✅ Found {len(available_posts)} posts in Google Drive")
        
        # Get rotation state summary
        state_summary = post_tracker.get_state_summary()
        logger.info(f"📊 Rotation state: {state_summary['posted_count']} posts already used")
        
        # Select next post
        logger.info("🎯 Selecting next post to publish...")
        next_post = post_tracker.get_next_post(available_posts)
        
        if not next_post:
            logger.error("❌ Failed to select next post")
            return 1
        
        logger.info(f"✅ Selected post: {next_post['name']}")
        
        # Download post content
        logger.info("📄 Downloading post content...")
        content = drive_reader.get_post_content(next_post['id'])
        logger.info(f"✅ Post content loaded ({len(content)} characters)")
        
        # Post to LinkedIn
        if args.dry_run:
            logger.info("=" * 70)
            logger.info("🧪 DRY RUN MODE - Would post the following:")
            logger.info("-" * 70)
            logger.info(content[:500] + ("..." if len(content) > 500 else ""))
            logger.info("-" * 70)
            logger.info("✅ Post NOT published (dry run mode)")
            logger.info("=" * 70)
            
            # Still mark as posted in dry run (for testing rotation)
            post_tracker.mark_as_posted(next_post['id'], next_post['name'])
        else:
            logger.info("🚀 Starting LinkedIn posting process...")
            
            # Use context manager for automatic cleanup
            with LinkedInPoster(linkedin_email, linkedin_password, headless=args.headless) as poster:
                # Login to LinkedIn
                logger.info("🔐 Logging into LinkedIn...")
                if not poster.login():
                    logger.error("❌ Failed to login to LinkedIn")
                    return 1
                
                logger.info("✅ Successfully logged into LinkedIn")
                
                # Navigate to profile
                logger.info(f"🧭 Navigating to profile: {profile_url}")
                poster.navigate_to_profile(profile_url)
                logger.info("✅ On profile page")
                
                # Post content
                logger.info("✍️  Posting content to LinkedIn...")
                if poster.post_content(content):
                    logger.info("✅ Content posted successfully!")
                    
                    # Mark as posted
                    post_tracker.mark_as_posted(next_post['id'], next_post['name'])
                    logger.info("✅ Post marked as used in rotation")
                    
                    logger.info("=" * 70)
                    logger.info("🎉 SUCCESS - Post published to LinkedIn!")
                    logger.info(f"📝 Post: {next_post['name']}")
                    logger.info(f"📊 Total posts used: {state_summary['posted_count'] + 1}")
                    logger.info("=" * 70)
                else:
                    logger.error("❌ Failed to post content")
                    return 1
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n⚠️  Bot interrupted by user")
        return 1
    except Exception as e:
        logger.error("=" * 70)
        logger.error(f"💥 FATAL ERROR: {e}", exc_info=args.debug)
        logger.error("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
