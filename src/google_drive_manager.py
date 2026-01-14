"""Google Drive Manager - Handles fetching posts from Google Drive"""
import os
import logging
from typing import List, Dict, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

logger = logging.getLogger(__name__)


class GoogleDriveManager:
    """Manages interaction with Google Drive API to fetch posts"""
    
    def __init__(self, credentials_path: str, folder_id: str):
        """
        Initialize Google Drive Manager
        
        Args:
            credentials_path: Path to service account JSON credentials
            folder_id: Google Drive folder ID containing posts
        """
        self.folder_id = folder_id
        self.credentials_path = credentials_path
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API using service account"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
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
            query = f"'{self.folder_id}' in parents and mimeType='text/plain' and trashed=false"
            
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
            return content
            
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
