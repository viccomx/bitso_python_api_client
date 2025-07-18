import requests
import json
from typing import Optional, Dict, Any
from requests.exceptions import RequestException, Timeout
import bitso_auth
from config_utils import ConfigUtils

class BitsoClient:
    """A client for making authenticated requests to Bitso API
    """
    
    def __init__(self, env: str, user_id: str, config_path: Optional[str] = None, timeout: int = 30):
        """
        Initialize BitsoClient from configuration
        
        Args:
            env: Environment name (e.g., 'prod', 'stage')
            user_id: User ID or level to use from credentials
            config_path: Optional path to config file. If not provided, looks in same directory
            timeout: Request timeout in seconds
            
        Raises:
            FileNotFoundError: If config file is not found
            KeyError: If required configuration keys are missing
            
        Example:
            client = BitsoClient('prod', '234237')
        """
        config = ConfigUtils.load_config(config_path)
        try:
            env_url = config["environments"][env]
            api = config["credentials"][env][user_id]
            
            self._base_url = env_url.rstrip('/')  # Remove trailing slash if present
            self._api_key = api["key"]
            self._api_secret = api["secret"]
            self._timeout = timeout
            
        except KeyError as e:
            raise KeyError(f"Missing required configuration: {e}")
    
    def _build_headers(self, request_path: str, method: str, payload: str = "") -> Dict[str, str]:
        """Build request headers with authentication"""
        auth_header = bitso_auth.build_authorization_header(
            self._api_key, 
            self._api_secret, 
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
        url = f"{self._base_url}{path}"
        json_payload = json.dumps(payload) if payload else ""
        headers = self._build_headers(path, method, json_payload)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=payload if payload else None,
                timeout=self._timeout
            )
            response.raise_for_status()
            return response
            
        except Timeout:
            raise RequestException(f"Request timed out after {self._timeout} seconds")
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
