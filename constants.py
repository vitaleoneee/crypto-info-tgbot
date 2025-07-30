REQUEST_LINK_INFO_ABOUT_CRYPTO = "https://api.coingecko.com/api/v3/coins/markets"
HEADERS = {
    'Accepts': 'application/json',
}
PARAMS = {
    'vs_currency': 'usd',
    'precision': '2',
}
RENAME_MAP = {
    'current_price': 'Price of marking (USD)',
    'market_cap': 'Market capitalization (USD)',
    'market_cap_rank': 'Market cap rank',
    'total_volume': 'Total volume (USD)',
    'high_24h': 'Highest price in the last 24h (USD)',
    'low_24h': 'Lowest price in the last 24h (USD)',
    'price_change_24h': 'Price change 24h (USD)',
    'price_change_percentage_24h': 'Price change percentage 24h (%)',
    'market_cap_change_24h': 'Market cap change 24h (USD)',
    'market_cap_change_percentage_24h': 'Market cap change percentage 24h (%)',
    'ath': 'ATH (USD)',
    'ath_change_percentage': 'ATH change percentage (%)',
    'ath_date': 'ATH date',
    'atl': 'ATL (USD)',
    'atl_change_percentage': 'ATL change percentage (%)',
    'atl_date': 'ATL date',
    'last_updated': 'Last update information (GMT+2 Central Europe)',
}
