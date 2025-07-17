import public.public_api as public
import internal.internal_api as internal
import internal.conversions_api as conversions
import internal.onboarding as onboarding
import time
import json
import os

def load_config():
    """Load configuration from config.json file"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            "config.json not found. Please copy config.template.json to config.json and fill in your credentials."
        )
    
    with open(config_path, 'r') as f:
        return json.load(f)

def placing_multiple_conversions(env_url, key, secret, required_conversions):
    print("Placing multiple conversion starting...")
    for i in range(required_conversions):
        print(f"Placing conversion {i+1} of {required_conversions}")
        conversion_execution(env_url, key, secret)
        time.sleep(1)
    print("Multiple conversion completed")

def conversion_execution(env_url, key, secret):
    #print("Conversion execution starting...")
    temperonal_convesion_id =conversions.request_quote_v4(env_url, key, secret, "50", "", "mxn", "pepe")
    if temperonal_convesion_id is None:
        print("Error: Failed to get conversion quote")
        return
    
    conversions.execute_quote_v4(env_url, key, secret, temperonal_convesion_id)
    #print("Conversion execution completed")

def main():
    # Load configuration
    config = load_config()
    
    # Set environment
    required_env = ""  # Change this to switch environments
    userId = ""      # Change this to switch users
    
    # Get environment URL and credentials
    env_url = config["environments"][required_env]
    api = config["credentials"][required_env][userId]
    key = api["key"]
    secret = api["secret"]

    #public_auth_place_order(env_url, key, secret, "btc_mxn", "sell", "limit", 1, "", 400000)
    public.account_status(env_url, key, secret)
    #public.catalogues(env_url, key, secret)
    #public_withdrawal_methods(env_url, key, secret, "mxn")
    #internal_terms(env_url, key, secret, simple_path, ["MX"])
    #internal_terms(env_url, key, secret, simple_path, ["MX","GI"])
    #internal_conversion_quote(env_url, key, secret, True, "1", "", "eth", "ars")
    #internal_conversion_quote(env_url, key, secret, "", "3919790.00", "eth", "ars")

    #onboarding.get_terms(env_url, key, secret, ["CO"])
    #onboarding.accept_terms(env_url, key, secret, ["CO"], '0', '0', '0')
    #internal.combined_balance(env_url, key, secret)
    #conversion_execution(env_url, key, secret)
    #placing_multiple_conversions(env_url, key, secret, 45)

if __name__ == "__main__":
   main()