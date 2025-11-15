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
import signal
import sys
import time
import socket
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


class IPAddressChecker:
    def __init__(self, cache_duration_in_seconds=14400):
        """
        :param cache_duration_in_seconds: The duration in seconds to cache the IP address for. Default is 4 hours.
        """
        self._ip_address = None
        self._last_checked = None
        self._cache_duration = cache_duration_in_seconds

    def get_ip_address(self):
        if self._last_checked is None or time.time() - self._last_checked > self._cache_duration:
            self._ip_address = self._retrieve_ip_address()
            self._last_checked = time.time()
        return self._ip_address

    @staticmethod
    def _retrieve_ip_address():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))  # Google DNS. Probably will never be down.
                return s.getsockname()[0]
        except Exception as e:
            print(f"Error: {e}")
            return ""


def shutdown(signum, frame):
    device.clear()
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)


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

                if device.height >= (line_height * 5):
                    draw.text((2, line_height * 4), ip_address_checker.get_ip_address(), font=font2, fill="white")
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
        ip_address_checker = IPAddressChecker()
        main()
    except KeyboardInterrupt:
        pass
    finally:
        device.clear()
