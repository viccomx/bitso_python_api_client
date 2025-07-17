import public.public_api as public
import internal.internal_api as internal
import internal.conversions_api as conversions
import time

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

    environments = {
        "local_host": "http://localhost:8080",
        "local" : "http://bitso.lan",
        "dev" : "https://dev.bitso.com",
        "stage" : "https://stage.bitso.com",
        "prod": "https://api.bitso.com"
    }

    credentials = {}

    simple_path = False
    #simple_path = True

    #required_env = "local_host"
    #required_env = "dev"
    required_env = "stage"
    #required_env = "prod"

    #userId = 45930
    #userId = 234237
    # STAGE
    #userId = 28
    userId = 63631

    env_url = environments[required_env]
    api = credentials[required_env][userId]
    key = api["key"]
    secret = api["secret"]


    #public_auth_place_order(env_url, key, secret, "btc_mxn", "sell", "limit", 1, "", 400000)
    #public.account_status(env_url, key, secret)
    #public.catalogues(env_url, key, secret)
    #public_withdrawal_methods(env_url, key, secret, "mxn")
    #internal_terms(env_url, key, secret, simple_path, ["MX"])
    #internal_terms(env_url, key, secret, simple_path, ["MX","GI"])
    #internal_conversion_quote(env_url, key, secret, True, "1", "", "eth", "ars")
    #internal_conversion_quote(env_url, key, secret, "", "3919790.00", "eth", "ars")

    #internal.get_terms(env_url, key, secret, ["CO"])
    #internal.accept_terms(env_url, key, secret, ["CO"], '0', '0', '0')
    #internal.combined_balance(env_url, key, secret)
    #conversion_execution(env_url, key, secret)
    placing_multiple_conversions(env_url, key, secret, 45)

if __name__ == "__main__":
   main()