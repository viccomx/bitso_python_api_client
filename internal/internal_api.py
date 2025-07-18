import http_utils
from bitso_client import BitsoClient
from typing import List, Optional
from requests.exceptions import RequestException


def conversion_quote(
    url,
    key,
    secret,
    simple_path,
    from_amount,
    to_amount,
    source_currency,
    target_currency,
):
    request_path = "/v3/conversion_quote"
    if not simple_path:
        request_path = "/api/v3/conversion_quote"

    if from_amount:
        request_path = (
            request_path
            + "?from_amount="
            + from_amount
            + "&from_currency="
            + source_currency
            + "&to_currency="
            + target_currency
        )

    if to_amount:
        request_path = (
            request_path
            + "?to_amount="
            + to_amount
            + "&from_currency="
            + source_currency
            + "&to_currency="
            + target_currency
        )

    print("Request path: " + request_path)
    response = http_utils.get(url, request_path, key, secret)
    print(response)
    print(response.content)


def withdrawal_methods(url, key, secret, currency):
    request_path = "/api/v3/withdrawal_methods"

    if currency:
        request_path = request_path + "/" + currency

    # print(request_path)

    response = http_utils.get(url, request_path, key, secret)
    print(response.content)


def combined_balance(url, key, secret):
    request_path = "/api/v3/combined_balance"

    # print(request_path)

    response = http_utils.get(url, request_path, key, secret)
    print(response.content)


def get_terms(
    client: BitsoClient,
    jurisdictions: Optional[List[str]] = None,
    include_text: str = "0",
    markdown: str = "0",
):
    """
    Get terms from the API

    Args:
        client: BitsoClient instance
        jurisdictions: Optional list of jurisdictions
        include_text: Include text flag ("0" or "1")
        markdown: Markdown flag ("0" or "1")

    Returns:
        dict: The payload data from successful response

    Raises:
        RequestException: For network/HTTP errors
        ValueError: For API errors with specific error code and message
    """
    request_path = "/api/v3/terms"

    # Build path with jurisdictions if provided
    if jurisdictions:
        jurisdictions_url = ",".join(jurisdictions)
        request_path = f"{request_path}/{jurisdictions_url}"

    # Add query parameters if needed
    params = []
    if include_text != "0":
        params.append(f"include_text={include_text}")
    if markdown != "0":
        params.append(f"markdown={markdown}")

    if params:
        request_path = f"{request_path}?{'&'.join(params)}"

    # Use the get method for automatic error handling and response parsing
    return client.get(request_path)
