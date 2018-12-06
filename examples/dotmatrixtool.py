#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Design a bitmap using http://dotmatrixtool.com/#, then paste the generated
hex values over those at lines 21-22.

See https://github.com/rm-hull/luma.led_matrix/issues/170
"""

import time
from demo_opts import get_device
from luma.core.render import canvas
from luma.core import legacy


def main():
    MY_CUSTOM_BITMAP_FONT = [
        [
            0x00, 0x3e, 0x08, 0x3e, 0x00, 0x3e, 0x2a, 0x22,
            0x00, 0x3e, 0x20, 0x20, 0x00, 0x3e, 0x0a, 0x0e
        ]
    ]

    device = get_device()
    with canvas(device) as draw:
        # Note that "\0" is the zero-th character in the font (i.e the only one)
        legacy.text(draw, (0, 0), "\0", fill="white", font=MY_CUSTOM_BITMAP_FONT)

    time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
