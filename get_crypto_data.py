import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from constants import REQUEST_LINK_INFO_ABOUT_CRYPTO, HEADERS, PARAMS, RENAME_MAP
from datetime import datetime


def create_text(d_obj):
    d_obj_copy = d_obj.copy()
    text = ''
    for i, (k, v) in enumerate(d_obj_copy.items()):
        text += f'{i + 1}: <b>{k.upper()} 🔹</b>\n'
        try:
            d_obj_copy[k]['usd_24h_change'] = round(d_obj_copy[k]['usd_24h_change'], 2)
            d_obj_copy[k]['last_updated_at'] = datetime.fromtimestamp(d_obj_copy[k]['last_updated_at'])
        except (KeyError, TypeError):
            d_obj_copy[k]['usd_24h_change'] = '-'
            d_obj_copy[k]['last_updated_at'] = '-'
        for kv, vv in v.items():
            new_key = RENAME_MAP.get(kv, kv)
            text += f'{new_key}: <i>{vv}</i>\n'
    return text


def get_popular_derivatives(symbols='btc,eth,sol,xrp'):
    PARAMS['symbols'] = symbols
    try:
        response = requests.get(REQUEST_LINK_INFO_ABOUT_CRYPTO, params=PARAMS, headers=HEADERS).json()
        if response:
            return create_text(response)
        return 'Information about your asset was not found!'
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e

#
# def get_crypto_info(symbols):
#     PARAMS['symbols'] = symbols
#     try:
#         response = requests.get(REQUEST_LINK_INFO_ABOUT_CRYPTO, params=PARAMS, headers=HEADERS).json()
#         if response:
#             return create_text(response)
#         return 'Вы ввели неправильно'
#     except (ConnectionError, Timeout, TooManyRedirects) as e:
#         return e
