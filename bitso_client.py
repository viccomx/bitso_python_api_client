import requests
import json
from typing import Optional, Dict, Any
from requests.exceptions import RequestException, Timeout
import bitso_auth

class BitsoClient:
    """A client for making authenticated requests to Bitso API"""
    
    def __init__(self, base_url: str, api_key: str, api_secret: str, timeout: int = 30):
        """
        Initialize the client with API credentials
        
        Args:
            base_url: The base URL for the API (e.g., https://api.bitso.com)
            api_key: The API key
            api_secret: The API secret
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout
        
    def _build_headers(self, request_path: str, method: str, payload: str = "") -> Dict[str, str]:
        """Build request headers with authentication"""
        auth_header = bitso_auth.build_authorization_header(
            self.api_key, 
            self.api_secret, 
            method, 
            request_path, 
            payload
        )
        
        return {
            "User-Agent": "vicco-local-python",
            "Authorization": auth_header,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, path: str, payload: Optional[Dict] = None) -> requests.Response:
        """
        Make an HTTP request with error handling and retries
        
        Args:
            method: HTTP method (GET, POST, PUT)
            path: API endpoint path
            payload: Request payload for POST/PUT requests
        
        Returns:
            Response object
        
        Raises:
            RequestException: If the request fails after retries
        """
        url = f"{self.base_url}{path}"
        json_payload = json.dumps(payload) if payload else ""
        headers = self._build_headers(path, method, json_payload)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=payload if payload else None,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
            
        except Timeout:
            raise RequestException(f"Request timed out after {self.timeout} seconds")
        except RequestException as e:
            raise RequestException(f"Request failed: {str(e)}")
    
    def get(self, path: str) -> requests.Response:
        """Make a GET request"""
        return self._make_request("GET", path)
    
    def post(self, path: str, payload: Dict[str, Any]) -> requests.Response:
        """Make a POST request"""
        return self._make_request("POST", path, payload)
    
    def put(self, path: str, payload: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make a PUT request"""
        return self._make_request("PUT", path, payload) 