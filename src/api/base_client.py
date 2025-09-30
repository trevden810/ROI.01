"""
Base API client with common functionality
"""

import requests
import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """Base class for API clients with retry logic and error handling"""
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 30, 
                 retry_attempts: int = 3):
        """
        Initialize base API client
        
        Args:
            base_url: Base URL for the API
            api_key: API authentication key
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts for failed requests
        """
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.session = requests.Session()
        
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     method: str = 'GET') -> Dict[str, Any]:
        """
        Make HTTP request with retry logic
        
        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            method: HTTP method (GET, POST, etc.)
        
        Returns:
            JSON response as dictionary
        
        Raises:
            requests.exceptions.RequestException: If request fails after all retries
        """
        url = f"{self.base_url}/{endpoint}"
        
        if params is None:
            params = {}
            
        # Add API key to params
        params['apiKey'] = self.api_key
        
        for attempt in range(self.retry_attempts):
            try:
                logger.debug(f"Making {method} request to {endpoint} (attempt {attempt + 1})")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    timeout=self.timeout
                )
                
                # Check for rate limiting
                if response.status_code == 429:
                    logger.warning("Rate limit hit, waiting 60 seconds...")
                    time.sleep(60)
                    continue
                
                # Raise exception for bad status codes
                response.raise_for_status()
                
                # Log remaining requests
                remaining = response.headers.get('x-requests-remaining')
                if remaining:
                    logger.info(f"API requests remaining: {remaining}")
                
                return response.json()
                
            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout (attempt {attempt + 1}/{self.retry_attempts})")
                if attempt == self.retry_attempts - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {str(e)}")
                if attempt == self.retry_attempts - 1:
                    raise
                time.sleep(2 ** attempt)
        
        raise requests.exceptions.RequestException("Max retry attempts reached")
    
    def close(self):
        """Close the session"""
        self.session.close()
