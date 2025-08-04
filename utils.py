import asyncio
from copy import deepcopy
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests
from aiogram import types

from constants import MAIN_RENAME_MAP, TOP_CAPITALIZATION_RENAME_MAP, PARAMS, REQUEST_LINK_INFO_ABOUT_CRYPTO, HEADERS


def add_symbol(d_value):
    return ' 📈\n' if d_value > 0 else ' 📉\n'


def add_medal(index):
    if index == 0:
        return '🥇'
    elif index == 1:
        return '🥈'
    elif index == 2:
        return '🥉'
    return ''


def format_large_number(n):
    try:
        n = float(n)
    except (ValueError, TypeError):
        return n

    if n >= 1_000_000_000_000:
        return f"{n / 1_000_000_000_000:.2f}T"
    elif n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.2f}B"
    elif n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    return f"{n:.0f}"


def parse_command_args(message: types.Message, max_args: int = 1):
    raw_args = message.text.split()
    args = [arg.strip() for arg in raw_args[1:]]
    if len(args) > max_args:
        return 'too_many', []
    elif len(args) == 0:
        return 'none', []
    else:
        return 'ok', args


def create_price_info_text(obj):
    text = ''
    for i, d in enumerate(obj):
        symbol = d.get('symbol', '???').upper()
        price_change = d.get('price_change_percentage_24h', 0)
        text += f'<b>🔥 Info about your coin(s) - {symbol.upper()}</b>:\n\n'
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
            if k in MAIN_RENAME_MAP:
                value = last_updated if k == 'last_updated' else v
                text += f"{MAIN_RENAME_MAP[k]}: <i>{value}</i>\n"

        text += "\n"
    return text


def create_top_capitalization_text(obj):
    text = f'<b>📎 Top {len(obj)} coins by capitalization</b>:\n📅 Relevant as of <ins>{datetime.today().strftime('%Y-%m-%d')}</ins>\n\n'
    for i, d in enumerate(obj):
        symbol = d.get('symbol', '???').upper()
        medal_text = add_medal(i)
        text += f"{i + 1}: <b>{symbol} {medal_text}</b>\n"

        for k, v in d.items():
            if k in TOP_CAPITALIZATION_RENAME_MAP:
                text += f"{TOP_CAPITALIZATION_RENAME_MAP[k]}: <i>${format_large_number(v)}</i>\n"

        text += "\n"
    return text


async def create_alert_task(bot, chat_id, symbol, timeout, price, direction="LONG"):
    end_time = datetime.now() + timedelta(hours=int(timeout))

    while datetime.now() < end_time:
        try:
            params = deepcopy(PARAMS)
            params['symbols'] = symbol
            response = requests.get(REQUEST_LINK_INFO_ABOUT_CRYPTO, params=params, headers=HEADERS).json()
            if not response or 'current_price' not in response[0]:
                await bot.send_message(chat_id=chat_id, text=f"⚠️ No data found for {symbol.upper()}!")
                return

            current_price = response[0]['current_price']
            price = float(price)

            if direction.upper() == "LONG" and current_price > price:
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"🔔 LONG alert: {symbol.upper()} > {price} → now {current_price}"
                )
                return

            elif direction.upper() == "SHORT" and current_price < price:
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"🔻 SHORT alert: {symbol.upper()} < {price} → now {current_price}"
                )
                return

        except Exception:
            await bot.send_message(chat_id=chat_id, text="⚠️ Error during alert check!")
            return

        await asyncio.sleep(60)

    await bot.send_message(chat_id=chat_id, text=f"⏰ Alert for {symbol.upper()} expired.")
