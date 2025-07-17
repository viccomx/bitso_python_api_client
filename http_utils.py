import bitso_auth

import requests
import json

def get(url, request_path, key, secret):
    destination_url = url + request_path

    headers = build_headers(request_path, key, secret, "GET")

    return requests.get(destination_url, headers = headers)

def put(url, request_path, key, secret):
    destination_url = url + request_path

    headers = build_headers(request_path, key, secret, "PUT")

    return requests.put(destination_url, headers = headers)

def post(url, request_path, key, secret, payload):

    json_payload = json.dumps(payload)

    destination_url = url + request_path

    headers = headers = build_headers(request_path, key, secret, "POST", json_payload)

    return requests.post(destination_url, headers = headers, json = payload)

def build_headers(request_path, key, secret, method, payload = ""):
    auth_header = bitso_auth.build_authorization_header(key, secret, method, request_path, payload)

    headers = {
        "user-agent": "vicco-local-python",
        "Authorization" : auth_header,
        "Content-Type" : "application/json"
    }

    return headers