""" Functions for interacting with the Stocktwits API """

import urllib
import os
from typing import Callable

import requests

STOCKTWITS_ACCESS_TOKEN = os.environ.get("STOCKTWITS_ACCESS_TOKEN")
if not STOCKTWITS_ACCESS_TOKEN:
    print("Error: The `STOCKTWITS_ACCESS_TOKEN` environment variable must be supplied.")

STOCKTWITS_BASE_URL = "https://api.stocktwits.com/api/2"


def map_method_name_to_requests_function(method_name: str) -> Callable:
    return {
        "POST": requests.post,
        "GET": requests.get,
        "PUT": requests.put,
        "PATCH": requests.patch,
        "DELETE": requests.delete,
    }[method_name.upper()]


def stocktwits_request(method: str, path: str, *args, headers={}, **kwargs) -> object:
    """ Makes a request to the Stocktwits API, passing along the username and password as
    authorization headers. """

    req_function = map_method_name_to_requests_function(method)
    merged_headers = {**headers, "Authorization": f"OAuth {STOCKTWITS_ACCESS_TOKEN}"}
    url = f"{STOCKTWITS_BASE_URL}{path}"
    res = req_function(url, *args, headers=merged_headers, **kwargs)
    return res.json()


def post_twit(content: str):
    print(f"Posting twit: {content}")
    escaped_content = urllib.parse.quote_plus(content)
    stocktwits_request("POST", "/messages/create.json", data=f"body={escaped_content}")
