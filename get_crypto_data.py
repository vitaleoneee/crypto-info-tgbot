import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from constants import REQUEST_LINK_INFO_ABOUT_CRYPTO, HEADERS, PARAMS
from copy import deepcopy

from utils import create_price_info_text, create_top_capitalization_text


def get_top_capitalization(count=10):
    params = deepcopy(PARAMS)
    params['order'] = 'market_cap_desc'
    params['per_page'] = count
    try:
        response = requests.get(REQUEST_LINK_INFO_ABOUT_CRYPTO, params=params, headers=HEADERS).json()
        if response:
            return create_top_capitalization_text(response)
        return 'Information about your asset was not found!'
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def get_assets_price(symbols='btc,eth,sol,xrp'):
    if len(symbols.split()) > 1:
        return 'Write the symbol of the cryptocurrency or separate them with commas if you want several (e.g. btc,eth,ada)'
    params = deepcopy(PARAMS)
    params['symbols'] = symbols
    try:
        response = requests.get(REQUEST_LINK_INFO_ABOUT_CRYPTO, params=params, headers=HEADERS).json()
        if response:
            return create_price_info_text(response)
        return 'Information about your asset was not found!'
    except (ConnectionError, Timeout, TooManyRedirects):
        return 'Error on the bot side. Contact the developer @vitaleoneee'
