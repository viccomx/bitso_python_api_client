import hashlib
import hmac
import time

# Util class to build all required authentication for bitso app

# Required method to build Bitso auth header
def build_authorization_header(key, secret, http_method, request_path, payload = ""):
    # Arbitrary number that can be used just once
    nonce = str(int(round(time.time() * 1000))) # milliseconds

    # Create signature
    message = nonce + http_method + request_path + payload

    signature = hmac.new(secret.encode('utf-8'), message.encode('utf-8'),hashlib.sha256).hexdigest()

    return 'Bitso %s:%s:%s' % (key, nonce, signature)
