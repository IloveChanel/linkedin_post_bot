#!/usr/bin/env python3
"""
LinkedIn Automation Bot - Selenium Edition
Automatically posACts to LinkedIn from Google Drive or local posts folder
"""

import os
import sys
import time
import random
import logging
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

from linkedin_poster import LinkedInPoster
from post_fetcher import PostFetcher

# Configure logging
logging.basicConfig(
    level=logging. INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def is_manual_run():
    """
    Detect if this is a manual workflow_dispatch run vs scheduled run
    GitHub Actions sets GITHUB_EVENT_NAME environment variable
    """
    event_name = os.getenv('GITHUB_EVENT_NAME', 'schedule')
    return event_name == 'workflow_dispatch'

def main(dry_run=False, headless=True):
    """Main execution function"""
    
    logger.info("=" * 70)
    logger.info("🤖 LinkedIn Automation Bot - Selenium Edition")
    logger.info(f"⏰ Time: {datetime. now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"🧪 Dry Run Mode: {dry_run}")
    logger.info(f"🎭 Headless Mode: {headless}")
    manual_run = is_manual_run()
    logger.info(f"🎯 Run Type: {'MANUAL (Testing)' if manual_run else 'SCHEDULED (Automated)'}")
    logger.info("=" * 70)
    
    # Add random delay ONLY for scheduled runs (not manual testing)
    if not manual_run:
        delay_minutes = random.randint(0, 59)
        delay_seconds = delay_minutes * 60
        target_time = datetime.now().timestamp() + delay_seconds
        target_datetime = datetime.fromtimestamp(target_time)
        
        logger.info(f"Adding random delay: {delay_minutes} minutes ({delay_seconds} seconds)")
        logger.info(f"Will start posting at: {target_datetime. strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(delay_seconds)
        logger.info("Random delay complete - starting bot...")
    else:
        logger.info("⚡ MANUAL RUN - Skipping random delay for testing!")
    
    # Load environment variables
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)
    
    # Validate environment variables
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    
    # Google Drive is optional for manual runs
    google_folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    google_credentials = os.getenv('GOOGLE_CREDENTIALS')
    
    if linkedin_email and linkedin_password:
        logger. info("✅ Environment variables loaded")
    else:
        logger. error("❌ Missing required environment variables:")
        if not linkedin_email:
            logger.error("   - LINKEDIN_EMAIL")
        if not linkedin_password:
            logger.error("   - LINKEDIN_PASSWORD")
        return False
    
    # Determine post source based on run type
    use_google_drive = False
    if not manual_run and google_folder_id and google_credentials:
        use_google_drive = True
        logger.info("📁 Will try Google Drive first (scheduled run)")
    else:
        if manual_run:
            logger. info("📂 Using LOCAL posts folder (manual run)")
        else:
            logger.info("⚠️  Google Drive not configured - using LOCAL posts folder")
    
    try:
        # Initialize post fetcher
        logger.info("📥 Initializing post fetcher...")
        fetcher = PostFetcher(use_local_fallback=True)
        
        # Fetch post content
        logger.info("📄 Fetching post content...")
        if use_google_drive:
            post_content = fetcher.get_next_post_from_drive()
            if not post_content:
                logger. warning("⚠️  No post from Google Drive, trying local folder...")
                post_content = fetcher.get_next_post_from_local()
        else:
            post_content = fetcher.get_next_post_from_local()
        
        if not post_content:
            logger.error("❌ No post content available!")
            return False
        
        logger.info(f"✅ Post content retrieved ({len(post_content)} characters)")
        logger.info(f"Preview: {post_content[:100]}...")
        
        if dry_run:
            logger.info("🧪 DRY RUN - Would post the following:")
            logger.info("-" * 70)
            logger.info(post_content)
            logger.info("-" * 70)
            logger.info("✅ Dry run complete!")
            return True
        
        # Initialize LinkedIn poster
        logger.info("🌐 Initializing LinkedIn poster...")
        poster = LinkedInPoster(headless=headless)
        
        # Post to LinkedIn
        logger.info("🚀 Posting to LinkedIn...")
        success = poster.post(post_content)
        
        if success: 
            logger.info("✅ Successfully posted to LinkedIn!")
            logger. info(f"📊 Post length: {len(post_content)} characters")
            return True
        else:
            logger.error("❌ Failed to post to LinkedIn")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error in main execution: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='LinkedIn Automation Bot')
    parser.add_argument('--dry-run', action='store_true', help='Run in dry-run mode (no actual posting)')
    parser.add_argument('--headless', action='store_true', default=True, help='Run browser in headless mode')
    parser.add_argument('--visible', action='store_true', help='Run browser in visible mode (for debugging)')
    
    args = parser.parse_args()
    
    # If --visible is set, override --headless
    headless = not args.visible if args.visible else args.headless
    
    success = main(dry_run=args.dry_run, headless=headless)
    sys.exit(0 if success else 1)
