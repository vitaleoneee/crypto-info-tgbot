from datetime import datetime
from zoneinfo import ZoneInfo

from constants import RENAME_MAP


def add_symbol(d_value):
    if d_value > 0:
        return ' 📈\n'
    return ' 📉\n'


def create_text(obj):
    text = ''
    for i, d in enumerate(obj):
        symbol = d.get('symbol', '???').upper()
        price_change = d.get('price_change_percentage_24h', 0)
        text += f"{i + 1}: <b>{symbol}</b> {add_symbol(price_change)}\n"

        raw_time = d.get('last_updated')
        if raw_time:
            try:
                last_updated = datetime.fromisoformat(
                    raw_time.replace('Z', '+00:00')
                ).astimezone(ZoneInfo('Europe/Prague')).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                last_updated = '-'
        else:
            last_updated = '-'

        for k, v in d.items():
            if k in RENAME_MAP:
                value = last_updated if k == 'last_updated' else v
                text += f"{RENAME_MAP[k]}: <i>{value}</i>\n"

        text += "\n"
    return text
