import http_utils
import json

def get_terms(url, key, secret, jurisdictions = [], include_text='0', markdown='0'):
    request_path = "/api/v3/terms"

    if jurisdictions:
        juridictions_url = ','.join(jurisdictions)
        request_path = request_path + "/" + juridictions_url

    if include_text != '0':
        request_path = request_path + "?include_text=" + include_text

    if markdown != '0':
        query_param_add_symbol = "?"
        if '?' in request_path:
            query_param_add_symbol = "&"
        request_path = request_path + query_param_add_symbol + "markdown=" + markdown

    print("Request path: " + request_path)
    response = http_utils.get(url, request_path, key, secret)
    print(response)
    print(response.content)

def accept_terms(url, key, secret,
    jurisdictions = [], include_text='0', markdown='0',
    agree_to_terms='0', password = ''):
    request_path = "/api/v3/terms"

    if jurisdictions:
        juridictions_url = ','.join(jurisdictions)
        request_path = request_path + "/" + juridictions_url

    if include_text != '0':
        request_path = request_path + "?include_text=" + include_text

    if markdown != '0':
        query_param_add_symbol = "?"
        if '?' in request_path:
            query_param_add_symbol = "&"
        request_path = request_path + query_param_add_symbol + "markdown=" + markdown

    payload = {
        'agree_to_terms': 1
    }

    if password:
        payload['password'] = password

    response = http_utils.post(url, request_path, key, secret, payload)
    print(response.content)

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
