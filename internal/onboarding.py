from typing import List, Optional
from requests.exceptions import RequestException
from bitso_client import BitsoClient

class Onboarding:
    """Static methods for handling Bitso onboarding-related API endpoints"""

    @staticmethod
    def get_terms(client: BitsoClient, jurisdictions: Optional[List[str]] = None, 
                 include_text: str = '0', markdown: str = '0') -> dict:
        """
        Get terms and conditions for specified jurisdictions
        
        Args:
            client: Configured BitsoClient instance
            jurisdictions: List of jurisdiction codes (e.g., ["MX", "CO"])
            include_text: Whether to include full text ('0' or '1')
            markdown: Whether to return text in markdown format ('0' or '1')
        
        Returns:
            Dictionary containing terms information
        
        Raises:
            RequestException: If the API request fails
        """
        request_path = "/api/v3/terms"

        # Build path with jurisdictions if provided
        if jurisdictions:
            jurisdictions_url = ','.join(jurisdictions)
            request_path = f"{request_path}/{jurisdictions_url}"

        # Add query parameters if needed
        params = []
        if include_text != '0':
            params.append(f"include_text={include_text}")
        if markdown != '0':
            params.append(f"markdown={markdown}")
        
        if params:
            request_path = f"{request_path}?{'&'.join(params)}"

        try:
            response = client.get(request_path)
            return response.json()
        except RequestException as e:
            print(f"Error getting terms: {e}")
            raise

    @staticmethod
    def accept_terms(client: BitsoClient, jurisdictions: List[str], include_text: str = '0', 
                    markdown: str = '0', agree_to_terms: bool = False, 
                    password: Optional[str] = None) -> dict:
        """
        Accept terms and conditions for specified jurisdictions
        
        Args:
            client: Configured BitsoClient instance
            jurisdictions: List of jurisdiction codes (e.g., ["MX", "CO"])
            include_text: Whether to include full text ('0' or '1')
            markdown: Whether to return text in markdown format ('0' or '1')
            agree_to_terms: Whether user agrees to terms (True/False)
            password: Optional password for confirmation
        
        Returns:
            Dictionary containing acceptance response
            
        Raises:
            RequestException: If the API request fails
        """
        request_path = "/api/v3/terms"

        # Build path with jurisdictions
        if jurisdictions:
            jurisdictions_url = ','.join(jurisdictions)
            request_path = f"{request_path}/{jurisdictions_url}"

        # Add query parameters if needed
        params = []
        if include_text != '0':
            params.append(f"include_text={include_text}")
        if markdown != '0':
            params.append(f"markdown={markdown}")
        
        if params:
            request_path = f"{request_path}?{'&'.join(params)}"

        # Prepare payload
        payload = {"agree_to_terms": 1 if agree_to_terms else 0}
        if password:
            payload["password"] = password

        try:
            response = client.post(request_path, payload)
            return response.json()
        except RequestException as e:
            print(f"Error accepting terms: {e}")
            raise

# Example usage:
"""
client = BitsoClient(
    base_url="https://api.bitso.com",
    api_key="your_key",
    api_secret="your_secret"
)

# Get terms
terms = Onboarding.get_terms(client, jurisdictions=["CO"])
print(terms)

# Accept terms
result = Onboarding.accept_terms(
    client,
    jurisdictions=["CO"],
    agree_to_terms=True,
    password='optional_password'
)
print(result)
"""
