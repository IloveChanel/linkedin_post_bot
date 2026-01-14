"""Google Drive Reader - Handles fetching posts from Google Drive"""
import os
import logging
from typing import List, Dict, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import json
import base64

logger = logging.getLogger(__name__)


class DriveReader:
    """Manages interaction with Google Drive API to fetch posts"""
    
    def __init__(self, credentials_json: str = None, credentials_path: str = None, folder_id: str = None):
        """
        Initialize Google Drive Reader
        
        Args:
            credentials_json: Base64 encoded JSON credentials (for GitHub Actions)
            credentials_path: Path to service account JSON credentials (for local)
            folder_id: Google Drive folder ID containing posts
        """
        self.folder_id = folder_id
        self.service = None
        self._authenticate(credentials_json, credentials_path)
    
    def _authenticate(self, credentials_json: str = None, credentials_path: str = None):
        """Authenticate with Google Drive API using service account"""
        try:
            if credentials_json:
                # Decode base64 credentials (GitHub Actions)
                logger.info("Using base64-encoded credentials")
                try:
                    creds_data = json.loads(base64.b64decode(credentials_json))
                except (json.JSONDecodeError, base64.binascii.Error, ValueError):
                    # Maybe it's already decoded JSON string
                    creds_data = json.loads(credentials_json)
                
                credentials = service_account.Credentials.from_service_account_info(
                    creds_data,
                    scopes=['https://www.googleapis.com/auth/drive.readonly']
                )
            elif credentials_path and os.path.exists(credentials_path):
                # Use file path (local development)
                logger.info(f"Using credentials file: {credentials_path}")
                credentials = service_account.Credentials.from_service_account_file(
                    credentials_path,
                    scopes=['https://www.googleapis.com/auth/drive.readonly']
                )
            else:
                raise ValueError("No valid credentials provided (need credentials_json or credentials_path)")
            
            self.service = build('drive', 'v3', credentials=credentials)
            logger.info("Successfully authenticated with Google Drive API")
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Drive: {e}")
            raise
    
    def list_posts(self) -> List[Dict]:
        """
        List all text files in the specified Drive folder
        
        Returns:
            List of post dictionaries with id, name, and createdTime
        """
        try:
            # Query for text files - using name filter for .txt extension
            query = f"'{self.folder_id}' in parents and name contains '.txt' and trashed=false"
            
            results = self.service.files().list(
                q=query,
                fields="files(id, name, createdTime)",
                orderBy="createdTime desc"
            ).execute()
            
            posts = results.get('files', [])
            logger.info(f"Found {len(posts)} posts in Google Drive folder")
            return posts
            
        except Exception as e:
            logger.error(f"Failed to list posts from Google Drive: {e}")
            raise
    
    def get_post_content(self, file_id: str) -> str:
        """
        Download and return content of a specific file
        
        Args:
            file_id: Google Drive file ID
            
        Returns:
            Content of the file as string
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_buffer = io.BytesIO()
            downloader = MediaIoBaseDownload(file_buffer, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.debug(f"Download progress: {int(status.progress() * 100)}%")
            
            content = file_buffer.getvalue().decode('utf-8')
            logger.info(f"Successfully downloaded post content (length: {len(content)})")
            return content.strip()
            
        except Exception as e:
            logger.error(f"Failed to download post content: {e}")
            raise
    
    def get_file_metadata(self, file_id: str) -> Dict:
        """
        Get metadata for a specific file
        
        Args:
            file_id: Google Drive file ID
            
        Returns:
            File metadata dictionary
        """
        try:
            metadata = self.service.files().get(
                fileId=file_id,
                fields="id, name, createdTime, modifiedTime, size"
            ).execute()
            
            logger.debug(f"Retrieved metadata for file: {metadata.get('name')}")
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to get file metadata: {e}")
            raise
