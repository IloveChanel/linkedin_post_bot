"""Post Rotator - Manages smart rotation of posts (newest to oldest, then loops)"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PostRotator:
    """Manages post rotation state and determines next post to publish"""
    
    def __init__(self, state_file: str = "rotation_state.json"):
        """
        Initialize the post rotator
        
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
                return {}
        return {}
    
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
        Get the next post to publish based on smart rotation logic
        
        Logic:
        1. Sort posts by creation date (newest first)
        2. If no posts have been used, start with newest
        3. Otherwise, continue through the list
        4. When all posts are used, reset and start over
        
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
        
        # Get used posts from state
        used_posts = self.state.get('used_posts', [])
        
        # If all posts have been used, reset
        # Only reset if we've used all posts that are currently available
        if set(post_ids).issubset(set(used_posts)):
            logger.info("All posts have been used. Resetting rotation.")
            used_posts = []
            self.state['used_posts'] = []
        
        # Find next unused post
        for post in sorted_posts:
            if post['id'] not in used_posts:
                logger.info(f"Selected next post: {post['name']}")
                
                # Mark as used
                used_posts.append(post['id'])
                self.state['used_posts'] = used_posts
                self.state['last_posted_id'] = post['id']
                self.state['last_posted_time'] = datetime.utcnow().isoformat()
                
                self._save_state()
                return post
        
        logger.warning("No unused posts found")
        return None
    
    def reset(self):
        """Reset rotation state"""
        self.state = {}
        self._save_state()
        logger.info("Rotation state reset")
    
    def get_state_summary(self) -> Dict:
        """Get summary of current rotation state"""
        return {
            'used_posts_count': len(self.state.get('used_posts', [])),
            'last_posted_id': self.state.get('last_posted_id'),
            'last_posted_time': self.state.get('last_posted_time')
        }
