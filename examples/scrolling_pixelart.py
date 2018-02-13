#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Another vertical scrolling demo, images (used without permission)
from @pixel_dailies twitter feed.
"""

import time
import random
import os.path
from demo_opts import get_device
from luma.core.virtual import viewport
from PIL import Image


def scroll_down(virtual, pos):
    x, y = pos
    if virtual.height > device.height:
        while y < virtual.height - device.height:
            virtual.set_position((x, y))
            y += 1
        y -= 1
    return (x, y)


def scroll_right(virtual, pos):
    x, y = pos
    if virtual.width > device.width:
        while x < virtual.width - device.width:
            virtual.set_position((x, y))
            x += 1
        x -= 1
    return (x, y)


def scroll_up(virtual, pos):
    x, y = pos
    while y >= 0:
        virtual.set_position((x, y))
        y -= 1
    y = 0
    return (x, y)


def scroll_left(virtual, pos):
    x, y = pos
    while x >= 0:
        virtual.set_position((x, y))
        x -= 1
    x = 0
    return (x, y)


def main():
    images = [
        "pixelart1.png",
        "pixelart2.png",
        "pixelart3.jpg",
        "pixelart4.jpg",
        "pixelart5.jpg"
    ]

    while True:
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
            'images', random.choice(images)))
        pixel_art = Image.open(img_path).convert(device.mode)
        w, h = pixel_art.size

        virtual = viewport(device, width=w, height=h)

        virtual.display(pixel_art)

        time.sleep(2)

        pos = (0, 0)
        pos = scroll_down(virtual, pos)
        time.sleep(2)
        pos = scroll_right(virtual, pos)
        time.sleep(2)
        pos = scroll_up(virtual, pos)
        time.sleep(2)
        pos = scroll_left(virtual, pos)
        time.sleep(2)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
