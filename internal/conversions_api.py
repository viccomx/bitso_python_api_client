import http_utils
import json

def request_quote_v4(url, key, secret, from_amount, to_amount, source_currency, target_currency):
    request_path = "/api/v4/currency_conversions"

    payload = {
        'from_currency': source_currency,
        'to_currency': target_currency
    }

    if from_amount and to_amount:
        print("from_amount and to_amount are not allowed to be used together")
        return None

    if from_amount:
        payload['spend_amount'] = from_amount

    if to_amount:
        payload['receive_amount'] = to_amount

    response = http_utils.post(url, request_path, key, secret, payload)
    # print(response)
    # print(response.content)
    
    # Parse JSON response
    if response.status_code == 200:
        try:
            response_data = response.json()
            if response_data.get('success') and 'payload' in response_data:
                quote_id = response_data['payload']['id']
                print(f"Quote ID: {quote_id}")
                return quote_id  # Return just the quote ID string
            else:
                print("Response does not contain expected success/payload structure")
                return None
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            return None
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None

def execute_quote_v4(url, key, secret, quote_id):
    if quote_id is None:
        print(f"Cannot execute quote: quote_id is None")
        return None
        
    request_path = "/api/v4/currency_conversions"
    request_path = request_path + "/" + quote_id

    # print("Request path: " + request_path)
    response = http_utils.put(url, request_path, key, secret)
    # print(response)
    # print(response.content)
    
    # Parse JSON response
    if response.status_code == 200:
        try:
            response_data = response.json()
            # print(f"Execute quote response: {response_data}")
            return response_data
        except json.JSONDecodeError as e:
            #print(f"Failed to parse JSON response: {e}")
            return None
    else:
        # print(f"Request failed with status code: {response.status_code}")
        return None