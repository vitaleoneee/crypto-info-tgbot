import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from constants import REQUEST_LINK_INFO_ABOUT_CRYPTO, HEADERS, PARAMS


def format_dict(d_obj):
    for k, v in d_obj.items():
        print(k, v)
    return 'Success'


def get_crypto_info(symbols):
    PARAMS['symbols'] = symbols
    try:
        response = requests.get(REQUEST_LINK_INFO_ABOUT_CRYPTO, params=PARAMS, headers=HEADERS).json()
        if response:
            return format_dict(response)
        return 'Вы ввели неправильно'
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e
