REQUEST_LINK_INFO_ABOUT_CRYPTO = "https://api.coingecko.com/api/v3/simple/price"
HEADERS = {
    'Accepts': 'application/json',
}
PARAMS = {
    'vs_currencies': 'usd',
    'include_market_cap': 'true',
    'include_24hr_vo': 'true',
    'include_24hr_change': 'true',
    'include_last_updated_at': 'true',
}
RENAME_MAP = {
    'usd': 'Price of marking (USD)',
    'usd_market_cap': 'Market capitalization (USD)',
    'usd_24h_change': 'Changes in 24 hours (in percent)',
    'last_updated_at': 'Last update information (GMT+2 Central Europe)'
}
