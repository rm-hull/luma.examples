#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2020 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

import sys
from pathlib import Path
from PIL import Image
from demo_opts import get_device

from luma.core.sprite_system import spritesheet, framerate_regulator


def main(num_iterations=sys.maxsize):
    data = {
        'image': str(Path(__file__).resolve().parent.joinpath('images', 'runner.png')),
        'frames': {
            'width': 64,
            'height': 67,
            'regX': 0,
            'regY': 2
        },
        'animations': {
            'run-right': {
                'frames': range(19, 9, -1),
                'next': "run-right",
            },
            'run-left': {
                'frames': range(0, 10),
                'next': "run-left"
            }
        }
    }

    regulator = framerate_regulator()
    sheet = spritesheet(**data)
    runner = sheet.animate('run-right')
    x = -sheet.frames.width
    dx = 3

    while num_iterations > 0:
        with regulator:
            num_iterations -= 1

            background = Image.new(device.mode, device.size, "white")
            background.paste(next(runner), (x, 0))
            device.display(background)
            x += dx

            if x >= device.width:
                runner = sheet.animate('run-left')
                dx = -dx

            if x <= -sheet.frames.width:
                runner = sheet.animate('run-right')
                dx = -dx


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
