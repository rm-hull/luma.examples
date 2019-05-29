#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-19 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
The Matrix.

Adapted from:
https://github.com/pimoroni/unicorn-hat-hd/blob/master/examples/matrix-hd.py
"""

from random import randint, gauss
from demo_opts import get_device
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator


def matrix(device):
    wrd_rgb = [
        (154, 173, 154),
        (0, 255, 0),
        (0, 235, 0),
        (0, 220, 0),
        (0, 185, 0),
        (0, 165, 0),
        (0, 128, 0),
        (0, 0, 0),
        (154, 173, 154),
        (0, 145, 0),
        (0, 125, 0),
        (0, 100, 0),
        (0, 80, 0),
        (0, 60, 0),
        (0, 40, 0),
        (0, 0, 0)
    ]

    clock = 0
    blue_pilled_population = []
    max_population = device.width * 8
    regulator = framerate_regulator(fps=10)

    def increase_population():
        blue_pilled_population.append([randint(0, device.width), 0, gauss(1.2, 0.6)])

    while True:
        clock += 1
        with regulator:
            with canvas(device, dither=True) as draw:
                for person in blue_pilled_population:
                    x, y, speed = person
                    for rgb in wrd_rgb:
                        if 0 <= y < device.height:
                            draw.point((x, y), fill=rgb)
                        y -= 1
                    person[1] += speed

        if clock % 5 == 0 or clock % 3 == 0:
            increase_population()

        while len(blue_pilled_population) > max_population:
            blue_pilled_population.pop(0)


if __name__ == "__main__":
    try:
        matrix(get_device())
    except KeyboardInterrupt:
        pass
