#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2022 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display basic system information.

Needs psutil (+ dependencies) installed::

  $ sudo apt-get install python-dev
  $ sudo -H pip install psutil
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

if os.name != 'posix':
    sys.exit(f'{os.name} platform is not supported')

from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont

try:
    import psutil
except ImportError:
    print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
    sys.exit()


# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return f"{n}B"


def cpu_usage():
    # cpu usage, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    cpu_percent = psutil.cpu_percent(interval=1)
    return "CPU: %d%% Up: %dd%dh%dm" % (cpu_percent, days, hours, minutes)


def mem_usage():
    usage = psutil.virtual_memory()
    return "RAM: %s/%s (%.0f%%)" % (
        bytes2human(usage.used),
        bytes2human(usage.total),
        usage.percent
    )


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD: %s/%s (%.0f%%)" % (
        bytes2human(usage.used),
        bytes2human(usage.total),
        usage.percent
    )


def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))


def stats(device):
    # use custom font
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', 'DejaVuSansMono.ttf'))
    font2 = ImageFont.truetype(font_path, 10)
    ascent, descent = font2.getmetrics()
    line_height = ascent + descent

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill=None)
        draw.text((2, line_height * 0), cpu_usage(), font=font2, fill="white")
        if device.height >= (line_height * 2):
            draw.text((2, line_height * 1), mem_usage(), font=font2, fill="white")

        if device.height >= (line_height * 3):
            draw.text((2, line_height * 2), disk_usage('/'), font=font2, fill="white")
            try:
                if device.height >= (line_height * 4):
                    draw.text((2, line_height * 3), network('wlan0'), font=font2, fill="white")
            except KeyError:
                # no wifi enabled/available
                pass


def main():
    while True:
        stats(device)
        time.sleep(5)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
