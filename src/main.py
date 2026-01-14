"""Main orchestration script for LinkedIn Auto-Posting Bot"""
import os
import sys
import logging
import argparse
from datetime import datetime
from dotenv import load_dotenv
import yaml

from google_drive_manager import GoogleDriveManager
from linkedin_poster import LinkedInPoster
from post_rotator import PostRotator


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


def load_config(config_path: str = "config/config.yaml"):
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load config from {config_path}: {e}")
        raise


def main():
    """Main execution function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='LinkedIn Auto-Posting Bot with Smart Rotation'
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
        '--config',
        default='config/config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset rotation state and start fresh'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(debug=args.debug)
    logger.info("=" * 60)
    logger.info("LinkedIn Auto-Posting Bot Started")
    logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Dry Run Mode: {args.dry_run}")
    logger.info("=" * 60)
    
    try:
        # Load environment variables
        load_dotenv('config/.env')
        logger.info("Environment variables loaded")
        
        # Load configuration
        config = load_config(args.config)
        logger.info(f"Configuration loaded from {args.config}")
        
        # Get credentials from environment
        linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        linkedin_person_id = os.getenv('LINKEDIN_PERSON_ID')
        google_creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        google_folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        
        # Validate credentials
        missing_vars = []
        if not linkedin_token:
            missing_vars.append('LINKEDIN_ACCESS_TOKEN')
        if not linkedin_person_id:
            missing_vars.append('LINKEDIN_PERSON_ID')
        if not google_creds_path:
            missing_vars.append('GOOGLE_CREDENTIALS_PATH')
        if not google_folder_id:
            missing_vars.append('GOOGLE_DRIVE_FOLDER_ID')
        
        if missing_vars:
            logger.error("Missing required environment variables:")
            for var in missing_vars:
                logger.error(f"  - {var}")
            return 1
        
        # Initialize components
        logger.info("Initializing components...")
        
        drive_manager = GoogleDriveManager(
            credentials_path=google_creds_path,
            folder_id=google_folder_id
        )
        
        linkedin_poster = LinkedInPoster(
            access_token=linkedin_token,
            person_id=linkedin_person_id
        )
        
        post_rotator = PostRotator(
            state_file=config.get('rotation_state_file', 'rotation_state.json')
        )
        
        # Reset rotation if requested
        if args.reset:
            logger.info("Resetting rotation state...")
            post_rotator.reset()
            logger.info("Rotation state reset complete")
            return 0
        
        # Validate LinkedIn token
        if not args.dry_run:
            logger.info("Validating LinkedIn access token...")
            if not linkedin_poster.validate_token():
                logger.error("LinkedIn token validation failed")
                return 1
        
        # Get available posts from Google Drive
        logger.info("Fetching posts from Google Drive...")
        available_posts = drive_manager.list_posts()
        
        if not available_posts:
            logger.warning("No posts found in Google Drive folder")
            return 1
        
        logger.info(f"Found {len(available_posts)} posts")
        
        # Get rotation state summary
        state_summary = post_rotator.get_state_summary()
        logger.info(f"Rotation state: {state_summary['used_posts_count']} posts already used")
        
        # Select next post
        logger.info("Selecting next post to publish...")
        next_post = post_rotator.get_next_post(available_posts)
        
        if not next_post:
            logger.error("Failed to select next post")
            return 1
        
        logger.info(f"Selected post: {next_post['name']}")
        
        # Download post content
        logger.info("Downloading post content...")
        content = drive_manager.get_post_content(next_post['id'])
        logger.info(f"Post content length: {len(content)} characters")
        
        # Post to LinkedIn
        if args.dry_run:
            logger.info("=" * 60)
            logger.info("DRY RUN MODE - Would post the following:")
            logger.info("-" * 60)
            logger.info(content)
            logger.info("-" * 60)
            logger.info("Post NOT published (dry run mode)")
            logger.info("=" * 60)
        else:
            logger.info("Publishing to LinkedIn...")
            result = linkedin_poster.post_text(content)
            logger.info(f"Post published successfully! Post ID: {result['post_id']}")
            logger.info("=" * 60)
            logger.info("SUCCESS - Post published to LinkedIn")
            logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"FATAL ERROR: {e}", exc_info=True)
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
