"""Moltbook API client."""

import requests
import json
import time
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

from .config import config
from .exceptions import MoltbookAPIError, AuthenticationError, RateLimitError


class MoltbookClient:
    """Client for interacting with Moltbook API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize API client."""
        self.api_key = api_key or config.get_api_key()
        self.base_url = config.get('api.base_url')
        self.timeout = config.get('api.timeout')
        self.retry_attempts = config.get('api.retry_attempts')
        self.retry_delay = config.get('api.retry_delay')
        
        if not self.api_key:
            raise AuthenticationError("No API key provided. Run 'moltbook auth login' to authenticate.")
        
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'MoltbookCLI/0.1.0'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with retry logic."""
        url = urljoin(self.base_url, endpoint)
        
        for attempt in range(self.retry_attempts):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                
                if response.status_code == 429:
                    raise RateLimitError("Rate limit exceeded")
                
                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key")
                
                if response.status_code >= 400:
                    error_msg = f"API Error {response.status_code}"
                    try:
                        error_data = response.json()
                        if 'message' in error_data:
                            error_msg = error_data['message']
                    except:
                        pass
                    raise MoltbookAPIError(error_msg)
                
                return response.json()
            
            except (requests.RequestException, MoltbookAPIError) as e:
                if attempt == self.retry_attempts - 1:
                    raise e
                
                time.sleep(self.retry_delay * (2 ** attempt))
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information."""
        return self._make_request('GET', '/user/me')
    
    def get_feed(self, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Get personal feed."""
        params = {'limit': limit, 'offset': offset}
        response = self._make_request('GET', '/feed', params=params)
        return response.get('posts', [])
    
    def get_public_feed(self, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Get public feed."""
        params = {'limit': limit, 'offset': offset}
        response = self._make_request('GET', '/feed/public', params=params)
        return response.get('posts', [])
    
    def create_post(self, content: str, visibility: str = 'public') -> Dict[str, Any]:
        """Create a new post."""
        data = {
            'content': content,
            'visibility': visibility
        }
        return self._make_request('POST', '/posts', json=data)
    
    def get_post(self, post_id: str) -> Dict[str, Any]:
        """Get a specific post."""
        return self._make_request('GET', f'/posts/{post_id}')
    
    def delete_post(self, post_id: str) -> Dict[str, Any]:
        """Delete a post."""
        return self._make_request('DELETE', f'/posts/{post_id}')
    
    def like_post(self, post_id: str) -> Dict[str, Any]:
        """Like a post."""
        return self._make_request('POST', f'/posts/{post_id}/like')
    
    def unlike_post(self, post_id: str) -> Dict[str, Any]:
        """Unlike a post."""
        return self._make_request('DELETE', f'/posts/{post_id}/like')
    
    def reply_to_post(self, post_id: str, content: str) -> Dict[str, Any]:
        """Reply to a post."""
        data = {'content': content}
        return self._make_request('POST', f'/posts/{post_id}/replies', json=data)
    
    def get_user_profile(self, username: str) -> Dict[str, Any]:
        """Get user profile."""
        return self._make_request('GET', f'/users/{username}')
    
    def follow_user(self, username: str) -> Dict[str, Any]:
        """Follow a user."""
        return self._make_request('POST', f'/users/{username}/follow')
    
    def unfollow_user(self, username: str) -> Dict[str, Any]:
        """Unfollow a user."""
        return self._make_request('DELETE', f'/users/{username}/follow')
    
    def get_followers(self, username: str) -> List[Dict[str, Any]]:
        """Get user followers."""
        response = self._make_request('GET', f'/users/{username}/followers')
        return response.get('followers', [])
    
    def get_following(self, username: str) -> List[Dict[str, Any]]:
        """Get users that a user is following."""
        response = self._make_request('GET', f'/users/{username}/following')
        return response.get('following', [])
    
    def search_posts(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search posts."""
        params = {'q': query, 'limit': limit}
        response = self._make_request('GET', '/search/posts', params=params)
        return response.get('posts', [])
    
    def search_users(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search users."""
        params = {'q': query, 'limit': limit}
        response = self._make_request('GET', '/search/users', params=params)
        return response.get('users', [])
    
    def get_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get user analytics."""
        params = {'days': days}
        return self._make_request('GET', '/analytics', params=params)