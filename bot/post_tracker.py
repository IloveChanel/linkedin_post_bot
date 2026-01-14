"""Post Tracker - Manages post rotation state"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PostTracker:
    """Manages post rotation state and determines next post to publish"""
    
    def __init__(self, state_file: str = "posted.json"):
        """
        Initialize the post tracker
        
        Args:
            state_file: Path to JSON file storing rotation state
        """
        self.state_file = state_file
        self.state = self._load_state()
        
    def _load_state(self) -> Dict:
        """Load rotation state from file"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load state file: {e}. Starting fresh.")
                return {'posted_ids': [], 'last_posted': None}
        return {'posted_ids': [], 'last_posted': None}
    
    def _save_state(self):
        """Save rotation state to file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            logger.debug(f"State saved to {self.state_file}")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def get_next_post(self, available_posts: List[Dict]) -> Optional[Dict]:
        """
        Get the next post to publish based on rotation logic
        
        Logic:
        1. Sort posts by creation date (newest first)
        2. Find first unposted post
        3. If all are posted, reset and start over
        
        Args:
            available_posts: List of post dictionaries with 'id', 'name', 'createdTime'
            
        Returns:
            Next post dictionary or None if no posts available
        """
        if not available_posts:
            logger.warning("No posts available for rotation")
            return None
        
        # Sort posts by creation time (newest first)
        sorted_posts = sorted(
            available_posts, 
            key=lambda x: x.get('createdTime', ''), 
            reverse=True
        )
        
        # Get list of post IDs in order
        post_ids = [post['id'] for post in sorted_posts]
        
        # Get posted posts from state
        posted_ids = self.state.get('posted_ids', [])
        
        # If all posts have been posted, reset
        if set(post_ids).issubset(set(posted_ids)) and len(posted_ids) > 0:
            logger.info("All posts have been used. Resetting rotation.")
            posted_ids = []
            self.state['posted_ids'] = []
        
        # Find next unposted post
        for post in sorted_posts:
            if post['id'] not in posted_ids:
                logger.info(f"Selected next post: {post['name']}")
                return post
        
        logger.warning("No unposted posts found")
        return None
    
    def mark_as_posted(self, post_id: str, post_name: str = None):
        """
        Mark a post as posted
        
        Args:
            post_id: Google Drive file ID
            post_name: Optional post name for logging
        """
        posted_ids = self.state.get('posted_ids', [])
        if post_id not in posted_ids:
            posted_ids.append(post_id)
            self.state['posted_ids'] = posted_ids
            self.state['last_posted'] = {
                'id': post_id,
                'name': post_name,
                'timestamp': datetime.utcnow().isoformat()
            }
            self._save_state()
            logger.info(f"Marked post as posted: {post_name or post_id}")
    
    def reset(self):
        """Reset rotation state"""
        self.state = {'posted_ids': [], 'last_posted': None}
        self._save_state()
        logger.info("Rotation state reset")
    
    def get_state_summary(self) -> Dict:
        """Get summary of current rotation state"""
        return {
            'posted_count': len(self.state.get('posted_ids', [])),
            'last_posted': self.state.get('last_posted')
        }
