#!/usr/bin/env python3
"""
Post Fetcher - Retrieves posts from Google Drive or local folder
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

logger = logging.getLogger(__name__)

class PostFetcher: 
    """Fetches and rotates through LinkedIn posts from Google Drive or local folder"""
    
    def __init__(self, use_local_fallback=True):
        """
        Initialize the post fetcher
        
        Args:
            use_local_fallback: If True, will try local posts/ folder if Google Drive fails
        """
        self.folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        self.credentials_json = os.getenv('GOOGLE_CREDENTIALS')
        self.rotation_file = Path(__file__).parent / 'posted.json'
        self.local_posts_dir = Path(__file__).parent.parent / 'posts'
        self.use_local_fallback = use_local_fallback
        self.drive_service = None
        
        # Initialize Google Drive if credentials available
        if self.credentials_json and self.folder_id:
            try:
                self._init_drive_service()
            except Exception as e:
                logger.warning(f"Could not initialize Google Drive:  {e}")
                if use_local_fallback: 
                    logger.info("Will use local posts folder as fallback")
    
    def _init_drive_service(self):
        """Initialize Google Drive service"""
        try: 
            # Parse credentials JSON
            import json
            creds_dict = json.loads(self.credentials_json)
            
            credentials = service_account.Credentials. from_service_account_info(
                creds_dict,
                scopes=['https://www.googleapis.com/auth/drive. readonly']
            )
            
            self.drive_service = build('drive', 'v3', credentials=credentials)
            logger. info("✅ Google Drive service initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Drive:  {e}")
            raise
    
    def _load_rotation_state(self) -> dict:
        """Load the rotation state from file"""
        if self.rotation_file.exists():
            try:
                with open(self.rotation_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load rotation state: {e}")
        return {'posted_files': [], 'last_post_date': None}
    
    def _save_rotation_state(self, state: dict):
        """Save the rotation state to file"""
        try:
            with open(self.rotation_file, 'w') as f:
                json.dump(state, f, indent=2)
            logger.info(f"✅ Rotation state saved: {len(state['posted_files'])} files tracked")
        except Exception as e: 
            logger.error(f"Failed to save rotation state: {e}")
    
    def get_next_post_from_drive(self) -> Optional[str]:
        """Get the next post from Google Drive"""
        if not self.drive_service:
            logger.warning("Google Drive service not available")
            return None
        
        try:
            # Query for text files in the folder
            query = f"'{self.folder_id}' in parents and mimeType='text/plain' and trashed=false"
            results = self.drive_service.files().list(
                q=query,
                fields='files(id, name, modifiedTime)',
                orderBy='name'
            ).execute()
            
            files = results.get('files', [])
            
            if not files:
                logger.warning("No . txt files found in Google Drive folder")
                return None
            
            logger.info(f"Found {len(files)} files in Google Drive")
            
            # Load rotation state
            state = self._load_rotation_state()
            posted_files = set(state. get('posted_files', []))
            
            # Find next unposted file
            next_file = None
            for file in files: 
                if file['id'] not in posted_files: 
                    next_file = file
                    break
            
            # If all files posted, reset and start over
            if not next_file:
                logger.info("All files posted - resetting rotation")
                posted_files = set()
                next_file = files[0]
            
            # Download file content
            request = self.drive_service.files().get_media(fileId=next_file['id'])
            file_handle = io.BytesIO()
            downloader = MediaIoBaseDownload(file_handle, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            content = file_handle.getvalue().decode('utf-8').strip()
            
            # Update rotation state
            posted_files.add(next_file['id'])
            state['posted_files'] = list(posted_files)
            state['last_post_date'] = Path(__file__).parent.joinpath('posted.json').stat().st_mtime if self.rotation_file.exists() else None
            self._save_rotation_state(state)
            
            logger.info(f"✅ Retrieved post from Google Drive: {next_file['name']}")
            return content
            
        except Exception as e:
            logger.error(f"Error fetching from Google Drive: {e}")
            return None
    
    def get_next_post_from_local(self) -> Optional[str]:
        """Get the next post from local posts/ folder"""
        try:
            if not self.local_posts_dir.exists():
                logger.error(f"Local posts directory not found:  {self.local_posts_dir}")
                return None
            
            # Find all . txt files
            txt_files = sorted(self.local_posts_dir. glob('*.txt'))
            
            if not txt_files: 
                logger.error(f"No .txt files found in {self.local_posts_dir}")
                return None
            
            logger.info(f"Found {len(txt_files)} local post files")
            
            # Load rotation state
            state = self._load_rotation_state()
            posted_files = set(state. get('posted_files', []))
            
            # Find next unposted file
            next_file = None
            for file_path in txt_files:
                if file_path.name not in posted_files:
                    next_file = file_path
                    break
            
            # If all files posted, reset and start over
            if not next_file:
                logger.info("All local files posted - resetting rotation")
                posted_files = set()
                next_file = txt_files[0]
            
            # Read file content
            content = next_file.read_text(encoding='utf-8').strip()
            
            # Update rotation state
            posted_files. add(next_file.name)
            state['posted_files'] = list(posted_files)
            from datetime import datetime
            state['last_post_date'] = datetime. now().isoformat()
            self._save_rotation_state(state)
            
            logger.info(f"✅ Retrieved post from local folder: {next_file.name}")
            return content
            
        except Exception as e:
            logger.error(f"Error fetching from local folder: {e}")
            return None
    
    def get_next_post(self) -> Optional[str]:
        """
        Get the next post, trying Google Drive first, then local fallback
        """
        # Try Google Drive first if available
        if self.drive_service:
            content = self.get_next_post_from_drive()
            if content:
                return content
            logger.warning("Google Drive failed, trying local fallback...")
        
        # Fallback to local if enabled
        if self.use_local_fallback:
            return self.get_next_post_from_local()
        
        return None
