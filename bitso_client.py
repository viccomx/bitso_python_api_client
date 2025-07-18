import requests
import json
import random
from typing import Optional, Dict, Any, List
from requests.exceptions import (
    RequestException, 
    Timeout, 
    ConnectionError, 
    HTTPError,
    TooManyRedirects,
    URLRequired
)
import bitso_auth
from config_utils import ConfigUtils

class BitsoClient:
    """A client for making authenticated requests to Bitso API with built-in error handling and API key rotation"""

    def __init__(
        self,
        env: str,
        user_id: str,
        config_path: Optional[str] = None,
        timeout: int = 30,
        enable_key_rotation: bool = False,
    ):
        """
        Initialize BitsoClient from configuration

        Args:
            env: Environment name (e.g., 'prod', 'stage')
            user_id: User ID or level to use from credentials
            config_path: Optional path to config file. If not provided, looks in same directory
            timeout: Request timeout in seconds
            enable_key_rotation: Whether to enable API key rotation for rate limiting

        Raises:
            FileNotFoundError: If config file is not found
            KeyError: If required configuration keys are missing

        Example:
            client = BitsoClient('prod', '234237')
            client_with_rotation = BitsoClient('prod', '234237', enable_key_rotation=True)
        """
        config = ConfigUtils.load_config(config_path)

        try:
            env_url = config["environments"][env]
            api = config["credentials"][env][user_id]

            self._base_url = env_url.rstrip("/")  # Remove trailing slash if present
            self._timeout = timeout
            self._enable_key_rotation = enable_key_rotation
            
            # Handle single API key (current behavior)
            if isinstance(api, dict):
                self._api_keys = [{"key": api["key"], "secret": api["secret"]}]
                self._current_key_index = 0
            
            # Handle multiple API keys for rotation
            elif isinstance(api, list):
                if not enable_key_rotation:
                    raise ValueError("Multiple API keys provided but key rotation is disabled. Set enable_key_rotation=True")
                self._api_keys = [{"key": key["key"], "secret": key["secret"]} for key in api]
                self._current_key_index = 0
                # Shuffle keys for better distribution
                random.shuffle(self._api_keys)
            else:
                raise ValueError("Invalid API configuration format")

        except KeyError as e:
            raise KeyError(f"Missing required configuration: {e}")

    def _get_current_key(self) -> Dict[str, str]:
        """Get the current API key and secret"""
        return self._api_keys[self._current_key_index]

    def _rotate_key(self):
        """Rotate to the next API key"""
        if len(self._api_keys) > 1:
            self._current_key_index = (self._current_key_index + 1) % len(self._api_keys)
            print(f"Rotated to API key {self._current_key_index + 1} of {len(self._api_keys)}")

    def _is_rate_limited(self, response: requests.Response) -> bool:
        """Check if the response indicates rate limiting"""
        # Check for standard rate limit status codes
        if response.status_code == 429:  # Too Many Requests
            return True
        
        # Check for rate limit in response body (common for APIs that use 400)
        try:
            response_data = response.json()
            if response_data.get("success") is False:
                error_code = response_data.get("error", {}).get("code", "")
                error_message = response_data.get("error", {}).get("message", "")
                
                # Specific detection for this API: 400 status + error code 200 + "Too many requests"
                if (response.status_code == 400 and 
                    str(error_code) == "200" and 
                    "too many requests" in str(error_message).lower()):
                    return True
                
                # Fallback: Common rate limit error codes and messages
                rate_limit_codes = [
                    "RATE_LIMIT", 
                    "TOO_MANY_REQUESTS", 
                    "429", 
                    "RATE_LIMIT_EXCEEDED",
                    "RATE_LIMIT_HIT",
                    "QUOTA_EXCEEDED",
                    "THROTTLE_LIMIT",
                    "LIMIT_EXCEEDED"
                ]
                
                rate_limit_messages = [
                    "rate limit",
                    "too many requests",
                    "quota exceeded",
                    "throttle",
                    "limit exceeded",
                    "rate limit exceeded"
                ]
                
                # Check error code
                if any(code in str(error_code).upper() for code in rate_limit_codes):
                    return True
                
                # Check error message
                if any(msg in str(error_message).lower() for msg in rate_limit_messages):
                    return True
                    
        except:
            pass
        
        return False

    def _build_headers(
        self, request_path: str, method: str, payload: str = ""
    ) -> Dict[str, str]:
        """Build request headers with authentication"""
        current_key = self._get_current_key()
        auth_header = bitso_auth.build_authorization_header(
            current_key["key"], current_key["secret"], method, request_path, payload
        )

        return {
            "User-Agent": "vicco-local-python",
            "Authorization": auth_header,
            "Content-Type": "application/json",
        }

    def _handle_response(self, response_data: Dict[str, Any]) -> Any:
        """
        Handle common API response patterns
        
        Args:
            response_data: Parsed JSON response
            
        Returns:
            The payload data from successful response
            
        Raises:
            ValueError: For API errors with specific error code and message
        """
        # Check if response has the expected structure
        if not isinstance(response_data, dict):
            raise ValueError(f"Unexpected response format: {response_data}")
        
        # Handle success case
        if response_data.get("success") is True:
            payload = response_data.get("payload")
            if payload is None:
                raise ValueError("Success response missing payload")
            return payload
        
        # Handle API error case
        elif response_data.get("success") is False:
            error_data = response_data.get("error", {})
            error_message = error_data.get("message", "Unknown error")
            error_code = error_data.get("code", "UNKNOWN")
            raise ValueError(f"API Error {error_code}: {error_message}")
        
        # Handle unexpected response structure
        else:
            raise ValueError(f"Unexpected response structure: {response_data}")

    def _make_request(
        self, method: str, path: str, payload: Optional[Dict] = None, max_retries: int = 3
    ) -> Any:
        """
        Make an HTTP request with automatic error handling, response parsing, and key rotation

        Args:
            method: HTTP method (GET, POST, PUT)
            path: API endpoint path
            payload: Request payload for POST/PUT requests
            max_retries: Maximum number of retries with different keys

        Returns:
            Parsed response data

        Raises:
            RequestException: If the request fails due to network/timeout issues
            ValueError: For API errors with specific error code and message
        """
        last_exception = RequestException("All retry attempts failed")
        
        for attempt in range(max_retries):
            url = f"{self._base_url}{path}"
            json_payload = json.dumps(payload) if payload else ""
            headers = self._build_headers(path, method, json_payload)

            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=payload if payload else None,
                    timeout=self._timeout,
                )
                
                # Check for rate limiting
                if self._enable_key_rotation and self._is_rate_limited(response):
                    print(f"Rate limited on attempt {attempt + 1}, rotating key...")
                    self._rotate_key()
                    if attempt < max_retries - 1:  # Don't rotate on last attempt
                        continue
                
                # Parse response
                response_data = response.json()
                return self._handle_response(response_data)

            except Timeout:
                last_exception = RequestException(f"Request timed out after {self._timeout} seconds")
            except ConnectionError as e:
                last_exception = RequestException(f"Connection failed: {str(e)}")
            except TooManyRedirects as e:
                last_exception = RequestException(f"Too many redirects: {str(e)}")
            except URLRequired as e:
                last_exception = RequestException(f"Invalid URL: {str(e)}")
            except RequestException as e:
                last_exception = RequestException(f"Request failed: {str(e)}")
            except ValueError as e:
                print(f"API error: {e}")
                last_exception = e
            except Exception as e:
                print(f"Unexpected error: {e}")
                last_exception = e
            
            # If we have more attempts and key rotation is enabled, try with next key
            if attempt < max_retries - 1 and self._enable_key_rotation and len(self._api_keys) > 1:
                print(f"Request failed on attempt {attempt + 1}, trying with next key...")
                self._rotate_key()
        
        # If we get here, all retries failed
        raise last_exception

    def get(self, path: str, max_retries: int = 1) -> Any:
        """Make a GET request with automatic response parsing and error handling"""
        return self._make_request("GET", path, None, max_retries)

    def post(self, path: str, payload: Dict[str, Any], max_retries: int = 1) -> Any:
        """Make a POST request with automatic response parsing and error handling"""
        return self._make_request("POST", path, payload, max_retries)

    def put(self, path: str, payload: Optional[Dict[str, Any]] = None, max_retries: int = 1) -> Any:
        """Make a PUT request with automatic response parsing and error handling"""
        return self._make_request("PUT", path, payload, max_retries)
