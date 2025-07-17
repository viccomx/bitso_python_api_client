import http_utils
import json

def conversion_quote(url, key, secret, simple_path,
    from_amount, to_amount, source_currency, target_currency):
    request_path = "/v3/conversion_quote"
    if not simple_path:
        request_path = "/api/v3/conversion_quote"

    if from_amount:
        request_path = request_path + "?from_amount=" + from_amount + "&from_currency=" + source_currency + "&to_currency=" + target_currency

    if to_amount:
        request_path = request_path + "?to_amount=" + to_amount + "&from_currency=" + source_currency + "&to_currency=" + target_currency

    print("Request path: " + request_path)
    response = http_utils.get(url, request_path, key, secret)
    print(response)
    print(response.content)

def withdrawal_methods(url, key, secret, currency):
    request_path = "/api/v3/withdrawal_methods"

    if currency:
        request_path = request_path + "/" + currency

    #print(request_path)

    response = http_utils.get(url, request_path, key, secret)
    print(response.content)

def combined_balance(url, key, secret):
    request_path = "/api/v3/combined_balance"

    #print(request_path)

    response = http_utils.get(url, request_path, key, secret)
    print(response.content)
