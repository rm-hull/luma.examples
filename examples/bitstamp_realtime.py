#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2022 Michael Svanström, Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Displays the latest Bitcoin trades in realtime at Bitstamp
"""

import sys
import time
import signal
import json
from pathlib import Path

try:
    import pusherclient
    global pusher
except ImportError:
    print("The pusherclient library was not found. Run 'sudo -H pip install pusherclient' to install it.")
    sys.exit()

from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont

# Bitstamp uses Pusher for websocket communication. This is their public Pusher key.
# Refer to https://www.bitstamp.net/websocket/ for more documentation.
BITSTAMP_PUSHER_KEY = 'de504dc5763aeef9ff52'

font_path = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
font = ImageFont.truetype(font_path, 12)

rows = []


# {"amount": 0.20952054000000001, "buy_order_id": 54237121,
# "sell_order_id": 54235858, "amount_str": "0.20952054",
# "price_str": "2190.00", "timestamp": "1500056837",
# "price": 2190.0, "type": 0, "id": 17270785}
def trade_callback(data):
    json_data = json.loads(data)

    str_row = f"${json_data['price_str']}  {json_data['amount']}"
    rows.insert(0, str_row)
    if len(rows) > 5:
        rows.pop()

    with canvas(device) as draw:
        for i, line in enumerate(rows):
            draw.text((0, 2 + (i * 12)), text=line, font=font, fill="white")


def connect_handler(data):
    channel = pusher.subscribe('live_trades')
    channel.bind('trade', trade_callback)


def show_loading():
    with canvas(device) as draw:
        draw.text((0, 0), "Awaiting a BTC trade...", font=font, fill="white")


def main():
    show_loading()
    while True:
        time.sleep(1)


def handler(signum, frame):
    pusher.disconnect()
    sys.exit()


pusher = pusherclient.Pusher(BITSTAMP_PUSHER_KEY)
pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
