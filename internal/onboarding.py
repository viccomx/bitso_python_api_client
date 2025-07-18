from typing import List, Optional
from requests.exceptions import RequestException
from bitso_client import BitsoClient
import internal.internal_api as internal_api
import time
import threading
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class Onboarding:

    @staticmethod
    def testing_terms_migration(client: BitsoClient):
        num_threads = 5
        required_iterations = 500
        
        start_time = datetime.datetime.now()
        print(f"Getting multiple terms starting at {start_time.strftime('%Y-%m-%d %H:%M:%S')} with {num_threads} threads...")
        
        def make_terms_request():
            """Function to be executed by each thread"""
            try:
                internal_api.get_terms(client)
                return True
            except Exception as e:
                print(f"Thread error: {e}")
                return False
        
        # Use ThreadPoolExecutor to manage threads
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit all tasks
            futures = [executor.submit(make_terms_request) for _ in range(required_iterations)]
            
            # Wait for all tasks to complete and collect results
            successful_requests = 0
            for future in as_completed(futures):
                if future.result():
                    successful_requests += 1
        
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        print(f"Multiple terms completed at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {duration.total_seconds():.2f} seconds")
        print(f"Successful requests: {successful_requests}/{required_iterations}")
        print(f"Average time per request: {duration.total_seconds()/required_iterations:.3f} seconds")

    @staticmethod
    def testing_terms_migration_with_rotation(env: str, user_id: str):
        """Test terms migration with API key rotation enabled"""
        # Create client with key rotation enabled
        client = BitsoClient(env=env, user_id=user_id, enable_key_rotation=True)
        Onboarding.testing_terms_migration(client)

    """Static methods for handling Bitso onboarding-related API endpoints"""

    @staticmethod
    def accept_terms(client: BitsoClient, jurisdictions: List[str], include_text: str = '0', 
                    markdown: str = '0', agree_to_terms: bool = False, 
                    password: Optional[str] = None) -> dict:
        """
        Accept terms and conditions for specified jurisdictions
        
        Args:
            client: BitsoClient instance
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
        payload: dict = {"agree_to_terms": int(agree_to_terms)}
        if password:
            payload["password"] = password

        try:
            response = client.post(request_path, payload)
            return response.json()
        except RequestException as e:
            print(f"Error accepting terms: {e}")
            raise
