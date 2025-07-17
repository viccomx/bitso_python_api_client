import http_utils

# https://bitso.com/api_info#place-an-order
def place_order(url, key, secret,
    book, side, type, major = "", minor = "", rate = "", origin_id = ""):
    request_path = "/api/v3/orders"
    payload = {
        'book':book,
        'side':side,
        'type':type,
    }

    if major:
        payload['major'] = major

    if minor:
        payload['minor'] = minor

    if rate:
        payload['price'] = rate

    if not origin_id:
        # For user sanity let's add a default origin id
        payload['origin_id'] = 'filler' + str(int(round(time.time() * 1000)))
    else:
        payload['origin_id'] = origin_id

    response = http_utils.post(url, request_path, key, secret, payload)
    print(response.content)

# https://bitso.com/api_info#account-status
def account_status(url, key, secret):
    request_path = "/api/v3/account_status"
    response = http_utils.get(url, request_path, key, secret)
    print(response.content)

def catalogues(url, key, secret):
    request_path = "/api/v3/catalogues"
    response = http_utils.get(url, request_path, key, secret)
    print(response.content)
