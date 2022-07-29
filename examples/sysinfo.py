#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2020 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK
# Just change the font to Raspberry Pi local font, so that once download the example, 
# you can adding to a service to run this code.

import os
import sys
import time
from pathlib import Path
from datetime import datetime
from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont
import psutil
import subprocess as sp


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
    return "%sB" % n


def cpu_usage():
    # load average
    av1, av2, av3 = os.getloadavg()
    return "Ld:%.1f %.1f %.1f " % (av1, av2, av3)


def uptime_usage():
    # uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    return "Up: %s" % (str(uptime).split('.')[0])

def ip_usage():
    # ip
    ip = sp.getoutput("hostname -I").split(' ')[0]
    return "IP: %s" % ip

def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
        % (bytes2human(usage.used), 100 - usage.percent)


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
        % (bytes2human(usage.used), usage.percent)


def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))


def stats(device):
    # use custom font
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
    font2 = ImageFont.truetype(font_path, 9)

    with canvas(device) as draw:
        draw.text((0, 0), cpu_usage(), font=font2, fill="white")
        if device.height >= 32:
            draw.text((0, 10), mem_usage(), font=font2, fill="white")

        if device.height >= 64:
            draw.text((0, 20), disk_usage('/'), font=font2, fill="white")
            try:
                draw.text((0, 30), network('wlan0'), font=font2, fill="white")
                draw.text((0, 40), uptime_usage(), font=font2, fill="white")
                draw.text((0, 50), ip_usage(), font=font2, fill="white")

            except KeyError:
                # no wifi enabled/available
                pass


device = get_device()

while True:
    stats(device)
    time.sleep(5)
