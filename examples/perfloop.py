#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Simple benchmarking utility to measure performance.

Ported from:
https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/examples/shapes.py
"""

import sys
import time
from PIL import Image, ImageDraw

from luma.core.sprite_system import framerate_regulator
from demo_opts import get_device
import demo


def main():
    print("Testing display rendering performance")
    print("Press Ctrl-C to abort test\n")

    regulator = framerate_regulator(fps=0)  # Unlimited
    device = get_device()
    image = Image.new(device.mode, device.size)
    draw = ImageDraw.Draw(image)
    demo.primitives(device, draw)

    for i in range(5, 0, -1):
        sys.stdout.write(f"Starting in {i} seconds...\r")
        sys.stdout.flush()
        time.sleep(1)

    try:
        while True:
            with regulator:
                device.display(image)

            if regulator.called % 31 == 0:
                avg_fps = regulator.effective_FPS()
                avg_transit_time = regulator.average_transit_time()

                sys.stdout.write("#### iter = {0:6d}: render time = {1:.2f} ms, frame rate = {2:.2f} FPS\r".format(regulator.called, avg_transit_time, avg_fps))
                sys.stdout.flush()

    except KeyboardInterrupt:
        del image


if __name__ == "__main__":
    main()
