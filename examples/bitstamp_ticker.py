#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Michael Svanström, Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Displays the Bitcoin price at Bitstamp

Example:

BTC/USD $2300.00
24h Hi $2400.00 Lo $2200.00
LTC/USD $40.00
24h Hi $50.00 Lo $30.00
"""

import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("The requests library was not found. Run 'sudo -H pip install requests' to install it.")
    sys.exit()

from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont


def fetch_price(crypto_currency, fiat_currency):
    bitstamp_api = "https://www.bitstamp.net/api/v2/ticker/" + crypto_currency.lower() + fiat_currency.lower()
    try:
        r = requests.get(bitstamp_api)
        return r.json()
    except:
        print("Error fetching from Bitstamp API")


def get_price_text(crypto_currency, fiat_currency):
    data = fetch_price(crypto_currency, fiat_currency)
    return [
        '{}/{} {}'.format(crypto_currency, fiat_currency, data['last']),
        '24h Hi {} Lo {}'.format(data['high'], data['low'])
    ]


def show_price(device):
    # use custom font
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 12)

    with canvas(device) as draw:
        rows = get_price_text("BTC", "USD")
        draw.text((0, 0), rows[0], font=font2, fill="white")
        draw.text((0, 14), rows[1], font=font2, fill="white")

        if device.height >= 64:
            rows = get_price_text("LTC", "USD")
            draw.text((0, 28), rows[0], font=font2, fill="white")
            draw.text((0, 42), rows[1], font=font2, fill="white")


def main():
    while True:
        show_price(device)
        time.sleep(60)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
