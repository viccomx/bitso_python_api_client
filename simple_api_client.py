import public.public_api as public
import internal.internal_api as internal
import internal.conversions_api as conversions
import internal.onboarding as onboarding
from bitso_client import BitsoClient
import time
from typing import Optional

def placing_multiple_conversions(client: BitsoClient, required_conversions: int) -> None:
    """
    Place multiple conversions
    
    Args:
        client: BitsoClient instance
        required_conversions: Number of conversions to place
    """
    print("Placing multiple conversion starting...")
    for i in range(required_conversions):
        print(f"Placing conversion {i+1} of {required_conversions}")
        conversion_execution(client)
        time.sleep(1)
    print("Multiple conversion completed")

def conversion_execution(client: BitsoClient) -> None:
    """
    Execute a single conversion
    
    Args:
        client: BitsoClient instance
    """
    #print("Conversion execution starting...")
    # temperonal_convesion_id = conversions.request_quote_v4(
    #     client.base_url, 
    #     client.api_key, 
    #     client.api_secret, 
    #     "50", "", "mxn", "pepe"
    # )
    
    # if temperonal_convesion_id is None:
    #     print("Error: Failed to get conversion quote")
    #     return
    
    # conversions.execute_quote_v4(
    #     client.base_url,
    #     client.api_key,
    #     client.api_secret,
    #     temperonal_convesion_id
    # )
    #print("Conversion execution completed")

def main() -> None:
    """Main execution function"""
    try:
        # Create BitsoClient instance
        client = BitsoClient(
            env="stage",      # Change this to switch environments
            user_id="28",     # Change this to switch users
            timeout=10        # Reduced timeout for faster processing
        )

        #public.account_status(client)
        onboarding.Onboarding.testing_terms_migration(client)
        
        # Commented examples
        """
        # Public API calls
        public.catalogues(client)
        public.withdrawal_methods(client, "mxn")
        
        # Internal API calls
        internal.get_terms(client, ["MX"])
        internal.get_terms(client, ["MX", "GI"])
        internal.conversion_quote(client, True, "1", "", "eth", "ars")
        internal.conversion_quote(client, "", "3919790.00", "eth", "ars")
        internal.combined_balance(client)
        
        # Onboarding
        onboarding.get_terms(client, ["CO"])
        onboarding.accept_terms(client, ["CO"])
        
        # Conversions
        conversion_execution(client)
        placing_multiple_conversions(client, 45)
        """
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()