import requests

def mockable_request(url: str, headers: dict = {}) -> json:
    return requests.get(url, headers=headers).json()