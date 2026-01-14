"""LinkedIn Poster - Handles posting content to LinkedIn via API"""
import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class LinkedInPoster:
    """Manages posting content to LinkedIn using the LinkedIn API"""
    
    def __init__(self, access_token: str, person_id: str):
        """
        Initialize LinkedIn Poster
        
        Args:
            access_token: LinkedIn OAuth 2.0 access token
            person_id: LinkedIn person URN (e.g., 'urn:li:person:ABC123')
        """
        self.access_token = access_token
        self.person_id = person_id
        self.api_base = "https://api.linkedin.com/v2"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
    
    def post_text(self, text: str) -> Dict:
        """
        Post text content to LinkedIn
        
        Args:
            text: Text content to post
            
        Returns:
            API response dictionary
        """
        try:
            # LinkedIn UGC Post API endpoint
            url = f"{self.api_base}/ugcPosts"
            
            # Construct post payload
            payload = {
                "author": self.person_id,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            logger.info(f"Posting to LinkedIn (text length: {len(text)})")
            logger.debug(f"Post preview: {text[:100]}...")
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json() if response.text else {}
            post_id = result.get('id', 'unknown')
            
            logger.info(f"Successfully posted to LinkedIn. Post ID: {post_id}")
            return {
                'success': True,
                'post_id': post_id,
                'response': result
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to post to LinkedIn: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"API response: {e.response.text}")
            raise
    
    def get_profile_info(self) -> Dict:
        """
        Get LinkedIn profile information for the authenticated user
        
        Returns:
            Profile information dictionary
        """
        try:
            url = f"{self.api_base}/me"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            profile = response.json()
            logger.info(f"Retrieved profile info for: {profile.get('localizedFirstName')} {profile.get('localizedLastName')}")
            return profile
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get profile info: {e}")
            raise
    
    def validate_token(self) -> bool:
        """
        Validate the access token by attempting to fetch profile info
        
        Returns:
            True if token is valid, False otherwise
        """
        try:
            self.get_profile_info()
            logger.info("Access token is valid")
            return True
        except Exception as e:
            logger.error(f"Access token validation failed: {e}")
            return False
