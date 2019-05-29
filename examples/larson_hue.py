#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-19 Richard Hull and contributors
# See LICENSE.rst for details.
#
# Based on https://github.com/pimoroni/blinkt/blob/master/examples/larson_hue.py

import math
import time
import colorsys

from demo_opts import get_device
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator


FALLOFF = 1.9
SCAN_SPEED = 3


def main():
    device = get_device()
    start_time = time.time()
    regulator = framerate_regulator(fps=10)

    while True:
        with regulator:
            delta = (time.time() - start_time)

            # Offset is a sine wave derived from the time delta
            # we use this to animate both the hue and larson scan
            # so they are kept in sync with each other
            offset = (math.sin(delta * SCAN_SPEED) + 1) / 2

            # Use offset to pick the right colour from the hue wheel
            hue = int(round(offset * 360))

            # Now we generate a value from 0 to 7
            offset = int(round(offset * device.width))

            with canvas(device, dither=True) as draw:
                for x in range(device.width):
                    sat = 1.0

                    val = (device.width - 1) - (abs(offset - x) * FALLOFF)
                    val /= (device.width - 1)  # Convert to 0.0 to 1.0
                    val = max(val, 0.0)  # Ditch negative values

                    xhue = hue  # Grab hue for this pixel
                    xhue += (1 - val) * 10  # Use the val offset to give a slight colour trail variation
                    xhue %= 360  # Clamp to 0-359
                    xhue /= 360.0  # Convert to 0.0 to 1.0

                    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(xhue, sat, val)]
                    draw.line((x, 0, x, device.height), fill=(r, g, b, int(val * 255)))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
