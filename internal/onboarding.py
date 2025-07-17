import http_utils

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
