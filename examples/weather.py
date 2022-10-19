#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2022 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
3 Day weather forecast from the BBC.
"""

import sys
import time

from demo_opts import get_device
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT

try:
    import feedparser
except ImportError:
    print("The feedparser library was not found. Run 'sudo -H pip install feedparser' to install it.")
    sys.exit()


def main(num_iterations=sys.maxsize):
    # Go to https://www.bbc.com/weather and enter your town/city into
    # the 'Find a forecast' box. Then when you click through, substitute
    # the location_id below
    location_id = 2647428
    weather_rss_url = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/{location_id}"

    device = get_device()

    while num_iterations > 0:
        num_iterations -= 1

        feed = feedparser.parse(weather_rss_url)
        msg = feed["feed"]["title"]
        show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT))
        time.sleep(1)

        for items in feed["items"]:
            msg = items["title"]
            msg = msg.split(",")[0]
            show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT))
            time.sleep(1)

            for msg in items["description"].split(","):
                show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT))
                time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
