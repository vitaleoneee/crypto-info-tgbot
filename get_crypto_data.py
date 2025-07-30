import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from constants import REQUEST_LINK_INFO_ABOUT_CRYPTO, HEADERS, PARAMS

from utils import create_text


def get_assets_price(symbols='btc,eth,sol,xrp'):
    PARAMS['symbols'] = symbols
    try:
        response = requests.get(REQUEST_LINK_INFO_ABOUT_CRYPTO, params=PARAMS, headers=HEADERS).json()
        if response:
            return create_text(response)
        return 'Information about your asset was not found!'
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e
